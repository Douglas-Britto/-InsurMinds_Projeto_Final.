# Importação das bibliotecas padrão do ReportLab para geração de documentos PDF
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Função mestre que constrói o PDF simulando o frontispício de uma apólice de D&O
def criar_pdf_apolice(nome_arquivo, seguradora, cnpj_seg, processo_susep, num_apolice, lmi_valor, franquia_b_valor, def_texto, reclamacao_texto):
    
    # Define a estrutura do documento com margens padrão de engenharia de documentos
    doc = SimpleDocTemplate(nome_arquivo, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = [] # Lista que armazena os elementos sequenciais do PDF
    styles = getSampleStyleSheet()
    
    # Customização de estilos visuais baseados nas apólices corporativas brasileiras
    style_header = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=12, leading=14, alignment=1, spaceAfter=10)
    style_section = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, leading=12, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor('#005A9C'))
    style_body = ParagraphStyle('Body', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=4)
    style_table_header = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.white)
    
    # Bloco 1: Cabeçalho Regulatório (Identificação da apólice perante a SUSEP)
    story.append(Paragraph("<b>FRONTISPÍCIO DE APÓLICE DIGITAL – RISK MANAGEMENT EXECUTIVE (D&O)</b>", style_header))
    story.append(Paragraph(f"<b>SEGURADORA:</b> {seguradora} | <b>CNPJ:</b> {cnpj_seg}", style_body))
    story.append(Paragraph(f"<b>REGISTRO PRODUTO SUSEP:</b> {processo_susep} | <b>Nº APÓLICE:</b> {num_apolice}", style_body))
    story.append(Spacer(1, 8))
    
    # Bloco 2: Dados de Enquadramento do Risco (Segurados Fictícios)
    dados_contrato = [
        [Paragraph('<b>DADOS DO TOMADOR (EMPRESA):</b>', style_body), Paragraph('<b>DADOS DO SEGURADO:</b>', style_body)],
        [Paragraph('ALFA METALOGRAFIA E TECNOLOGIA LTDA<br/>CNPJ: 99.999.999/0001-99<br/>SÃO PAULO - SP', style_body),
         Paragraph('DIRETORES, CONSELHEIROS E<br/>ADMINISTRADORES ELEITOS DA TOMADOR', style_body)],
        [Paragraph('<b>VIGÊNCIA DA APÓLICE:</b>', style_body), Paragraph('<b>ÂMBITO GEOGRÁFICO:</b>', style_body)],
        [Paragraph('13/09/2026 a 13/09/2027', style_body), Paragraph('Território Nacional e Internacional', style_body)]
    ]
    
    # Formatação e estilização da tabela de dados cadastrais
    t_dados = Table(dados_contrato, colWidths=[270, 270])
    t_dados.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#005A9C')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E6F0FA')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#E6F0FA')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_dados)
    
    # Bloco 3: Quadro de Limites e Franquias (Variáveis que o OCR e a IA vão auditar)
    story.append(Paragraph("GARANTIAS CONTRATADAS, LIMITES E RETENÇÕES (FRANQUIAS)", style_section))
    tabela_valores = [
        [Paragraph('<b>Modalidade / Cobertura</b>', style_table_header), Paragraph('<b>Limite Máximo (LMI)</b>', style_table_header), Paragraph('<b>Franquia (Retenção Co. A)</b>', style_table_header), Paragraph('<b>Franquia (Reembolso Co. B)</b>', style_table_header)],
        [Paragraph('Cobertura A - Direta Executivos', style_body), Paragraph(f"R$ {lmi_valor:,.2f}", style_body), Paragraph('ISENTO (R$ 0,00)', style_body), Paragraph('Não Aplicável', style_body)],
        [Paragraph('Cobertura B - Reembolso Companhia', style_body), Paragraph(f"R$ {lmi_valor:,.2f}", style_body), Paragraph('Não Aplicável', style_body), Paragraph(f"R$ {franquia_b_valor:,.2f}", style_body)],
        [Paragraph('Cobertura Adicional - Custos de Defesa', style_body), Paragraph(def_texto, style_body), Paragraph('ISENTO (R$ 0,00)', style_body), Paragraph('ISENTO (R$ 0,00)', style_body)]
    ]
    
    # Aplicação de design azul corporativo na tabela de valores
    t_valores = Table(tabela_valores, colWidths=[150, 110, 140, 140])
    t_valores.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#005A9C')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#005A9C')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_valores)
    
    # Bloco 4: Condições Contratuais (Cláusulas Legais que geram as assimetrias de negócio)
    story.append(Paragraph("OBJETO E CONDIÇÕES CONTRATUAIS GERAIS DO RISCO", style_section))
    story.append(Paragraph("<b>1. RISCOS COBERTOS:</b> Este seguro de Responsabilidade Civil D&O garante a indenização aos Segurados por Prejuízos decorrentes de reclamações de terceiros baseadas estritamente em atos culposos de gestão (negligência, imperícia ou omissão) praticados no exercício de suas funções administrativas capitaneadas no contrato social.", style_body))
    story.append(Paragraph("<b>2. EXCLUSÃO DE DOLO E FRAUDE:</b> Estão formalmente excluídos da cobertura securitária todos os atos tipificados como dolosos, fraudulentos ou que tragam vantagens financeiras ilícitas aos administradores. O adiantamento de custos de defesa será mantido até a sentença judicial Transitada em Julgado. Configurado o dolo final, haverá a reversão imediata com obrigação de devolução dos valores à Seguradora.", style_body))
    
    story.append(Paragraph("PROCEDIMENTO DE RECLAMAÇÃO, GATILHOS E INDENIZAÇÃO", style_section))
    story.append(Paragraph(f"<b>3. GATILHO E PRAZO DE NOTIFICAÇÃO:</b> {reclamacao_texto}", style_body))
    story.append(Paragraph("<b>4. PRAZO DE LIQUIDAÇÃO E INDENIZAÇÃO:</b> Com base nas normas circulares da SUSEP, uma vez concluído o rito de auditoria com o protocolo do último documento obrigatório exigido para comprovação do nexo causal, a Seguradora terá o prazo regulamentar improrrogável de até 30 (trinta) dias cíveis para efetuar o pagamento da indenização ou reembolso financeiro sob pena de juros moratórios.", style_body))
    
    # Compilação e construção física do arquivo PDF
    doc.build(story)
    print(f"Documento gerado com sucesso: {nome_arquivo}")

# Execução do script para consolidação das duas bases concorrentes de D&O
if __name__ == "__main__":
    
    # Geração da Apólice 1: Padrão Chubb (Sem sublimites de defesa, processo direto por e-mail)
    criar_pdf_apolice(
        "apolice_real_chubb.pdf", 
        "CHUBB SEGUROS BRASIL S.A.", "03.502.099/0001-06", "15414.900832/2017-90", "01.82.0049182.00",
        15000000.00, 150000.00, "Livre (Consome LMI Global)", 
        "O Estipulante ou Segurado deverá notificar a seguradora via e-mail oficial (sinistros.linhasfinanceiras@chubb.com) no prazo limite de até 30 dias corridos a partir da ciência da citação cível ou intimação administrativa."
    )
    
    # Geração da Apólice 2: Padrão Tokio Marine (Com sub-limite agressivo e barreira de homologação prévia)
    criar_pdf_apolice(
        "apolice_real_tokio.pdf", 
        "TOKIO MARINE SEGURADORA S.A.", "33.164.021/0001-00", "15414.901489/2017-09", "DO-2026-881923-SP",
        12000000.00, 200000.00, "Sublimitado em R$ 4.000.000,00", 
        "O Tomador ou Segurado deve notificar IMEDIATAMENTE o sinistro. Os honorários e despesas advocatícias de livre escolha dependem obrigatoriamente de PRÉVIA HOMOLOGAÇÃO do orçamento de custos pela banca técnica da Tokio Marine antes do reembolso."
    )
