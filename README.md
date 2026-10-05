# Comparador de Apólices de Seguro D&O com IA 📑🤖

## 📋 Descrição do Projeto
Este projeto consiste em uma ferramenta baseada em Inteligência Artificial desenvolvida para automatizar a análise, extração e comparação de dados presentes em apólices de seguro **D&O (Directors and Officers)**. 

O sistema realiza o processamento de documentos PDF de diferentes seguradoras (como Chubb, Tokio Marine e Allianz), armazena as informações estruturadas em um banco de dados local e utiliza modelos de linguagem (IA) para cruzar cláusulas complexas e identificar discrepâncias de cobertura de forma automatizada.

---

## 🛠️ Tecnologias Utilizadas
*   **Linguagem Principal:** Python 3.10
*   **Interface do Usuário:** Streamlit
*   **Inteligência Artificial:** Google Gemini API (módulo `extracao_gemini.py`)
*   **Banco de Dados:** SQLite (`auditoria_apolices.db`)

---

## ⚙️ Instruções de Instalação

1. Clone este repositório público no seu computador:
   ```bash
   git clone https://github.com[SEU_USUARIO_GITHUB]/[NOME_DO_REPOSITORIO].git
   ```
2. Acesse a pasta do projeto:
   ```bash
   cd [NOME_DO_REPOSITORIO]
   ```
3. Ative o ambiente virtual (`venv`) que já está configurado na máquina.

---

## 🚀 Instruções de Execução

Para iniciar a interface visual do projeto e realizar as consultas, execute o seguinte comando no terminal:
```bash
streamlit run src/app_streamlit.py
```

---

## 👥 Identificação dos Integrantes
*   **[Nome Completo 1]** - RM: [Número]
*   **[Nome Completo 2]** - RM: [Número]
*   **[Nome Completo 3]** - RM: [Número]

---

## 📄 Licença
Este projeto está sob a licença MIT. consulte o arquivo LICENSE para obter mais detalhes.
