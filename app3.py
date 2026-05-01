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
# DADOS (EDITÁVEIS)
# =========================
st.sidebar.header("📊 Parâmetros Financeiros")

receita_liquida = st.sidebar.number_input("Receita Líquida", value=5619785.97)
lucro_liquido = st.sidebar.number_input("Lucro Líquido", value=549917.84)
lucro_bruto = st.sidebar.number_input("Lucro Bruto", value=2649029.06)

ativo_circulante = st.sidebar.number_input("Ativo Circulante", value=1613095.98)
passivo_circulante = st.sidebar.number_input("Passivo Circulante", value=3030963.15)

patrimonio_liquido = st.sidebar.number_input("Patrimônio Líquido", value=469848.11)
passivo_total = st.sidebar.number_input("Passivo Total", value=5537686.45)

estoque = st.sidebar.number_input("Estoque", value=1372033.76)

cmv = st.sidebar.number_input("CMV", value=4456545.33)

# =========================
# INDICADORES
# =========================
margem_liquida = (lucro_liquido / receita_liquida) * 100
margem_bruta = (lucro_bruto / receita_liquida) * 100
liquidez = ativo_circulante / passivo_circulante
endividamento = (passivo_total / patrimonio_liquido) * 100
estoque_ratio = (estoque / passivo_total) * 100

# =========================
# TABS (ESTILO POWER BI)
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executivo",
    "📈 DRE",
    "🏦 Balanço",
    "📦 Operações",
    "⚠️ Risco"
])

# =========================
# TAB 1 - EXECUTIVO
# =========================
with tab1:
    st.title("Dashboard Executivo")

    c1, c2, c3 = st.columns(3)
    c1.metric("Margem Líquida", f"{margem_liquida:.2f}%")
    c2.metric("Liquidez", f"{liquidez:.2f}")
    c3.metric("Endividamento", f"{endividamento:.2f}%")

    st.info("Visão estratégica para diretoria e tomada de decisão.")

# =========================
# TAB 2 - DRE
# =========================
with tab2:
    st.title("Demonstração de Resultados")

    st.write(f"Receita Líquida: {brl(receita_liquida)}")
    st.write(f"Lucro Bruto: {brl(lucro_bruto)}")
    st.write(f"Lucro Líquido: {brl(lucro_liquido)}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Bruto", "Líquido"],
        y=[lucro_bruto, lucro_liquido]
    ))
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 3 - BALANÇO
# =========================
with tab3:
    st.title("Balanço Patrimonial")

    st.write(f"Ativo Circulante: {brl(ativo_circulante)}")
    st.write(f"Passivo Circulante: {brl(passivo_circulante)}")
    st.write(f"Patrimônio Líquido: {brl(patrimonio_liquido)}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Ativo", "Passivo"],
        y=[ativo_circulante, passivo_circulante]
    ))
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 4 - OPERAÇÕES
# =========================
with tab4:
    st.title("Eficiência Operacional")

    st.write(f"Estoque: {brl(estoque)}")
    st.write(f"CMV: {brl(cmv)}")
    st.write(f"% Estoque: {estoque_ratio:.2f}%")

# =========================
# TAB 5 - RISCO
# =========================
with tab5:
    st.title("Análise de Risco")

    if liquidez < 1:
        st.error("Baixa liquidez → risco financeiro")

    if endividamento > 300:
        st.error("Alto endividamento")

    if estoque_ratio > 20:
        st.warning("Estoque elevado")

# =========================
# PDF EXECUTIVO
# =========================
def gerar_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("RELATÓRIO EXECUTIVO FINANCEIRO", styles["Title"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Resumo Executivo", styles["Heading2"]))
    story.append(Paragraph(f"Margem Líquida: {margem_liquida:.2f}%", styles["Normal"]))
    story.append(Paragraph(f"Liquidez: {liquidez:.2f}", styles["Normal"]))
    story.append(Paragraph(f"Endividamento: {endividamento:.2f}%", styles["Normal"]))

    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "A empresa apresenta estrutura financeira sob pressão, com dependência relevante de capital de terceiros e necessidade de otimização operacional.",
        styles["Normal"]
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.subheader("📄 Relatório Executivo")

st.download_button(
    "⬇️ Baixar PDF Executivo",
    data=gerar_pdf(),
    file_name="relatorio_executivo_bi.pdf",
    mime="application/pdf"
)
    
