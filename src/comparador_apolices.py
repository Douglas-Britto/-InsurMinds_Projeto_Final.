# ==============================================================================
# BLOCO 1: IMPORTAÇÃO DA CAMADA DE CONSULTA (ETAPA 5)
# ==============================================================================
# Comentário: Importa a função do arquivo anterior para ler os dados do SQLite.
from consulta_banco import consultar_todas_apolices

# ==============================================================================
# BLOCO 2: FUNÇÃO MESTRE DE COMPARAÇÃO E ANÁLISE DE ASSIMETRIAS (ETAPA 6)
# ==============================================================================
def executar_comparacao_auditoria():
    # Comentário: Executa a Etapa 5 para carregar as apólices guardadas no banco.
    apolices = consultar_todas_apolices()
    
    # Comentário: Validação de segurança. Se não houver pelo menos 2 apólices, cancela.
    if len(apolices) < 2:
        print("[Erro Etapa 6]: São necessárias pelo menos 2 apólices no banco para comparar.")
        return None
        
    # Comentário: Isola os dois registros do banco em variáveis locais.
    ap1 = apolices[0]
    ap2 = apolices[1]
    
    print("========================================================================")
    print("        ETAPA 6 - MOTOR DE AUDITORIA: RELATÓRIO DE ASSIMETRIAS          ")
    print("========================================================================")
    
    # --- ASSIMETRIA 1: CAPACIDADE FINANCEIRA (LIMITE MÁXIMO DE INDENIZAÇÃO - LMI) ---
    print("\n[Métrica 1] Limite Máximo de Indenização Global (LMI):")
    diff_lmi = abs(ap1['limite_global_lmi'] - ap2['limite_global_lmi'])
    
    if ap1['limite_global_lmi'] > ap2['limite_global_lmi']:
        print(f" 🔴 Diferença detectada: A {ap1['seguradora']} oferece R$ {diff_lmi:,.2f} A MAIS de proteção total que a {ap2['seguradora']}.")
    elif ap2['limite_global_lmi'] > ap1['limite_global_lmi']:
        print(f" 🔴 Diferença detectada: A {ap2['seguradora']} oferece R$ {diff_lmi:,.2f} A MAIS de proteção total que a {ap1['seguradora']}.")
    else:
        print(" Ambas as seguradoras oferecem limites financeiros idênticos.")

    # --- ASSIMETRIA 2: RENTENÇÃO CORPORATIVA (FRANQUIA COBERTURA B) ---
    print("\n[Métrica 2] Franquia de Reembolso Corporativo (Cobertura B):")
    diff_fran = abs(ap1['franquia_cobertura_b'] - ap2['franquia_cobertura_b'])
    
    if ap1['franquia_cobertura_b'] < ap2['franquia_cobertura_b']:
        print(f" 🟢 Vantagem Financeira: A {ap1['seguradora']} possui franquia corporativa R$ {diff_fran:,.2f} MAIS BARATA que a {ap2['seguradora']}.")
    elif ap2['franquia_cobertura_b'] < ap1['franquia_cobertura_b']:
        print(f" 🟢 Vantagem Financeira: A {ap2['seguradora']} possui franquia corporativa R$ {diff_fran:,.2f} MAIS BARATA que a {ap1['seguradora']}.")
    else:
        print(" Ambas as apólices exigem a mesma participação obrigatória (franquia).")

    # --- ASSIMETRIA 3: CLAUSULADO DE RISCO (CUSTOS DE DEFESA JUDICIAL) ---
    print("\n[Métrica 3] Análise Restritiva de Cláusulas (Custos de Defesa):")
    if ap1['custos_defesa_sublimitados'] != ap2['custos_defesa_sublimitados']:
        print(" ⚠️ ASSIMETRIA CRÍTICA DE RISCO DETECTADA:")
        if ap1['custos_defesa_sublimitados'] == 1:
            print(f" -> A apólice da {ap1['seguradora']} é RESTRITIVA: {ap1['custos_defesa_descricao']}.")
        if ap2['custos_defesa_sublimitados'] == 1:
            print(f" -> A apólice da {ap2['seguradora']} é RESTRITIVA: {ap2['custos_defesa_descricao']}.")
        print(" -> Recomendação jurídica: Priorizar a apólice com custos de defesa livres (Sem Sublimites).")
    else:
        print(" Ambas utilizam o mesmo mecanismo padrão de tratamento de despesas judiciais.")
        
    print("\n========================================================================")
    print("[Análise Concluída]: Assimetrias extraídas e prontas para a Interface.")
    print("========================================================================")

# ==============================================================================
# BLOCO 3: AMBIENTE DE EXECUÇÃO ISOLADO PARA VALIDAÇÃO DO PROCESSO
# ==============================================================================
if __name__ == "__main__":
    # Comentário: Dispara o motor de comparação de forma direta.
    executar_comparacao_auditoria()
