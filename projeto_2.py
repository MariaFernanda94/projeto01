import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import statsmodels.formula.api as smf

# 1. Configuração da página (Modo Wide para usar toda a largura)
st.set_page_config(
     page_title="Previsão de Renda",
     page_icon="💰",
     layout="wide",
)

st.write('# 💰 Análise e Previsão de Renda')
st.markdown("---")

# 2. Carregamento dos dados com tratamento de erro de caminho
try:
    renda = pd.read_csv('./input/previsao_de_renda.csv')
except:
    try:
        renda = pd.read_csv('previsao_de_renda.csv')
    except Exception as e:
        st.error(f"Erro: O arquivo CSV não foi encontrado. Certifique-se de que ele está na mesma pasta do script. Detalhe: {e}")
        st.stop()

# Limpeza de dados (Importante para o modelo rodar)
renda['tempo_emprego'] = renda['tempo_emprego'].fillna(0)

# 3. Abas para organização
tab1, tab2 = st.tabs(["📊 Gráficos de Análise", "🤖 Simulador de Previsão"])

with tab1:
    st.write("## Análise Exploratória")
    st.info("Os gráficos abaixo mostram a evolução da renda de acordo com diferentes variáveis.")

    # GRÁFICO 1: POSSE DE IMÓVEL
    # Definimos figsize=(15, 6) para ser bem largo e preencher a tela
    fig1, ax1 = plt.subplots(figsize=(15, 6))
    sns.lineplot(x='data_ref', y='renda', hue='posse_de_imovel', data=renda, ax=ax1)
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_title("Evolução da Renda por Posse de Imóvel", fontsize=16)
    st.pyplot(fig1)
    
    st.markdown("---") # Linha divisória

    # GRÁFICO 2: ESCOLARIDADE
    fig2, ax2 = plt.subplots(figsize=(15, 6))
    sns.lineplot(x='data_ref', y='renda', hue='educacao', data=renda, ax=ax2)
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_title("Evolução da Renda por Nível de Escolaridade", fontsize=16)
    # Movemos a legenda para fora para não tampar o gráfico
    sns.move_legend(ax2, "upper left", bbox_to_anchor=(1, 1))
    st.pyplot(fig2)

with tab2:
    st.header("Simulador de Previsão de Renda")
    
    # Criando o modelo para a previsão
    modelo = smf.ols('renda ~ tempo_emprego + idade + C(sexo) + C(educacao)', data=renda).fit()

    # Inputs na barra lateral para o simulador
    st.sidebar.header("Dados do Novo Cliente")
    input_idade = st.sidebar.slider("Idade", 18, 80, 35)
    input_tempo = st.sidebar.slider("Tempo de Emprego (anos)", 0, 40, 5)
    input_sexo = st.sidebar.selectbox("Sexo", ["M", "F"])
    input_educ = st.sidebar.selectbox("Escolaridade", renda['educacao'].unique())

    # Cálculo da Previsão
    novo_cliente = pd.DataFrame({
        'idade': [input_idade],
        'tempo_emprego': [input_tempo],
        'sexo': [input_sexo],
        'educacao': [input_educ]
    })
    previsao = modelo.predict(novo_cliente)[0]

    # Exibição do Resultado em destaque
    st.success(f"### A renda estimada para este perfil é de: **R$ {previsao:.2f}**")
    
    # Gráfico de Avaliação do Modelo (Fica na Tab 2 para não poluir a Tab 1)
    st.write("#### Qualidade do Modelo (R-quadrado)")
    st.metric(label="R²", value=f"{modelo.rsquared:.4f}")
    
    fig3, ax3 = plt.subplots(figsize=(15, 5))
    sns.scatterplot(x=modelo.fittedvalues, y=modelo.resid, alpha=0.3, ax=ax3)
    ax3.axhline(y=0, color='red', linestyle='--')
    ax3.set_title("Gráfico de Resíduos (Erro do Modelo)", fontsize=14)
    st.pyplot(fig3)