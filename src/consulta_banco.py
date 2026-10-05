# ==============================================================================
# BLOCO 1: IMPORTAÇÃO DA BIBLIOTECA NATIVA DE BANCO DE DADOS RELACIONAL
# ==============================================================================
# Comentário: Importa o sqlite3 para abrir e ler o arquivo de banco de dados local.
import sqlite3

# ==============================================================================
# BLOCO 2: FUNÇÃO MESTRE DE CONSULTA E EXTRAÇÃO DE DADOS (READ LAYER)
# ==============================================================================
def consultar_todas_apolices():
    print("\n[Etapa 5 - Consulta]: Conectando ao banco SQLite para recuperar registros...")
    
    # Comentário: Abre a conexão física com o arquivo de banco gerado na etapa anterior.
    conexao = sqlite3.connect("auditoria_apolices.db")
    
    # Comentário: Configura o row_factory para fazer o SQLite retornar os dados como um Dicionário.
    # Comentário: Isso permite acessar as colunas pelo nome (ex: apolice['seguradora']) e não por números.
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    
    # Comentário: Executa a query SQL clássica de seleção para trazer todas as colunas da tabela.
    cursor.execute("""
        SELECT 
            seguradora, 
            numero_apolice, 
            processo_susep, 
            vigencia_inicio, 
            vigencia_fim, 
            limite_global_lmi, 
            franquia_cobertura_a, 
            franquia_cobertura_b, 
            custos_defesa_sublimitados, 
            custos_defesa_descricao, 
            email_sinistro, 
            prazo_notificacao_dias
        FROM apolices_d_o
    """)
    
    # Comentário: Captura todas as linhas encontradas pelo banco de dados na consulta.
    linhas = cursor.fetchall()
    
    # Comentário: Fecha a conexão com o arquivo para liberar a memória do sistema operacional.
    conexao.close()
    
    print(f"[Etapa 5 - Consulta]: {len(linhas)} registro(s) encontrado(s) e carregado(s) com sucesso.\n")
    return linhas

# ==============================================================================
# BLOCO 3: AMBIENTE DE EXECUÇÃO E IMPRESSÃO PARA VALIDAÇÃO DO ESTUDO
# ==============================================================================
if __name__ == "__main__":
    # Comentário: Dispara a função de leitura para testar o script de forma isolada.
    lista_apolices = consultar_todas_apolices()
    
    # Comentário: Itera (passa por cada linha) sobre os registros recuperados do banco de dados.
    for i, apolice in enumerate(lista_apolices, 1):
        print(f"--- [REGISTRO {i}] ---")
        print(f"🏢 Seguradora: {apolice['seguradora']}")
        print(f"📄 Nº Apólice: {apolice['numero_apolice']}")
        print(f"💰 Limite Global (LMI): R$ {apolice['limite_global_lmi']:,.2f}")
        print(f"🛡️ Franquia Pessoa Física (Co. A): {apolice['franquia_cobertura_a']}")
        print(f"🏢 Franquia Corporativa (Co. B): R$ {apolice['franquia_cobertura_b']:,.2f}")
        print(f"⚖️ Defesa Sublimitada? {'SIM' if apolice['custos_defesa_sublimitados'] == 1 else 'NÃO'}")
        print(f"📝 Regra de Defesa: {apolice['custos_defesa_descricao']}")
        print(f"📬 E-mail Sinistros: {apolice['email_sinistro']}")
        print(f"⏱️ Prazo Notificação: {apolice['prazo_notificacao_dias']} dias")
        print("-" * 50)
pyt