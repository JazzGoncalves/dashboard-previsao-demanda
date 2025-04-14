
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Previsão e Alertas", layout="wide")

# Título e introdução
st.title("📊 Dashboard de Previsão de Demanda e Alertas de Reposição")
st.markdown("Este painel interativo apresenta a performance do modelo preditivo de demanda, alertas operacionais e ferramentas de análise para o time de estoque e reposição.")

# Dados
monitoramento_path = "data/monitoramento_jan2024.csv"
alerta_path = "data/previsao_alerta_2024-01-02.csv"

df_monitoramento = pd.read_csv(monitoramento_path)
df_alertas = pd.read_csv(alerta_path)

# Filtros
st.sidebar.header("🔍 Filtros")
produtos = st.sidebar.multiselect("Filtrar por Produto", sorted(df_monitoramento["produto"].unique()))
categorias = st.sidebar.multiselect("Filtrar por Categoria", sorted(df_monitoramento["categoria"].unique()))
datas = st.sidebar.multiselect("Filtrar por Data de Previsão", sorted(df_monitoramento["data_previsao"].unique()))

df_monitoramento_filtrado = df_monitoramento.copy()
if produtos:
    df_monitoramento_filtrado = df_monitoramento_filtrado[df_monitoramento_filtrado["produto"].isin(produtos)]
if categorias:
    df_monitoramento_filtrado = df_monitoramento_filtrado[df_monitoramento_filtrado["categoria"].isin(categorias)]
if datas:
    df_monitoramento_filtrado = df_monitoramento_filtrado[df_monitoramento_filtrado["data_previsao"].isin(datas)]

# Seção: Desempenho preditivo
st.subheader("📈 Erro Absoluto Médio por Dia")
erro_diario = df_monitoramento_filtrado.groupby("data_previsao")["erro_absoluto"].mean()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(erro_diario.index, erro_diario.values, marker="o", color="teal")
ax.set_title("Erro médio absoluto por dia - Janeiro 2024")
ax.set_xlabel("Data")
ax.set_ylabel("Erro Absoluto")
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)

# Seção: Ranking de produtos com maior erro
st.subheader("🔝 Top Produtos com Maior Erro Médio de Previsão")
top_erro_produto = df_monitoramento_filtrado.groupby("produto")["erro_absoluto"].mean().sort_values(ascending=False).head(10)
st.dataframe(top_erro_produto.reset_index().rename(columns={"erro_absoluto": "Erro Médio"}), use_container_width=True)

# Seção: Alertas de reposição
st.subheader("🚨 Produtos com Alerta de Reposição (2024-01-02)")
df_alertas_filtrados = df_alertas[df_alertas["alerta_reposicao"] == True]
if produtos:
    df_alertas_filtrados = df_alertas_filtrados[df_alertas_filtrados["produto"].isin(produtos)]
if categorias:
    df_alertas_filtrados = df_alertas_filtrados[df_alertas_filtrados["categoria"].isin(categorias)]

st.dataframe(df_alertas_filtrados[["produto", "categoria", "previsao", "limite_reposicao"]].reset_index(drop=True), use_container_width=True)
