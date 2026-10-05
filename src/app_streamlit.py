# ==============================================================================
# BLOCO 1: IMPORTAÇÃO DE FRAMEWORKS GRÁFICOS, BANCO, TEMPO E SDK DA GOOGLE IA
# ==============================================================================
import streamlit as st
import sqlite3
import pandas as pd
import time
from google import genai
from google.genai import types

# ==============================================================================
# BLOCO 2: CONFIGURAÇÃO DE IDENTIDADE VISUAL CORPORATIVA (MODO ESCURO)
# ==============================================================================
st.set_page_config(
    page_title="D&O Audit Intel | Terminal de Riscos Executivos",
    page_icon="🛡️",
    layout="wide"
)

# Inicializa o cliente do Gemini usando a nova biblioteca SDK oficial da Google.
client = genai.Client(api_key="AQ.Ab8RN6LKqg1EDvaSD0f9wmxBmh1gPVjT5y_eC4ADkNs3vKzICw")

# ==============================================================================
# BLOCO 3: ACESSO À CAMADA DE DADOS DO BANCO (ETAPA 5)
# ==============================================================================
def carregar_dados_banco_local():
    try:
        conexao = sqlite3.connect("auditoria_apolices.db")
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM apolices_d_o")
        linhas = cursor.fetchall()
        conexao.close()
        return linhas
    except Exception:
        return []

lista_apolices = carregar_dados_banco_local()

# ==============================================================================
# BLOCO 4: MENU LATERAL DE GOVERNANÇA (SIDEBAR DESIGN)
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🛡️</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #6366F1;'>D&O AUDIT INTEL</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ⚙️ Conectividade")
    if len(lista_apolices) >= 2:
        st.success("SISTEMA ONLINE (SQLite)")
    else:
        st.error("AGUARDANDO DADOS")
    st.markdown("---")
    st.caption("Plataforma de auditoria preditiva estruturada sob as Circulares de Riscos de Danos da SUSEP.")

# ==============================================================================
# BLOCO 5: INTERFACE PRINCIPAL
# ==============================================================================
if len(lista_apolices) < 2:
    st.error("❌ Banco de dados offline ou incompleto. Certifique-se de que os dados foram inseridos no SQLite.")
else:
    ap1 = lista_apolices[0]  
    ap2 = lista_apolices[1]  

    st.title("🛡️ Terminal Analítico de Riscos Executivos (D&O)")
    st.markdown("Plataforma inteligente para cruzamentos de apólices digitais cíveis e detecção de assimetrias contratuais.")
    st.markdown("---")

    # Painel de Indicadores de Impacto Financeiro (Métricas Neon)
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(
            label="Diferença de Cobertura Global (LMI)", 
            value=f"R$ {abs(float(ap1['limite_global_lmi']) - float(ap2['limite_global_lmi'])):,.2f}", 
            delta="Gap de Exposição Patrimonial"
        )
    with col_m2:
        st.metric(
            label="Disparidade de Franquia PJ (Co. B)", 
            value=f"R$ {abs(float(ap1['franquia_cobertura_b']) - float(ap2['franquia_cobertura_b'])):,.2f}", 
            delta="Impacto de Caixa Imediato", 
            delta_color="inverse"
        )
    with col_m3:
        st.metric(
            label="Análise de Vulnerabilidade", 
            value="1 Cláusula Crítica", 
            delta="Risco Técnico Identificado", 
            delta_color="off"
        )

    st.markdown("---")

    # Navegação por Abas Horizontais Profissionais
    aba_tabela, aba_auditoria, aba_chat = st.tabs([
        "📊 Matriz Comparativa Estruturada", 
        "🧠 Diagnóstico de Assimetrias",
        "💬 Consultar Assistente com IA"
    ])

    # ABA 1: Grade Eletrônica de Dados
    with aba_tabela:
        st.markdown("### Grade de Dados Normalizada (Padrão de Mercado)")
        dados_plataforma = {
            "Métricas de Controle Contratual": [
                "Seguradora Emitente", "Processo de Homologação SUSEP", "Número de Identificação da Apólice",
                "Teto Máximo de Indenização (LMI Global)", "Participação Segurado Pessoa Física (Co. A)",
                "Franquia Reembolso Corporativo (Co. B)", "Regra de Custos de Defesa Judicial"
            ],
            f"Proposta 01 ({ap1['seguradora']})": [
                ap1['seguradora'], ap1['processo_susep'], ap1['numero_apolice'],
                f"R$ {float(ap1['limite_global_lmi']):,.2f}", ap1['franquia_cobertura_a'],
                f"R$ {float(ap1['franquia_cobertura_b']):,.2f}", ap1['custos_defesa_descricao']
            ],
            f"Proposta 02 ({ap2['seguradora']})": [
                ap2['seguradora'], ap2['processo_susep'], ap2['numero_apolice'],
                f"R$ {float(ap2['limite_global_lmi']):,.2f}", ap2['franquia_cobertura_a'],
                f"R$ {float(ap2['franquia_cobertura_b']):,.2f}", ap2['custos_defesa_descricao']
            ]
        }
        df = pd.DataFrame(dados_plataforma)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ABA 2: Relatório Clínico Determinado por Código
    with aba_auditoria:
        st.markdown("### Relatório de Engenharia de Riscos e Vulnerabilidades")
        if float(ap1['limite_global_lmi']) != float(ap2['limite_global_lmi']):
            maior_lmi = ap1 if float(ap1['limite_global_lmi']) > float(ap2['limite_global_lmi']) else ap2
            st.warning(f"⚠️ **Vulnerabilidade de Escopo:** A companhia **{maior_lmi['seguradora']}** reduz a exposição ao risco patrimonial por entregar um limite de indenização expandido.")

        if float(ap1['franquia_cobertura_b']) != float(ap2['franquia_cobertura_b']):
            menor_fran = ap1 if float(ap1['franquia_cobertura_b']) < float(ap2['franquia_cobertura_b']) else ap2
            st.success(f"🟢 **Otimização de Caixa:** A franquia de reembolso à sociedade da **{menor_fran['seguradora']}** é financeiramente mais vantajosa para a saúde fiscal do Tomador.")

        st.markdown("#### Parecer sobre Escopo de Defesa Jurídica")
        if int(ap1['custos_defesa_sublimitados']) == 1:
            st.error(f"🔴 **Gargalo Técnico Detectado:** A apólice da **{ap1['seguradora']}** impõe barreira contratual por sublimitar as despesas judiciais (*{ap1['custos_defesa_descricao']}*).")
        if int(ap2['custos_defesa_sublimitados']) == 1:
            st.error(f"🔴 **Gargalo Técnico Detectado:** A apólice da **{ap2['seguradora']}** impõe barreira contratual por sublimitar as despesas judiciais (*{ap2['custos_defesa_descricao']}*).")

    # ABA 3: Camada Conversacional Estabilizada (Antibug Estruturado)
    with aba_chat:
        st.markdown("### 💬 Tire suas dúvidas sobre as apólices com a IA")
        
        if "resposta_guardada" not in st.session_state:
            st.session_state.resposta_guardada = ""
        if "pergunta_guardada" not in st.session_state:
            st.session_state.pergunta_guardada = ""

        pergunta_usuario = st.text_input("Digite sua dúvida aqui (Pressione Enter para enviar):", key="campo_pergunta")
        
        area_status = st.empty()
        area_resposta = st.empty()
        
        if pergunta_usuario and pergunta_usuario != st.session_state.pergunta_guardada:
            area_status.info("🧠 Analisando cláusulas contratuais com Gemini, aguarde...")
            
            prompt_dados = f"D&O Analista. P1: {ap1['seguradora']}, LMI {ap1['limite_global_lmi']}, PF {ap1['franquia_cobertura_a']}, PJ {ap1['franquia_cobertura_b']}. P2: {ap2['seguradora']}, LMI {ap2['limite_global_lmi']}, PF {ap2['franquia_cobertura_a']}, PJ {ap2['franquia_cobertura_b']}. Pergunta: {pergunta_usuario}"
            
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt_dados
                )
                st.session_state.pergunta_guardada = pergunta_usuario
                st.session_state.resposta_guardada = response.text
                area_status.empty()
            except Exception as e:
                area_status.empty()
                st.error(f"Falha na IA: {e}")
        
        if st.session_state.resposta_guardada:
            with area_resposta.container():
                st.markdown("---")
                st.markdown(f"**🧑‍💻 Sua pergunta:** {st.session_state.pergunta_guardada}")
                st.markdown("### 🧠 Resposta do Auditor AI:")
                st.write(st.session_state.resposta_guardada)
