import streamlit as st
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from io import BytesIO

st.set_page_config(layout="wide")

# =========================
# FORMATAÇÃO
# =========================
def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# =========================
# INPUTS
# =========================
st.sidebar.header("📊 Dados da Empresa")

receita_liquida = st.sidebar.number_input("Receita Líquida", value=5619785.97)
lucro_bruto = st.sidebar.number_input("Lucro Bruto", value=2649029.06)
lucro_liquido = st.sidebar.number_input("Lucro Líquido", value=549917.84)

ativo_total = st.sidebar.number_input("Ativo Total", value=5537686.45)
ativo_circulante = st.sidebar.number_input("Ativo Circulante", value=1613095.98)

passivo_total = st.sidebar.number_input("Passivo Total", value=5537686.45)
passivo_circulante = st.sidebar.number_input("Passivo Circulante", value=3030963.15)

patrimonio_liquido = st.sidebar.number_input("Patrimônio Líquido", value=469848.11)

despesas_adm = st.sidebar.number_input("Despesas Administrativas", value=1635675.01)
despesas_pessoal = st.sidebar.number_input("Despesas com Pessoal", value=806341.45)

estoque = st.sidebar.number_input("Estoque", value=1372033.76)

cmv = st.sidebar.number_input("CMV", value=4456545.33)
custos_totais = st.sidebar.number_input("Custos e Despesas Totais", value=6659568.03)

# =========================
# INDICADORES FINANCEIROS (CLÁSSICOS)
# =========================

margem_bruta = (lucro_bruto / receita_liquida) * 100
margem_liquida = (lucro_liquido / receita_liquida) * 100

liquidez_corrente = ativo_circulante / passivo_circulante

endividamento_total = (passivo_total / patrimonio_liquido) * 100
endividamento_real = (passivo_total / patrimonio_liquido) * 100  # ajustável se quiser excluir compensatório

# Operacional
pct_pessoal = (despesas_pessoal / despesas_adm) * 100
estoque_sobre_ativo = (estoque / ativo_total) * 100
cmv_sobre_custos = (cmv / custos_totais) * 100

# =========================
# DASHBOARD
# =========================
st.title("📊 Dashboard Financeiro Inteligente")

st.subheader("📊 INDICADORES FINANCEIROS")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Margem Bruta", f"{margem_bruta:.2f}%")
c2.metric("Margem Líquida", f"{margem_liquida:.2f}%")
c3.metric("Liquidez Corrente", f"{liquidez_corrente:.2f}")
c4.metric("Endividamento Total", f"{endividamento_total:.2f}%")
c5.metric("Endividamento Real", f"{endividamento_real:.2f}%")

st.divider()

# =========================
# ANÁLISE OPERACIONAL
# =========================
st.subheader("📊 ANÁLISE OPERACIONAL")

st.write(f"Despesas Administrativas: {brl(despesas_adm)}")
st.write(f" └─ Despesas com Pessoal: {brl(despesas_pessoal)}")
st.write(f" └─ % das Despesas com Pessoal: {pct_pessoal:.2f}%")

st.divider()

# =========================
# ESTOQUE
# =========================
st.subheader("📦 GESTÃO DE ESTOQUE")

st.write(f"Estoque Total: {brl(estoque)}")
st.write(f"% do Estoque sobre o Ativo: {estoque_sobre_ativo:.2f}%")

st.divider()

# =========================
# CMV
# =========================
st.subheader("🏭 DEPENDÊNCIA DE FORNECEDORES")

st.write(f"CMV: {brl(cmv)}")
st.write(f"Custos e Despesas Totais: {brl(custos_totais)}")
st.write(f"% CMV nos Custos Totais: {cmv_sobre_custos:.2f}%")

# =========================
# ALERTAS
# =========================
st.subheader("⚠️ Diagnóstico Automático")

if margem_liquida < 10:
    st.warning("Margem líquida baixa")

if liquidez_corrente < 1:
    st.error("Risco de liquidez")

if endividamento_total > 300:
    st.error("Endividamento elevado")

if pct_pessoal > 50:
    st.warning("Alta dependência de folha de pagamento")

if cmv_sobre_custos > 70:
    st.warning("CMV muito elevado nos custos totais")

# =========================
# RELATÓRIO PROFISSIONAL DINÂMICO
# =========================
def gerar_relatorio():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("RELATÓRIO FINANCEIRO GERENCIAL", styles["Title"]))
    story.append(Spacer(1, 12))

    # MARGENS
    story.append(Paragraph("1. Rentabilidade", styles["Heading2"]))
    story.append(Paragraph(f"Margem Bruta: {margem_bruta:.2f}%", styles["Normal"]))
    story.append(Paragraph(f"Margem Líquida: {margem_liquida:.2f}%", styles["Normal"]))

    if margem_liquida < 10:
        story.append(Paragraph("A empresa apresenta baixa rentabilidade, indicando pressão sobre custos operacionais.", styles["Normal"]))
    else:
        story.append(Paragraph("A rentabilidade está em nível saudável.", styles["Normal"]))

    story.append(Spacer(1, 10))

    # LIQUIDEZ
    story.append(Paragraph("2. Liquidez", styles["Heading2"]))
    story.append(Paragraph(f"Liquidez Corrente: {liquidez_corrente:.2f}", styles["Normal"]))

    if liquidez_corrente < 1:
        story.append(Paragraph("Existe risco de liquidez de curto prazo.", styles["Normal"]))
    else:
        story.append(Paragraph("A empresa possui capacidade de pagamento adequada.", styles["Normal"]))

    story.append(Spacer(1, 10))

    # ENDIVIDAMENTO
    story.append(Paragraph("3. Endividamento", styles["Heading2"]))
    story.append(Paragraph(f"Endividamento Total: {endividamento_total:.2f}%", styles["Normal"]))
    story.append(Paragraph(f"Endividamento Real: {endividamento_real:.2f}%", styles["Normal"]))

    if endividamento_total > 300:
        story.append(Paragraph("Estrutura de capital altamente dependente de terceiros.", styles["Normal"]))
    else:
        story.append(Paragraph("Endividamento sob controle.", styles["Normal"]))

    story.append(Spacer(1, 10))

    # OPERACIONAL
    story.append(Paragraph("4. Estrutura Operacional", styles["Heading2"]))
    story.append(Paragraph(f"Despesas com Pessoal: {pct_pessoal:.2f}% das despesas administrativas", styles["Normal"]))

    if pct_pessoal > 50:
        story.append(Paragraph("Alta dependência de folha de pagamento.", styles["Normal"]))
    else:
        story.append(Paragraph("Estrutura de pessoal equilibrada.", styles["Normal"]))

    story.append(Spacer(1, 10))

    # CMV
    story.append(Paragraph("5. Fornecedores e Custos", styles["Heading2"]))
    story.append(Paragraph(f"CMV nos custos: {cmv_sobre_custos:.2f}%", styles["Normal"]))

    if cmv_sobre_custos > 70:
        story.append(Paragraph("Alta dependência de fornecedores e custo de mercadorias elevado.", styles["Normal"]))
    else:
        story.append(Paragraph("Dependência de fornecedores sob controle.", styles["Normal"]))

    story.append(Spacer(1, 10))

    # CONCLUSÃO
    story.append(Paragraph("6. Conclusão Geral", styles["Heading2"]))

    conclusao = ""

    if margem_liquida < 10:
        conclusao += "Baixa rentabilidade. "
    if liquidez_corrente < 1:
        conclusao += "Risco de liquidez. "
    if endividamento_total > 300:
        conclusao += "Endividamento elevado. "
    if pct_pessoal > 50:
        conclusao += "Alta folha de pagamento. "

    if conclusao == "":
        conclusao = "Empresa com estrutura financeira equilibrada."

    story.append(Paragraph(conclusao, styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.subheader("📄 Relatório Gerencial")

st.download_button(
    "⬇️ Baixar Relatório PDF",
    data=gerar_relatorio(),
    file_name="relatorio_financeiro.pdf",
    mime="application/pdf"
)