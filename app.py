import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Configuração da Página (API)
st.set_page_config(page_title="Streamlit Master App", layout="wide")

# 2. Título e Texto (Getting Started)
st.title("🚀 Streamlit I - Módulo 15")
st.markdown("Esta app reproduz funcionalidades essenciais da documentação oficial.")

# 3. Sidebar (Advanced Concepts)
st.sidebar.header("Configurações")
app_mode = st.sidebar.selectbox("Escolha uma seção", ["Home", "Exploração de Dados", "Performance & Estado"])

if app_mode == "Home":
    # 4. Escrita de Texto Simples
    st.header("1. Elementos de Texto e Input")
    
    # 5. Texto de ajuda
    name = st.text_input("Qual é o teu nome?", "Utilizador")
    
    # 6. Botão de clique
    if st.button("Dizer Olá"):
        st.write(f"Olá, {name}!")

    # 7. Slider Numérico
    age = st.slider("Seleciona um valor", 0, 100, 25)

    # 8. Checkbox para mostrar conteúdo condicional
    if st.checkbox("Mostrar segredo"):
        st.success("O Streamlit facilita imenso o desenvolvimento Web!")

    # 9. Radio Buttons
    genre = st.radio("Qual o teu género cinematográfico favorito?", ('Sci-Fi', 'Drama', 'Comédia'))

    # 10. Multiselect
    options = st.multiselect('Cores favoritas', ['Verde', 'Amarelo', 'Vermelho', 'Azul'], ['Amarelo'])

elif app_mode == "Exploração de Dados":
    st.header("2. Visualização de Dados (Data Explorer)")

    # 11. Geração de Dados com NumPy (Caching Simulation)
    @st.cache_data
    def load_data(nrows):
        data = pd.DataFrame(
            np.random.randn(nrows, 3),
            columns=['A', 'B', 'C']
        )
        return data

    data_load_state = st.text('A carregar dados...')
    df = load_data(100)
    data_load_state.text('Dados carregados! (Usando st.cache_data)')

    # 12. Tabela Interativa
    st.subheader("DataFrame Interativo")
    st.dataframe(df.style.highlight_max(axis=0))

    # 13. Tabela Estática
    st.subheader("Tabela Estática")
    st.table(df.head(5))

    # 14. Gráfico de Linhas
    st.subheader("Gráfico de Linhas Nativo")
    st.line_chart(df)

    # 15. Gráfico de Áreas
    st.subheader("Gráfico de Áreas")
    st.area_chart(df)

    # 16. Mapa (Geoprocessamento simples)
    st.subheader("Mapa de Coordenadas Aleatórias")
    map_data = pd.DataFrame(
        np.random.randn(50, 2) / [50, 50] + [38.7, -9.1], # Coordenadas perto de Lisboa
        columns=['lat', 'lon']
    )
    st.map(map_data)

elif app_mode == "Performance & Estado":
    st.header("3. Caching & Session State")

    # 17. Session State (Contador)
    if 'count' not in st.session_state:
        st.session_state.count = 0

    increment = st.button('Incrementar Contador')
    if increment:
        st.session_state.count += 1
    
    st.write(f"Valor do contador no Session State: {st.session_state.count}")

    # 18. Spinner de Carregamento
    with st.spinner('A processar algo pesado...'):
        time.sleep(1)
        st.write("Processamento concluído!")

    # 19. Colunas (Layout)
    col1, col2 = st.columns(2)
    with col1:
        # 20. Expander
        with st.expander("Ver detalhes técnicos"):
            st.code("pip install streamlit", language='bash')
    
    with col2:
        # 21. Métricas
        st.metric(label="Temperatura", value="24 °C", delta="1.2 °C")

# 22. Informação no Rodapé
st.divider()
st.caption("App criada para fins educativos seguindo os guias de Getting Started, Caching e API.")