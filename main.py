# main.py
import streamlit as st
import pandas as pd
from datetime import datetime
import functions  # Importar o módulo de funções criado

# Carregar e pré-processar dados
customer_data, message_data = functions.load_data()
customer_data, message_data = functions.preprocess_data(customer_data, message_data)

# Inicializar Filtros do Painel
regions = customer_data['Region'].unique().tolist()
subscription_types = customer_data['SubscriptionType'].unique().tolist()
date_range = [customer_data['DateJoined'].min(), customer_data['DateJoined'].max()]

# Configurar tema do Streamlit para laranja e branco
st.set_page_config(page_title="Painel Inicial", layout="wide")

# Aplicar CSS personalizado para cores do tema
def local_css(css):
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

css = """
<style>
    .css-18e3th9 {
        background-color: white;
    }
    .stButton>button {
        background-color: orange;
        color: white;
    }
    .stSidebar .css-1d391kg {
        background-color: #FF7F00;
    }
</style>
"""

local_css(css)

# Navegação na Barra Lateral
st.sidebar.header("Navegação")
page = st.sidebar.radio("Ir para", ("Informações de clientes", "Pesquisas de satisfação"))

# Filtros na Barra Lateral
st.sidebar.header("Filtros")

selected_regions = st.sidebar.multiselect(
    "Selecionar Regiões", options=regions, default=regions
)

selected_subscription_types = st.sidebar.multiselect(
    "Selecionar Tipos de Assinatura", options=subscription_types, default=subscription_types
)

selected_date_range = st.sidebar.date_input(
    "Selecionar Intervalo de Datas",
    value=(date_range[0].to_pydatetime(), date_range[1].to_pydatetime()),
)

# Converter intervalo de datas selecionado para datetime
start_date = pd.to_datetime(selected_date_range[0])
end_date = pd.to_datetime(selected_date_range[1])

# DataFrames Filtrados
filtered_customer_data = functions.get_filtered_customer_data(
    customer_data, selected_regions, selected_subscription_types, start_date, end_date
)
filtered_message_data = functions.get_filtered_message_data(
    message_data, selected_regions, start_date, end_date
)

# Layout da Página Principal
st.title("Painel Inicial")

if page == "Informações de clientes":
    # Informações de Clientes
    st.header("Informações de Clientes")
    col1, col2 = st.columns(2)
    total_cust = functions.total_customers(filtered_customer_data)
    avg_sat = functions.average_satisfaction(filtered_customer_data)
    col1.metric("Total de Clientes", total_cust)
    col2.metric("Pontuação Média de Satisfação", f"{avg_sat:.2f}" if avg_sat else "N/A")
    
    # Exibir Pesquisas de Satisfação
    st.header("Pesquisas de Satisfação")
    fig1 = functions.satisfaction_by_region_chart(filtered_customer_data)
    if fig1:
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Não há dados disponíveis para 'Pontuação de Satisfação do Cliente por Região'.")
    
    fig2 = functions.feedback_sentiment_chart(filtered_customer_data)
    if fig2:
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Não há dados disponíveis para 'Análise de Sentimento do Feedback'.")

elif page == "Pesquisas de satisfação":
    st.header("Pesquisas de Satisfação")
    # Exibir Gráficos relacionados às pesquisas de satisfação
    fig1 = functions.subscription_type_distribution_chart(filtered_customer_data)
    if fig1:
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Não há dados disponíveis para 'Distribuição do Tipo de Assinatura'.")
    
    fig2 = functions.messages_open_rate_over_time_chart(filtered_message_data)
    if fig2:
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Não há dados disponíveis para 'Taxa de Abertura de Mensagens ao Longo do Tempo'.")
    
    fig3 = functions.conversion_rate_by_message_type_chart(filtered_message_data)
    if fig3:
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Não há dados disponíveis para 'Taxa de Conversão por Tipo de Mensagem'.")
    
    fig4 = functions.preferred_contact_method_chart(filtered_customer_data)
    if fig4:
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Não há dados disponíveis para 'Distribuição do Método de Contato Preferido'.")
else:
    st.write("Selecione uma opção de navegação.")
