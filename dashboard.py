import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurar o cliente do BigQuery
client = bigquery.Client()

# Definir consultas SQL para cada tabela
QUERIES = {
    "Receita": "SELECT * FROM `pipeline-etl-ecommerce.etl_ecommerce.tb_receita`",
    "Vendas por Categoria": "SELECT * FROM `pipeline-etl-ecommerce.etl_ecommerce.tb_vendas_categoria`",
    "Vendas por Mês/Ano": "SELECT * FROM `pipeline-etl-ecommerce.etl_ecommerce.tb_vendas_mes_ano`",
    "Vendas por Região": "SELECT * FROM `pipeline-etl-ecommerce.etl_ecommerce.tb_vendas_regiao`",
}

# Função para buscar os dados do BigQuery e armazenar em cache
@st.cache_data
def get_data(query):
    return client.query(query).to_dataframe()

# Configurar a página do Streamlit
st.set_page_config(page_title="Dashboard de E-commerce", layout="wide")
st.title("Dashboard de E-commerce")

# Obter dados das tabelas
df_receita = get_data(QUERIES["Receita"])
df_categoria = get_data(QUERIES["Vendas por Categoria"])
df_mes_ano = get_data(QUERIES["Vendas por Mês/Ano"])
df_regiao = get_data(QUERIES["Vendas por Região"])

# Layout do dashboard
st.sidebar.header("Filtros")

# Filtro por Categoria
categorias = df_categoria["Description"].unique()
categoria_selecionada = st.sidebar.multiselect("Selecione as Categorias", categorias, default=categorias)

# Filtro por Região
regioes = df_regiao["Country"].unique()
regiao_selecionada = st.sidebar.multiselect("Selecione as Regiões", regioes, default=regioes)

# Aplicar filtros
df_categoria_filtrada = df_categoria[df_categoria["Description"].isin(categoria_selecionada)]
df_regiao_filtrada = df_regiao[df_regiao["Country"].isin(regiao_selecionada)]

# Criar layout de colunas para os cards
col1, col2, col3 = st.columns(3)

# Exibir o total de vendas no formato de card
with col1:
    if not df_receita.empty and "TotalSales" in df_receita.columns:
        total_sales = df_receita["TotalSales"].iloc[0]
        st.markdown(f"""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #2a9d8f; color: white;">
                <h2>Total de Vendas</h2>
                <h1>R$ {total_sales:,.2f}</h1>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.write("Dados de receita não encontrados.")

# Exibir o total de categorias no formato de card
with col2:
    total_categorias = df_categoria_filtrada["Description"].nunique()
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #e76f51; color: white;">
            <h2>Total de Categorias</h2>
            <h1>{total_categorias}</h1>
        </div>
    """, unsafe_allow_html=True)

# Exibir o total de regiões no formato de card
with col3:
    total_regioes = df_regiao_filtrada["Country"].nunique()
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f4a261; color: white;">
            <h2>Total de Regiões</h2>
            <h1>{total_regioes}</h1>
        </div>
    """, unsafe_allow_html=True)

# Layout para gráficos
st.markdown("---")
st.markdown("### Análise de Vendas")

# Layout de colunas para os gráficos
col1, col2 = st.columns(2)

# Gráfico de barras para "Vendas por Categoria"
with col1:
    if not df_categoria_filtrada.empty and "Description" in df_categoria_filtrada.columns and "Quantity" in df_categoria_filtrada.columns:
        st.write("### Produtos mais vendidos")
        
        # Ordenar os produtos por quantidade vendida (descendente)
        df_sorted = df_categoria_filtrada.sort_values(by="Quantity", ascending=False).head(10)  # Top 10 produtos
        
        # Criar gráfico de barras
        fig = px.bar(df_sorted, x="Quantity", y="Description", orientation="h",
                     title="Top 10 Produtos mais vendidos", labels={"Quantity": "Quantidade", "Description": "Produto"},
                     color="Quantity", color_continuous_scale="blues")
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Dados insuficientes para gerar gráfico.")

# Gráfico de barras para "Vendas por Região"
with col2:
    if not df_regiao_filtrada.empty and {"Country", "TotalSales"}.issubset(df_regiao_filtrada.columns):
        st.write("### Total de Vendas por Região")

        # Ordenar por TotalSales
        df_sorted = df_regiao_filtrada.sort_values(by="TotalSales", ascending=True)

        # Criar gráfico de barras horizontal
        fig = px.bar(df_sorted, x="TotalSales", y="Country", orientation="h",
                     title="Vendas por País", labels={"TotalSales": "Total de Vendas", "Country": "País"},
                     color="TotalSales", color_continuous_scale="viridis")

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Dados insuficientes para gerar gráfico.")

# Layout para evolução de vendas
st.markdown("---")
st.markdown("### Evolução das Vendas ao Longo do Tempo")

# Gráfico de evolução de vendas por mês/ano
if not df_mes_ano.empty and {"Year", "Month", "TotalSales"}.issubset(df_mes_ano.columns):
    # Criar uma coluna de data combinando Ano e Mês
    df_mes_ano["Date"] = pd.to_datetime(df_mes_ano["Year"].astype(str) + "-" + df_mes_ano["Month"], format="%Y-%B")

    # Ordenar os dados por data
    df_mes_ano = df_mes_ano.sort_values(by="Date")

    # Criar gráfico de linha
    fig = px.line(df_mes_ano, x="Date", y="TotalSales", title="Vendas ao longo do tempo",
                  labels={"TotalSales": "Total de Vendas", "Date": "Data"},
                  markers=True)

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Dados insuficientes para gerar gráfico.")