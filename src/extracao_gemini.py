# ==============================================================================
# BLOCO 1: IMPORTAÇÃO DE BIBLIOTECAS, SDK DA GOOGLE E SCRIPT DO BANCO LOCAL
# ==============================================================================
# Comentário: Importa módulos de tempo, o SDK da Google e a função de salvamento do SQLite.
import os
import time
from google import genai
from google.genai import types
from banco_dados import inicializar_banco, salvar_apolice_no_banco

# Comentário: Inicializa o cliente do Gemini usando a nova biblioteca SDK oficial.
# SUBSTITUA 'SUA_CHAVE_AQUI' pela chave real copiada do site do Google AI Studio.
client = genai.Client(api_key="AQ.Ab8RN6LKqg1EDvaSD0f9wmxBmh1gPVjT5y_eC4ADkNs3vKzICw")

# ==============================================================================
# BLOCO 2: FUNÇÃO MESTRE MULTIMODAL COM LÓGICA ANTI-ERRO 503 (RETRY LOGIC)
# ==============================================================================
def analisar_apolice_com_gemini(caminho_pdf):
    # Comentário: Define os parâmetros de resiliência caso os servidores gratuitos oscilem.
    max_tentativas = 3
    pausa_segundos = 6
    
    # Comentário: Abre o PDF digital em formato de leitura de bytes binários.
    with open(caminho_pdf, "rb") as f:
        pdf_bytes = f.read()

    # Comentário: Engenharia de prompt baseada estritamente no Ramo de Seguros D&O e SUSEP.
    prompt_sistema = """
    Você é um auditor automatizado especialista em seguros corporativos de Linhas Financeiras (D&O).
    Analise o frontispício desta apólice digital e extraia rigorosamente os dados contratuais.
    Você deve mapear e agrupar as informações exatamente na estrutura JSON solicitada abaixo.
    
    Atenção às chaves obrigatórias do JSON:
    {
      "dados_apolice": {
        "numero_apolice": "String",
        "seguradora": "String",
        "cnpj_seguradora": "String",
        "registro_susep": "String",
        "vigencia_inicio": "String",
        "vigencia_fim": "String"
      },
      "garantias_e_limites": {
        "limite_maximo_garantia_global": 0.00,
        "cobertura_a_direta_executivos": {"franquia": "String"},
        "cobertura_b_reembolso_companhia": {"franquia": 0.00},
        "custos_de_defesa": {
          "sublimite_restritivo": true/false,
          "descricao_limite": "String"
        }
      },
      "procedimento_sinistro": {
        "email_notificacao": "String",
        "prazo_notificacao_dias": 0
      }
    }
    """

    # Comentário: Loop estruturado para interceptar e contornar erros de indisponibilidade (HTTP 503).
    for tentativa in range(1, max_tentativas + 1):
        print(f"[Gemini 3.6 Flash] Tentativa {tentativa}/{max_tentativas}: Processando {caminho_pdf}...")
        
        try:
            resposta = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=[
                    types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'),
                    prompt_sistema
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1 # Comentário: Baixa temperatura elimina o risco de alucinações matemáticas.
                )
            )
            # Comentário: Se obteve sucesso na comunicação, retorna o JSON puro que a IA gerou.
            return resposta.text
            
        except Exception as e:
            print(f"⚠️ Alerta: Servidor da Google instável. (Motivo: {e})")
            if tentativa < max_tentativas:
                print(f" Ativando pausa de {pausa_segundos} segundos antes de tentar novamente...")
                time.sleep(pausa_segundos)
            else:
                print("❌ Limite de tentativas esgotado. Erro de infraestrutura externa.")
                return None

# ==============================================================================
# BLOCO 3: ORQUESTRAÇÃO COMPLETA DO PIPELINE (IA + SQLITE PERSISTENCE)
# ==============================================================================
if __name__ == "__main__":
    print("========================================================================")
    print("INICIANDO PIPELINE AUTOMATIZADO: EXTRAÇÃO + ORGANIZAÇÃO + ARMAZENAMENTO")
    print("========================================================================")
    
    # Passo A: Garante que a estrutura física das tabelas do SQLite está criada na pasta.
    inicializar_banco()
    
    # Passo B: Executa a leitura e gravação da Apólice 1 (Chubb D&O)
    if os.path.exists("apolice_real_chubb.pdf"):
        json_chubb = analisar_apolice_com_gemini("apolice_real_chubb.pdf")
        if json_chubb:
            print("\n✅ Sucesso na extração da Apólice Chubb! Gravando no banco...")
            salvar_apolice_no_banco(json_chubb)
            print("-" * 72)
            
    # Passo C: Executa a leitura e gravação da Apólice 2 (Tokio Marine D&O)
    if os.path.exists("apolice_real_tokio.pdf"):
        json_tokio = analisar_apolice_com_gemini("apolice_real_tokio.pdf")
        if json_tokio:
            print("\n✅ Sucesso na extração da Apólice Tokio Marine! Gravando no banco...")
            salvar_apolice_no_banco(json_tokio)
            print("-" * 72)
            
    print("\n[Pipeline Concluído]: Os dados lidos pela IA estão salvos de forma estruturada!")
