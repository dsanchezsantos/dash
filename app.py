import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv("dados.csv")

# Converter coluna de data para datetime
df["data"] = pd.to_datetime(df["data"])
df["hora"] = pd.to_datetime(df["hora"], format='%H:%M').dt.hour

# Criar colunas auxiliares
df["dia_da_semana"] = df["data"].dt.day_name()
df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month

# Sidebar - Filtros de ano e mês
ano_selecionado = st.sidebar.selectbox("Selecione o ano", sorted(df["ano"].unique()))
mes_selecionado = st.sidebar.selectbox("Selecione o mês", range(1, 13))

# Filtrar dados com base nos seletores
df_filtrado = df[(df["ano"] == ano_selecionado) & (df["mes"] == mes_selecionado)]

# Gráfico de histogramas
st.title("Análise de Registros")
st.subheader("Distribuição por Dia da Semana")
fig1 = px.histogram(df_filtrado, x="dia_da_semana", title="Quantidade de Registros por Dia da Semana")
st.plotly_chart(fig1)

st.subheader("Distribuição por Hora do Dia")
fig2 = px.histogram(df_filtrado, x="hora", title="Quantidade de Registros por Hora do Dia", nbins=24)
st.plotly_chart(fig2)
