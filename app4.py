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
st.sidebar.header("📊 Dados Financeiros")

receita_liquida = st.sidebar.number_input("Receita Líquida", value=5619785.97)
lucro_bruto = st.sidebar.number_input("Lucro Bruto", value=2649029.06)
lucro_liquido = st.sidebar.number_input("Lucro Líquido", value=549917.84)

ativo_circulante = st.sidebar.number_input("Ativo Circulante", value=1613095.98)
passivo_circulante = st.sidebar.number_input("Passivo Circulante", value=3030963.15)

patrimonio_liquido = st.sidebar.number_input("Patrimônio Líquido", value=469848.11)
passivo_total = st.sidebar.number_input("Passivo Total", value=5537686.45)

estoque = st.sidebar.number_input("Estoque", value=1372033.76)

cmv_dre = st.sidebar.number_input("CMV DRE", value=2970756.91)
cmv_operacional = st.sidebar.number_input("CMV Operacional", value=4456545.33)

# =========================
# INDICADORES
# =========================
margem_bruta = (lucro_bruto / receita_liquida) * 100
margem_liquida = (lucro_liquido / receita_liquida) * 100
liquidez = ativo_circulante / passivo_circulante

endividamento_total = (passivo_total / patrimonio_liquido) * 100
endividamento_real = (passivo_total / patrimonio_liquido) * 100  # ajuste se quiser excluir compensatório

cmv_dre_pct = (cmv_dre / receita_liquida) * 100
cmv_operacional_pct = (cmv_operacional / receita_liquida) * 100

# =========================
# TÍTULO
# =========================
st.title("📊 Dashboard Financeiro Inteligente")

# =========================
# KPIs
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Margem Líquida", f"{margem_liquida:.2f}%")
c2.metric("Liquidez", f"{liquidez:.2f}")
c3.metric("Endividamento Total", f"{endividamento_total:.2f}%")
c4.metric("Endividamento Real", f"{endividamento_real:.2f}%")

st.divider()

# =========================
# CMV
# =========================
st.subheader("📦 CMV (DRE vs Operacional)")

col1, col2 = st.columns(2)

col1.metric("CMV DRE", brl(cmv_dre))
col1.metric("% Receita", f"{cmv_dre_pct:.2f}%")

col2.metric("CMV Operacional", brl(cmv_operacional))
col2.metric("% Receita", f"{cmv_operacional_pct:.2f}%")

fig = go.Figure()

fig.add_trace(go.Bar(name="CMV DRE", x=["CMV"], y=[cmv_dre]))
fig.add_trace(go.Bar(name="CMV Operacional", x=["CMV"], y=[cmv_operacional]))

fig.update_layout(barmode="group", title="Comparação CMV")
st.plotly_chart(fig, use_container_width=True)

# =========================
# DRE VISUAL
# =========================
st.subheader("📊 Demonstração de Resultados")

fig2 = go.Figure()
fig2.add_trace(go.Bar(x=["Lucro Bruto", "Lucro Líquido"], y=[lucro_bruto, lucro_liquido]))
st.plotly_chart(fig2, use_container_width=True)

# =========================
# ALERTAS
# =========================
st.subheader("⚠️ Diagnóstico Automático")

if liquidez < 1:
    st.error("Risco de liquidez baixa")

if endividamento_total > 300:
    st.error("Endividamento elevado")

if cmv_dre_pct > 70:
    st.warning("CMV muito alto impactando margem")

if margem_liquida < 10:
    st.warning("Margem líquida baixa")

# =========================
# RELATÓRIO PDF PROFISSIONAL
# =========================
def gerar_relatorio():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # TÍTULO
    story.append(Paragraph("RELATÓRIO FINANCEIRO GERENCIAL", styles["Title"]))
    story.append(Spacer(1, 12))

    # MARGEM
    story.append(Paragraph("Margem Líquida", styles["Heading2"]))
    story.append(Paragraph(f"Valor: {margem_liquida:.2f}%", styles["Normal"]))

    if margem_liquida < 10:
        story.append(Paragraph("Análise: Margem baixa, pressão sobre rentabilidade.", styles["Normal"]))
    else:
        story.append(Paragraph("Análise: Margem saudável e eficiente.", styles["Normal"]))

    story.append(Spacer(1, 10))

    # LIQUIDEZ
    story.append(Paragraph("Liquidez Corrente", styles["Heading2"]))
    story.append(Paragraph(f"Valor: {liquidez:.2f}", styles["Normal"]))

    if liquidez < 1:
        story.append(Paragraph("Análise: Risco de caixa no curto prazo.", styles["Normal"]))
    else:
        story.append(Paragraph("Análise: Liquidez adequada.", styles["Normal"]))

    story.append(Spacer(1, 10))

    # ENDIVIDAMENTO
    story.append(Paragraph("Endividamento", styles["Heading2"]))
    story.append(Paragraph(f"Total: {endividamento_total:.2f}%", styles["Normal"]))

    if endividamento_total > 300:
        story.append(Paragraph("Análise: Endividamento elevado.", styles["Normal"]))
    else:
        story.append(Paragraph("Análise: Estrutura de capital controlada.", styles["Normal"]))

    story.append(Spacer(1, 10))

    # CMV
    story.append(Paragraph("CMV", styles["Heading2"]))
    story.append(Paragraph(f"CMV DRE: {cmv_dre_pct:.2f}%", styles["Normal"]))
    story.append(Paragraph(f"CMV Operacional: {cmv_operacional_pct:.2f}%", styles["Normal"]))

    if cmv_dre_pct > 70:
        story.append(Paragraph("Análise: CMV elevado pressiona lucro.", styles["Normal"]))
    else:
        story.append(Paragraph("Análise: CMV sob controle.", styles["Normal"]))

    # CONCLUSÃO
    story.append(Spacer(1, 10))
    story.append(Paragraph("Conclusão Geral", styles["Heading2"]))

    conclusao = ""

    if margem_liquida < 10:
        conclusao += "Baixa rentabilidade. "
    if liquidez < 1:
        conclusao += "Risco de liquidez. "
    if endividamento_total > 300:
        conclusao += "Endividamento elevado. "
    if cmv_dre_pct > 70:
        conclusao += "CMV alto impactando resultado. "

    if conclusao == "":
        conclusao = "Empresa com estrutura financeira equilibrada."

    story.append(Paragraph(conclusao, styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.subheader("📄 Relatório Automático")

st.download_button(
    "⬇️ Baixar PDF",
    data=gerar_relatorio(),
    file_name="relatorio_financeiro.pdf",
    mime="application/pdf"
)