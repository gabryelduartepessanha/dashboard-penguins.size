import streamlit as st
import pandas as pd

st.title('Dashboard de Pinguins (Palmer Penguins)')

@st.cache_data
def carregar_dados():
    # Lê o ficheiro CSV. Notar o uso de sep=';' adequado a este ficheiro específico
    return pd.read_csv('penguins_size.csv', sep=';')

# Carregamento seguro com tratamento de erro
try:
    df = carregar_dados()
except FileNotFoundError:
    st.error("Ficheiro 'penguins_size.csv' não encontrado. Adicione o ficheiro na mesma pasta para continuar.")
    st.stop()

st.sidebar.title('Filtros')

# Pega os valores únicos da coluna 'species' (espécie) para criar as opções do filtro
# O dropna() garante que não vai pegar valores nulos
lista_de_especies = df['species'].dropna().unique().tolist()

# Widget interativo de seleção múltipla (por predefinição, deixamos todas selecionadas)
especies_selecionadas = st.sidebar.multiselect(
    'Selecione as Espécies', 
    options=lista_de_especies,
    default=lista_de_especies
)

# Filtra o DataFrame com base nas espécies selecionadas
if especies_selecionadas:
    df_filtrado = df[df['species'].isin(especies_selecionadas)]
else:
    # Se nada estiver selecionado, cria um dataframe vazio para limpar o ecrã
    df_filtrado = pd.DataFrame(columns=df.columns) 

# Divisão da parte superior em duas colunas proporcionais
col1, col2 = st.columns([1, 1])

# Cálculos das métricas com base no dataframe FILTRADO
massa_media = df_filtrado['body_mass_g'].mean()
total_pinguins = len(df_filtrado)

# Adição dos indicadores numéricos
with col1:
    # Tratamento caso o filtro resulte em dados vazios ou sem massa registada
    if pd.isna(massa_media):
        st.metric(label='Massa Corporal Média', value="0 g")
    else:
        st.metric(label='Massa Corporal Média', value=f"{massa_media:.1f} g")

with col2:
    st.metric(label='Total de Pinguins', value=total_pinguins)

# Criação da área de navegação por separadores (abas)
aba1, aba2 = st.tabs(['Distribuição por Ilha', 'Tabela de Dados'])

# Conteúdo do primeiro separador (Gráfico de Barras)
with aba1:
    if not df_filtrado.empty:
        # Conta quantos pinguins existem em cada ilha com base no filtro
        dados_agrupados = df_filtrado['island'].value_counts()
        # Gera o gráfico de barras nativo do Streamlit
        st.bar_chart(dados_agrupados)
    else:
        st.info("Selecione pelo menos uma espécie para visualizar o gráfico.")

# Conteúdo do segundo separador (Tabela e Exportação)
with aba2:
    # Exibe o DataFrame filtrado como tabela interativa
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Prepara o ficheiro CSV para ser descarregado (mantendo o separador ponto e vírgula)
    csv_para_download = df_filtrado.to_csv(index=False, sep=';').encode('utf-8')
    
    # Adiciona o botão para descarregar os dados
    st.download_button(
        label="Descarregar Dados Filtrados (CSV)",
        data=csv_para_download,
        file_name='pinguins_filtrados.csv',
        mime='text/csv'
    )