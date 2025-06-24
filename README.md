
# Visualização Interativa de Ocorrências - Hackathon COPEL 2024

Este projeto foi desenvolvido durante o Hackathon da COPEL realizado em Curitiba no ano de 2024. Ele tem como objetivo fornecer uma interface visual interativa para análise de dados de ocorrências utilizando mapas, gráficos e filtros temporais.

## 🧠 Objetivo

Permitir que usuários visualizem e analisem comunicações de ocorrências registradas pela COPEL com base em critérios geográficos e temporais, ajudando na identificação de padrões e possíveis áreas críticas.

## 🚀 Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Folium](https://python-visualization.github.io/folium/)
- [streamlit-folium](https://github.com/randyzwitch/streamlit-folium)

## 📂 Estrutura de Arquivos

```
📁 ICI-COPEL--HACKATHON-main/
├── main.py                # Aplicação principal em Streamlit
├── Merged_Data.csv        # Dataset consolidado com localizações e datas
├── customer_data.csv      # Dados adicionais de clientes
├── message_data.csv       # Logs ou mensagens de comunicação
├── .streamlit/config.toml # Configuração da interface Streamlit
├── .vscode/settings.json  # Configuração de ambiente
```

## 🗺️ Funcionalidades

- Visualização de dados temporais (gráficos de linha)
- Mapa de calor das ocorrências no estado do Paraná
- Filtros dinâmicos por data e critérios
- Interface web acessível via navegador

## 🛠️ Como Executar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute a aplicação:

```bash
streamlit run main.py
```

3. Acesse via navegador no endereço:

```
http://localhost:8501
```

## 👥 Equipe

Eron Ponce Pereira
Matheus Vinicius Pires da Silva Garvão
Mariana Yumi
Ana Julia torregiani

## 📄 Licença

Este projeto foi criado exclusivamente para fins de demonstração e não possui licença de uso comercial.
