import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Função para carregar e preparar o dataset
@st.cache_data
def carregar_dados():
    data = pd.read_csv('Merged_Data.csv')
    data['Comunicado'] = pd.to_datetime(data['Comunicado'], format='%Y-%m-%d')
    data['AnoMes'] = data['Comunicado'].dt.to_period('M')
    return data

# Função para gerar gráficos de linha
def gerar_grafico_linha(x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(x, y, marker='o')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=90)
    ax.grid(True)
    st.pyplot(fig)

# Função para gerar heatmap
def gerar_heatmap(data, criterio):
    parana_map = folium.Map(location=[-24.6, -51.6], zoom_start=7)
    heat_data = [[row['lat'], row['lng']] for index, row in data.iterrows()]
    HeatMap(heat_data, radius=15, blur=30, max_zoom=1).add_to(parana_map)
    st_folium(parana_map, width=700, height=500)

# Carregar dados
data = carregar_dados()

# Sidebar para selecionar a análise
st.sidebar.title("Selecione a Análise")
opcao = st.sidebar.selectbox("Escolha uma opção", ["Análise de Chamados", "Heatmap Demográfico", "Relação Idade x Satisfação e Comunicação"])

# Análise de Chamados por Mês
if opcao == "Análise de Chamados":
    st.title('Análise de Chamados por Mês')
    
    st.header('Selecione o intervalo de datas')
    start_date = st.date_input('Data de início', data['Comunicado'].min().date())
    end_date = st.date_input('Data de fim', data['Comunicado'].max().date())

    # Filtrar os dados
    filtered_data = data[(data['Comunicado'] >= pd.to_datetime(start_date)) & (data['Comunicado'] <= pd.to_datetime(end_date))]

    # Contagem de chamados
    chamados_por_mes = filtered_data.groupby('AnoMes').size().reset_index(name='Chamados')
    
    # Exibir gráfico
    gerar_grafico_linha(chamados_por_mes['AnoMes'].astype(str), chamados_por_mes['Chamados'],
                        f'Número de Chamados por Mês (de {start_date} a {end_date})', 'Ano-Mês', 'Número de Chamados')

    if filtered_data.empty:
        st.write("Não há dados para o intervalo de datas selecionado.")
# Heatmap Demográfico
elif opcao == "Heatmap Demográfico":
    st.title('Heatmap Demográfico: Idade, Satisfação, Recebimento e Quedas')

    # Perguntar se o usuário deseja exibir um gráfico com pontos interativos ou um heatmap
    visualizacao = st.radio('Escolha a visualização:', ['Pontos Interativos', 'Heatmap'])

    # Função para gerar heatmap de densidade
    def gerar_heatmap_densidade(data):
        parana_map = folium.Map(location=[-24.6, -51.6], zoom_start=7)
        heat_data = [[row['lat'], row['lng']] for index, row in data.iterrows()]
        HeatMap(heat_data, radius=15, blur=30, max_zoom=1).add_to(parana_map)
        st_folium(parana_map, width=700, height=500)

    # Função para gerar mapa com pontos interativos, incluindo as quedas
    def gerar_mapa_com_pontos(data):
        parana_map = folium.Map(location=[-24.6, -51.6], zoom_start=7)
        for _, row in data.iterrows():
            popup_text = (
                f"Idade: {row['Idade']}<br>"
                f"Satisfação: {row.get('Satisfacao', 'N/A')}<br>"
                f"Recebimento: {row.get('recebimento', 'N/A')}<br>"
                f"Quedas: {row.get('Queda', 0)}"  # Mostrando a quantidade de quedas
            )
            folium.Marker(
                location=[row['lat'], row['lng']],
                popup=popup_text,
                tooltip="Clique para mais informações"
            ).add_to(parana_map)
        st_folium(parana_map, width=700, height=500)

    # Caso o usuário escolha "Pontos Interativos"
    if visualizacao == 'Pontos Interativos':
        st.write("Exibindo gráfico com pontos interativos.")
        gerar_mapa_com_pontos(data)

    # Caso o usuário escolha "Heatmap"
    else:
        # Seleção de critério de análise
        selected_criteria = st.selectbox('Selecione o critério para análise:', ['Idade', 'Satisfação', 'Recebimento', 'Quedas'])

        # Caso o critério seja "Quedas", filtrar apenas onde o valor de queda seja 1
        if selected_criteria == 'Quedas':
            # Certificar que a coluna "Queda" exista ou corrigir o nome da coluna
            if 'Queda' in data.columns:
                filtered_data = data[data['Queda'] == 1]  # Considerando apenas registros com valor 1 em "Queda"
            else:
                st.error("A coluna 'Queda' não existe no dataset. Verifique o nome correto da coluna.")
                filtered_data = pd.DataFrame()  # Dados vazios para evitar erro

            total_quedas = filtered_data.shape[0]
            st.write(f"Total de registros de quedas (valor 1): {total_quedas}")
            
            if not filtered_data.empty:
                gerar_heatmap_densidade(filtered_data)
            else:
                st.write("Não há dados para exibir no mapa de Quedas.")
        else:
            # Aplicar os filtros para Idade, Satisfação ou Recebimento
            if selected_criteria == 'Idade':
                min_val = int(data['Idade'].min())
                max_val = int(data['Idade'].max())
                limiar_min = st.slider('Idade mínima', min_val, max_val, min_val)
                limiar_max = st.slider('Idade máxima', min_val, max_val, max_val)
                filtered_data = data[(data['Idade'] >= limiar_min) & (data['Idade'] <= limiar_max)]
                st.write(f"Total de registros para Idade: {filtered_data.shape[0]}")
            elif selected_criteria == 'Satisfação':
                min_val = float(data['Satisfacao'].min())
                max_val = float(data['Satisfacao'].max())
                limiar_min = st.slider('Satisfação mínima', min_val, max_val, min_val)
                limiar_max = st.slider('Satisfação máxima', min_val, max_val, max_val)
                filtered_data = data[(data['Satisfacao'] >= limiar_min) & (data['Satisfacao'] <= limiar_max)]
                st.write(f"Total de registros para Satisfação: {filtered_data.shape[0]}")
            else:  # Recebimento
                min_val = float(data['recebimento'].min())
                max_val = float(data['recebimento'].max())
                limiar_min = st.slider('Recebimento mínimo', min_val, max_val, min_val)
                limiar_max = st.slider('Recebimento máximo', min_val, max_val, max_val)
                filtered_data = data[(data['recebimento'] >= limiar_min) & (data['recebimento'] <= limiar_max)]
                st.write(f"Total de registros para Recebimento: {filtered_data.shape[0]}")

            # Gerar o heatmap
            if not filtered_data.empty:
                gerar_heatmap_densidade(filtered_data)
            else:
                st.write(f"Não há dados para o intervalo selecionado de {selected_criteria}.")

# Relação Idade x Satisfação e Comunicação
elif opcao == "Relação Idade x Satisfação e Comunicação":
    st.title('Análise de Relações: Idade x Satisfação e Idade x Comunicação')

    # Filtro por Idade
    st.header('Filtro por Idade')
    idade_min = int(data['Idade'].min())
    idade_max = int(data['Idade'].max())
    idade_min_sel = st.slider('Idade mínima', idade_min, idade_max, idade_min, key='idade_min')
    idade_max_sel = st.slider('Idade máxima', idade_min, idade_max, idade_max, key='idade_max')

    data_filtered = data[(data['Idade'] >= idade_min_sel) & (data['Idade'] <= idade_max_sel)]

    # Gráfico 1: Idade x Satisfação
    st.header('Idade x Satisfação')
    idade_satisfacao = data_filtered.groupby('Idade')['Satisfacao'].mean().reset_index()
    gerar_grafico_linha(idade_satisfacao['Idade'], idade_satisfacao['Satisfacao'],
                        f'Média de Satisfação por Idade ({idade_min_sel} - {idade_max_sel} anos)', 'Idade', 'Média de Satisfação')

    # Filtro por Tipo de Comunicação
    st.header('Filtro por Tipo de Comunicação')
    tipos_comunicacao = data['comunicacao'].unique()
    tipo_comunicacao_sel = st.multiselect('Selecione o(s) Tipo(s) de Comunicação:', tipos_comunicacao, default=tipos_comunicacao)
    
    data_filtered_comunicacao = data_filtered[data_filtered['comunicacao'].isin(tipo_comunicacao_sel)]

    # Gráfico 2: Idade x Tipo de Comunicação
    st.header('Idade x Tipo de Comunicação')
    idade_comunicacao = data_filtered_comunicacao.groupby(['Idade', 'comunicacao']).size().reset_index(name='Quantidade')

    fig2, ax2 = plt.subplots(figsize=(10,6))
    for comunicacao in tipo_comunicacao_sel:
        filtro_comunicacao = idade_comunicacao[idade_comunicacao['comunicacao'] == comunicacao]
        ax2.plot(filtro_comunicacao['Idade'], filtro_comunicacao['Quantidade'], marker='o', linestyle='-', label=comunicacao)
    
    ax2.set_title(f'Quantidade de Comunicação por Idade ({idade_min_sel} - {idade_max_sel} anos)')
    ax2.set_xlabel('Idade')
    ax2.set_ylabel('Quantidade de Comunicações')
    ax2.legend(title='Tipo de Comunicação')
    ax2.grid(True)
    st.pyplot(fig2)

    if data_filtered.empty:
        st.write("Não há dados para o intervalo de idade selecionado.")
    if data_filtered_comunicacao.empty:
        st.write("Não há dados para o(s) tipo(s) de comunicação selecionado(s).")
