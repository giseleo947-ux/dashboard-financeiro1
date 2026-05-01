import streamlit as st
import plotly.graph_objects as go

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

ativo_circulante = st.sidebar.number_input("Ativo Circulante", value=1613095.98)
passivo_circulante = st.sidebar.number_input("Passivo Circulante", value=3030963.15)

passivo_total = st.sidebar.number_input("Passivo Total", value=5537686.45)
passivo_compensatorio = st.sidebar.number_input("Passivo Compensatório", value=2036875.19)

patrimonio_liquido = st.sidebar.number_input("Patrimônio Líquido", value=469848.11)

despesas_pessoal = st.sidebar.number_input("Despesas com Pessoal", value=806341.45)
despesas_adm = st.sidebar.number_input("Despesas Administrativas", value=1635675.01)

estoque = st.sidebar.number_input("Estoque", value=1372033.76)

cmv = st.sidebar.number_input("CMV", value=4456545.33)
custos_totais = st.sidebar.number_input("Custos e Despesas Totais", value=6659568.03)

# =========================
# INDICADORES
# =========================
margem_bruta = (lucro_bruto / receita_liquida) * 100
margem_liquida = (lucro_liquido / receita_liquida) * 100

liquidez_corrente = ativo_circulante / passivo_circulante

endividamento_total = (passivo_total / patrimonio_liquido) * 100
passivo_real = passivo_total - passivo_compensatorio
endividamento_real = (passivo_real / patrimonio_liquido) * 100

pct_pessoal = (despesas_pessoal / despesas_adm) * 100
pct_outros = 100 - pct_pessoal

estoque_sobre_ativo = (estoque / (ativo_circulante + passivo_total)) * 100
cmv_sobre_custos = (cmv / custos_totais) * 100

# =========================
# TÍTULO
# =========================
st.title("📊 Dashboard Financeiro Inteligente")

# =========================
# KPIs
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Margem Bruta", f"{margem_bruta:.2f}%")
c2.metric("Margem Líquida", f"{margem_liquida:.2f}%")
c3.metric("Liquidez Corrente", f"{liquidez_corrente:.2f}")
c4.metric("Endividamento Total", f"{endividamento_total:.2f}%")

st.metric("Endividamento Real (sem compensatório)", f"{endividamento_real:.2f}%")

st.divider()

# =========================
# RESULTADOS
# =========================
st.subheader("📊 Resultado da Empresa")

fig1 = go.Figure()

fig1.add_trace(go.Bar(name="Lucro Bruto", x=["Resultado"], y=[lucro_bruto]))
fig1.add_trace(go.Bar(name="Lucro Líquido", x=["Resultado"], y=[lucro_liquido]))

fig1.update_layout(barmode="group")
st.plotly_chart(fig1, use_container_width=True)

# =========================
# ENDIVIDAMENTO
# =========================
st.subheader("🏦 Estrutura de Endividamento")

fig2 = go.Figure()

fig2.add_trace(go.Bar(name="Total", x=["Endividamento"], y=[endividamento_total]))
fig2.add_trace(go.Bar(name="Real", x=["Endividamento"], y=[endividamento_real]))

fig2.update_layout(barmode="group")
st.plotly_chart(fig2, use_container_width=True)

# =========================
# CUSTOS
# =========================
st.subheader("🏭 Estrutura de Custos")

fig3 = go.Figure()

fig3.add_trace(go.Bar(name="CMV", x=["Custos"], y=[cmv]))
fig3.add_trace(go.Bar(name="Despesas Adm", x=["Custos"], y=[despesas_adm]))

fig3.update_layout(barmode="group")
st.plotly_chart(fig3, use_container_width=True)

# =========================
# ✔ CORREÇÃO AQUI (ESTRUTURA OPERACIONAL EM %)
# =========================
st.subheader("👥 Estrutura Operacional (%)")

fig4 = go.Figure()

fig4.add_trace(go.Bar(
    x=["Pessoal", "Outras Despesas"],
    y=[pct_pessoal, pct_outros],
    text=[f"{pct_pessoal:.2f}%", f"{pct_outros:.2f}%"],
    textposition="auto"
))

fig4.update_layout(
    yaxis_title="% das Despesas Administrativas",
    yaxis=dict(range=[0, 100])
)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# ESTOQUE
# =========================
st.subheader("📦 Estoque")

fig5 = go.Figure()

fig5.add_trace(go.Pie(
    labels=["Estoque", "Demais Ativos"],
    values=[estoque, ativo_circulante + passivo_total]
))

st.plotly_chart(fig5, use_container_width=True)

# =========================
# ALERTAS
# =========================
st.subheader("⚠️ Diagnóstico Automático")

if liquidez_corrente < 1:
    st.error("Risco de liquidez")

if endividamento_total > 300:
    st.error("Endividamento total elevado")

if cmv_sobre_custos > 70:
    st.warning("CMV muito alto nos custos")

if pct_pessoal > 50:
    st.warning("Alta dependência de folha de pagamento")

if margem_liquida < 10:
    st.warning("Margem líquida baixa")