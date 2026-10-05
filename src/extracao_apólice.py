# ==============================================================================
# BLOCO 1: IMPORTAÇÃO DO SDK OFICIAL DA GOOGLE IA E BIBLIOTECAS PADRÃO
# ==============================================================================
# Comentário: Importa os módulos necessários do Google GenAI para autenticação e chamadas.
import os
from google import genai
from google.genai import types

# Comentário: Inicializa o cliente do Gemini.
# SUBSTITUA 'SUA_CHAVE_AQUI' pela chave real copiada do site do Google AI Studio.
client = genai.Client(api_key="AQ.Ab8RN6LKqg1EDvaSD0f9wmxBmh1gPVjT5y_eC4ADkNs3vKzICw")

# ==============================================================================
# BLOCO 2: FUNÇÃO MESTRE MULTIMODAL DE EXTRAÇÃO E FORMATAÇÃO JSON
# ==============================================================================
# Comentário: Função que lê o arquivo PDF binário e orquestra a chamada de inteligência.
def analisar_apolice_com_gemini(caminho_pdf):
    print(f"\n[Gemini 2.5 Flash]: Abrindo e analisando o arquivo digital: {caminho_pdf}...")
    
    # Comentário: Executa a leitura física dos bytes do PDF para envio direto na chamada.
    with open(caminho_pdf, "rb") as f:
        pdf_bytes = f.read()

    # Comentário: Engenharia de prompt baseada nas regras de negócio da SUSEP para o Ramo D&O.
    prompt_sistema = """
    Você é um auditor automatizado especialista em seguros corporativos de Linhas Financeiras (D&O).
    Sua tarefa é analisar o frontispício desta apólice digital e extrair rigorosamente os dados contratuais.
    Você deve mapear e agrupar as informações exatamente na estrutura JSON solicitada abaixo.
    
    Atenção às regras atuariais de D&O:
    - O Limite Financeiro Global deve ser capturado como número puro (float).
    - Diferencie a Franquia da Cobertura A (Pessoa Física) que geralmente é Isenta da Franquia da Cobertura B (Reembolso à Empresa).
    - Identifique se os Custos de Defesa consomem o limite global livremente ou se possuem um Sub-limite restritivo.
    - Capture o rito de acionamento de sinistro (prazos e canais de e-mail).
    """

    try:
        # Comentário: Dispara a requisição multimodal para o modelo Gemini 2.5 Flash.
        resposta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=pdf_bytes,
                    mime_type='application/pdf',
                ),
                prompt_sistema
            ],
            # Comentário: Configura o Modo de Saída Estruturada forçando a IA a devolver apenas JSON válido.
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1 # Comentário: Temperatura baixa (0.1) anula riscos de alucinação do modelo.
            )
        )
        
        # Comentário: Retorna a string do objeto JSON estruturado gerado pela IA.
        return resposta.text

    except Exception as e:
        print(f"Erro crítico na conexão com a API do Gemini: {e}")
        return None

# ==============================================================================
# BLOCO 3: PONTO DE ENTRADA DO SCRIPT PARA TESTE INDIVIDUAL DAS EXTRAÇÕES
# ==============================================================================
if __name__ == "__main__":
    
    # Comentário: Executa o teste de leitura automatizada do primeiro PDF (Padrão Chubb)
    if os.path.exists("apolice_real_chubb.pdf"):
        json_chubb = analisar_apolice_com_gemini("apolice_real_chubb.pdf")
        print("\n========================================================")
        print("--- JSON ESTRUTURADO EXTRAÍDO DA APÓLICE CHUBB ---")
        print("========================================================")
        print(json_chubb)
        
    # Comentário: Executa o teste de leitura automatizada do segundo PDF (Padrão Tokio Marine)
    if os.path.exists("apolice_real_tokio.pdf"):
        json_tokio = analisar_apolice_com_gemini("apolice_real_tokio.pdf")
        print("\n========================================================")
        print("--- JSON ESTRUTURADO EXTRAÍDO DA APÓLICE TOKIO MARINE ---")
        print("========================================================")
        print(json_tokio)
