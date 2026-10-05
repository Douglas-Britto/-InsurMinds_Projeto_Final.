# ==============================================================================
# BLOCO 1: IMPORTAÇÃO DA BIBLIOTECA NATIVA DE BANCO DE DADOS
# ==============================================================================
# Comentário: Importa o módulo sqlite3, que manipula bancos de dados locais em formato de arquivo.
import sqlite3
import json

# ==============================================================================
# BLOCO 2: FUNÇÃO PARA CRIAÇÃO FÍSICA DA TABELA RELACIONAL (D&O MODEL)
# ==============================================================================
def inicializar_banco():
    # Comentário: Conecta ao arquivo do banco. Se não existir, o Python cria o arquivo na hora.
    conexao = sqlite3.connect("auditoria_apolices.db")
    cursor = conexao.cursor()
    
    # Comentário: Cria a tabela estruturada mapeando as variáveis regulatórias do Ramo D&O.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS apolices_d_o (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seguradora TEXT NOT NULL,
            numero_apolice TEXT UNIQUE NOT NULL,
            processo_susep TEXT,
            vigencia_inicio TEXT,
            vigencia_fim TEXT,
            limite_global_lmi REAL,
            franquia_cobertura_a TEXT,
            franquia_cobertura_b REAL,
            custos_defesa_sublimitados INTEGER, -- Comentário: 0 para Não, 1 para Sim
            custos_defesa_descricao TEXT,
            email_sinistro TEXT,
            prazo_notificacao_dias INTEGER,
            json_bruto TEXT -- Comentário: Guarda a cópia de segurança do JSON gerado pela IA
        )
    """)
    
    conexao.commit()
    conexao.close()
    print("[Banco de Dados]: Arquivo 'auditoria_apolices.db' inicializado com sucesso.")

# ==============================================================================
# BLOCO 3: FUNÇÃO DE INSERÇÃO E EXTRAÇÃO LÓGICA DO JSON PARA O BANCO
# ==============================================================================
def salvar_apolice_no_banco(string_json_ia):
    if not string_json_ia:
        print("[Erro Banco]: Impossível gravar um JSON nulo.")
        return False
        
    try:
        # Comentário: Transforma o texto vindo da IA em um dicionário de dados do Python.
        dados = json.loads(string_json_ia)
        
        # Comentário: Navega pelas chaves exatas geradas pelo Gemini 3.6 Flash.
        dados_gerais = dados.get("dados_apolice", {})
        garantias = dados.get("garantias_e_limites", {})
        procedimento = dados.get("procedimento_sinistro", {})
        
        seguradora = dados_gerais.get("seguradora")
        num_apolice = dados_gerais.get("numero_apolice")
        susep = dados_gerais.get("registro_susep")
        inicio = dados_gerais.get("vigencia_inicio")
        fim = dados_gerais.get("vigencia_fim")
        
        lmi = garantias.get("limite_maximo_garantia_global")
        fran_a = garantias.get("cobertura_a_direta_executivos", {}).get("franquia")
        fran_b = garantias.get("cobertura_b_reembolso_companhia", {}).get("franquia")
        
        c_defesa = garantias.get("custos_de_defesa", {})
        sublimitado = 1 if c_defesa.get("sublimite_restritivo") else 0
        desc_defesa = c_defesa.get("descricao_limite")
        
        email = procedimento.get("email_notificacao")
        prazo_notif = procedimento.get("prazo_notificacao_dias")

        # Comentário: Conecta e executa a gravação dos dados limpos nas colunas do banco.
        conexao = sqlite3.connect("auditoria_apolices.db")
        cursor = conexao.cursor()
        
        # Comentário: Se a apólice já existir, ele atualiza os dados antigos (UPSERT).
        cursor.execute("""
            INSERT OR REPLACE INTO apolices_d_o (
                seguradora, numero_apolice, processo_susep, vigencia_inicio, vigencia_fim,
                limite_global_lmi, franquia_cobertura_a, franquia_cobertura_b,
                custos_defesa_sublimitados, custos_defesa_descricao, email_sinistro,
                prazo_notificacao_dias, json_bruto
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            seguradora, num_apolice, susep, inicio, fim,
            lmi, str(fran_a), float(fran_b) if fran_b else 0.0,
            sublimitado, desc_defesa, email, prazo_notif, string_json_ia
        ))
        
        conexao.commit()
        conexao.close()
        print(f"[Banco de Dados]: Dados da {seguradora} persistidos com sucesso.")
        return True
        
    except Exception as e:
        print(f"[Erro Banco]: Falha ao processar e salvar: {e}")
        return False

# ==============================================================================
# BLOCO 4: INTERFACE DE EXECUÇÃO ISOLADA PARA TESTE DO PASSO 4
# ==============================================================================
if __name__ == "__main__":
    # Comentário: Executa a criação física da tabela quando rodamos este arquivo sozinho.
    inicializar_banco()
