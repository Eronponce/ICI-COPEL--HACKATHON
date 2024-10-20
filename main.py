import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
# Carregar o dataset
data = pd.read_csv('Merged_Data.csv')

# Converter a coluna 'Comunicado' para formato de data
data['Comunicado'] = pd.to_datetime(data['Comunicado'], format='%Y-%m-%d')

# Criar uma coluna para o mês e ano combinados
data['AnoMes'] = data['Comunicado'].dt.to_period('M')

# Título da aplicação
st.title('Análise de Chamados por Mês')

# Intervalo de datas para seleção
st.header('Selecione o intervalo de datas')
start_date = st.date_input('Data de início', data['Comunicado'].min().date())
end_date = st.date_input('Data de fim', data['Comunicado'].max().date())

# Filtrar os dados pelo intervalo de datas escolhido
filtered_data = data[(data['Comunicado'] >= pd.to_datetime(start_date)) & (data['Comunicado'] <= pd.to_datetime(end_date))]

# Contar o número de chamados por mês no intervalo selecionado
chamados_por_mes = filtered_data.groupby('AnoMes').size().reset_index(name='Chamados')

# Gerar o gráfico de linha
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(chamados_por_mes['AnoMes'].astype(str), chamados_por_mes['Chamados'], marker='o')
ax.set_title(f'Número de Chamados por Mês (de {start_date} a {end_date})')
ax.set_xlabel('Ano-Mês')
ax.set_ylabel('Número de Chamados')
plt.xticks(rotation=90)  # Rotacionar os rótulos do eixo x para melhor leitura
ax.grid(True)

# Exibir o gráfico no Streamlit
st.pyplot(fig)

# Exibir uma mensagem se não houver dados no intervalo selecionado
if filtered_data.empty:
    st.write("Não há dados para o intervalo de datas selecionado.")
# Carregar o dataset
data = pd.read_csv('Merged_Data.csv')
# Converter a coluna 'Comunicado' para formato de data
data['Comunicado'] = pd.to_datetime(data['Comunicado'], format='%Y-%m-%d')

# Título da aplicação
st.title('Heatmap Demográfico: Idade, Satisfação e Recebimento')

# Selecionar o critério para o heatmap (idade, satisfação ou recebimento)
selected_criteria = st.selectbox('Selecione o critério para análise:', ['Idade', 'Satisfação', 'Recebimento'])

# Definir o limiar com base no critério selecionado
if selected_criteria == 'Idade':
    min_val = int(data['Idade'].min())
    max_val = int(data['Idade'].max())
    limiar_min = st.slider('Idade mínima', min_val, max_val, min_val)
    limiar_max = st.slider('Idade máxima', min_val, max_val, max_val)
    # Filtrar os dados pela faixa etária
    filtered_data = data[(data['Idade'] >= limiar_min) & (data['Idade'] <= limiar_max)]
elif selected_criteria == 'Satisfação':
    min_val = float(data['Satisfacao'].min())
    max_val = float(data['Satisfacao'].max())
    limiar_min = st.slider('Satisfação mínima', min_val, max_val, min_val)
    limiar_max = st.slider('Satisfação máxima', min_val, max_val, max_val)
    # Filtrar os dados pela faixa de satisfação
    filtered_data = data[(data['Satisfacao'] >= limiar_min) & (data['Satisfacao'] <= limiar_max)]
else:  # Recebimento
    min_val = float(data['recebimento'].min())
    max_val = float(data['recebimento'].max())
    limiar_min = st.slider('Recebimento mínimo', min_val, max_val, min_val)
    limiar_max = st.slider('Recebimento máximo', min_val, max_val, max_val)
    # Filtrar os dados pela faixa de recebimento
    filtered_data = data[(data['recebimento'] >= limiar_min) & (data['recebimento'] <= limiar_max)]

# Exibir o número de registros filtrados
st.write(f"Total de registros para {selected_criteria}: {filtered_data.shape[0]}")

# Criar o mapa do Paraná (coordenadas aproximadas do Paraná)
parana_map = folium.Map(location=[-24.6, -51.6], zoom_start=7)

# Preparar os dados para o HeatMap (latitude e longitude)
heat_data = [[row['lat'], row['lng']] for index, row in filtered_data.iterrows()]

# Adicionar o HeatMap ao mapa
HeatMap(heat_data, radius=15, blur=30, max_zoom=1).add_to(parana_map)

# Exibir o mapa no Streamlit
st_folium(parana_map, width=700, height=500)

# Exibir uma mensagem se não houver dados no intervalo selecionado
if filtered_data.empty:
    st.write(f"Não há dados para o intervalo selecionado de {selected_criteria}.")



# Converter a coluna 'Comunicado' para formato de data
data['Comunicado'] = pd.to_datetime(data['Comunicado'], format='%Y-%m-%d')

# Título da aplicação
st.title('Análise de Relações: Idade x Satisfação e Idade x Comunicação')

# ---- Limitar a faixa etária ----
st.header('Filtro por Idade')

idade_min = int(data['Idade'].min())
idade_max = int(data['Idade'].max())

# Sliders para selecionar o intervalo de idade (com chave única)
idade_min_sel = st.slider('Idade mínima', idade_min, idade_max, idade_min, key='idade_min')
idade_max_sel = st.slider('Idade máxima', idade_min, idade_max, idade_max, key='idade_max')

# Filtrar os dados pela faixa etária selecionada
data_filtered = data[(data['Idade'] >= idade_min_sel) & (data['Idade'] <= idade_max_sel)]

# ---- Gráfico 1: Relação entre Idade e Satisfação ----
st.header('Idade x Satisfação')

# Calcular a média de satisfação por idade no intervalo selecionado
idade_satisfacao = data_filtered.groupby('Idade')['Satisfacao'].mean().reset_index()

# Gerar o gráfico de linha para Idade x Satisfação
fig1, ax1 = plt.subplots(figsize=(10,6))
ax1.plot(idade_satisfacao['Idade'], idade_satisfacao['Satisfacao'], marker='o', linestyle='-')
ax1.set_title(f'Média de Satisfação por Idade ({idade_min_sel} - {idade_max_sel} anos)')
ax1.set_xlabel('Idade')
ax1.set_ylabel('Média de Satisfação')
ax1.grid(True)

# Exibir o gráfico no Streamlit
st.pyplot(fig1)

# ---- Filtro por Tipo de Comunicação ----
st.header('Filtro por Tipo de Comunicação')
tipos_comunicacao = data['comunicacao'].unique()
tipo_comunicacao_sel = st.multiselect('Selecione o(s) Tipo(s) de Comunicação:', tipos_comunicacao, default=tipos_comunicacao)

# Filtrar os dados pelo(s) tipo(s) de comunicação selecionado(s)
data_filtered_comunicacao = data_filtered[data_filtered['comunicacao'].isin(tipo_comunicacao_sel)]

# ---- Gráfico 2: Relação entre Idade e Tipo de Comunicação ----
st.header('Idade x Tipo de Comunicação')

# Contar o número de ocorrências de cada tipo de comunicação por faixa etária no intervalo selecionado
idade_comunicacao = data_filtered_comunicacao.groupby(['Idade', 'comunicacao']).size().reset_index(name='Quantidade')

# Gerar o gráfico de linha para Idade x Tipo de Comunicação
fig2, ax2 = plt.subplots(figsize=(10,6))

# Plotar um gráfico de linha para cada tipo de comunicação selecionado
for comunicacao in tipo_comunicacao_sel:
    filtro_comunicacao = idade_comunicacao[idade_comunicacao['comunicacao'] == comunicacao]
    ax2.plot(filtro_comunicacao['Idade'], filtro_comunicacao['Quantidade'], marker='o', linestyle='-', label=comunicacao)

ax2.set_title(f'Quantidade de Comunicação por Idade ({idade_min_sel} - {idade_max_sel} anos)')
ax2.set_xlabel('Idade')
ax2.set_ylabel('Quantidade de Comunicações')
ax2.legend(title='Tipo de Comunicação')
ax2.grid(True)

# Exibir o gráfico no Streamlit
st.pyplot(fig2)

# Exibir uma mensagem se não houver dados filtrados
if data_filtered.empty:
    st.write("Não há dados para o intervalo de idade selecionado.")
if data_filtered_comunicacao.empty:
    st.write("Não há dados para o(s) tipo(s) de comunicação selecionado(s).")
