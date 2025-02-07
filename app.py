import streamlit as st
import pandas as pd
import locale
import plotly.express as px
from supabase import create_client
from datetime import datetime as dt

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZmaHl1dmppcW9zZHJ6Y3FneHBhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMTQ1NjIwNywiZXhwIjoyMDE3MDMyMjA3fQ.EvNKry-AIdhfq-SZW6lrhEM0716nRDd-KLCxqhn6Y1s"
SUPABASE_URL="https://vfhyuvjiqosdrzcqgxpa.supabase.co"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

offset = 0
batch_size = 1000

planos = []

while True:
    planos_query = supabase.table('planos').select('data_saida', 'hora_saida').range(offset, offset + batch_size -1).execute()

    if planos_query.data:

        planos.extend(planos_query.data)

        offset += batch_size
    
    else:
        break

# Carregar dados
df = pd.DataFrame(planos)

# Converter coluna de data para datetime
df["data_saida"] = pd.to_datetime(df["data_saida"])
df["Hora da saída"] = pd.to_datetime(df["hora_saida"], format='%H:%M').dt.hour

# Criar colunas auxiliares
df["Dia da semana"] = df["data_saida"].dt.day_name()
df["ano"] = df["data_saida"].dt.year
df["mes"] = df["data_saida"].dt.month

# Gráfico de histogramas
st.title("Análise de Planos de Navegação")

col1, col2 = st.columns(2)

# Filtros de ano e mês
ano_selecionado = col1.selectbox("Selecione o ano", sorted(df["ano"].unique()))
mes_selecionado = col2.selectbox("Selecione o mês", range(1, 13))

# Filtrar dados com base nos seletores
df_filtrado = df[(df["ano"] == ano_selecionado) & (df["mes"] == mes_selecionado)]

st.subheader("Distribuição por Dia da Semana")
fig1 = px.histogram(df_filtrado, x="Dia da semana", title="Quantidade de Registros por Dia da Semana")
st.plotly_chart(fig1)

st.subheader("Distribuição por Hora do Dia")
fig2 = px.histogram(df_filtrado, x="Hora da saída", title="Quantidade de Registros por Hora do Dia", nbins=24)
st.plotly_chart(fig2)