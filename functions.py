# functions.py
import pandas as pd
import plotly.express as px

# Carregar datasets
def load_data():
    customer_data = pd.read_csv('customer_data.csv', parse_dates=['DateJoined', 'LastInteractionDate'])
    message_data = pd.read_csv('message_data.csv', parse_dates=['DateSent'])
    return customer_data, message_data

# Pré-processamento de Dados
def preprocess_data(customer_data, message_data):
    customer_data['Feedback'] = customer_data['Feedback'].astype(str)
    message_data['SubjectLine'] = message_data['SubjectLine'].astype(str)
    
    # Análise de Sentimento (Placeholder para pontuações reais de sentimento)
    def analyze_sentiment(feedback):
        feedback = feedback.lower()
        if "not" in feedback or "needs improvement" in feedback:
            return "Negativo"
        elif "great" in feedback or "excellent" in feedback or "very satisfied" in feedback:
            return "Positivo"
        else:
            return "Neutro"
    
    customer_data['Sentimento'] = customer_data['Feedback'].apply(analyze_sentiment)
    return customer_data, message_data

# DataFrames Filtrados
def get_filtered_customer_data(customer_data, selected_regions, selected_subscription_types, start_date, end_date):
    return customer_data[
        (customer_data['Region'].isin(selected_regions)) &
        (customer_data['SubscriptionType'].isin(selected_subscription_types)) &
        (customer_data['DateJoined'] >= start_date) &
        (customer_data['DateJoined'] <= end_date)
    ]

def get_filtered_message_data(message_data, selected_regions, start_date, end_date):
    return message_data[
        (message_data['Region'].isin(selected_regions)) &
        (message_data['DateSent'] >= start_date) &
        (message_data['DateSent'] <= end_date)
    ]

# Funções de Insights Chave
def total_customers(df):
    return len(df)

def average_satisfaction(df):
    if not df.empty:
        return df['SatisfactionScore'].mean()
    else:
        return None

def total_messages_sent(df):
    return len(df)

# Gráficos
def satisfaction_by_region_chart(df):
    if df.empty:
        return {}
    df_grouped = df.groupby('Region')['SatisfactionScore'].mean().reset_index()
    fig = px.bar(df_grouped,
                 x='Region', y='SatisfactionScore',
                 title='Pontuação de Satisfação do Cliente por Região')
    return fig

def subscription_type_distribution_chart(df):
    if df.empty:
        return {}
    fig = px.pie(df, names='SubscriptionType',
                 title='Distribuição do Tipo de Assinatura')
    return fig

def feedback_sentiment_chart(df):
    if df.empty:
        return {}
    sentiment_counts = df['Sentimento'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentimento', 'Contagem']
    fig = px.bar(sentiment_counts,
                 x='Sentimento', y='Contagem',
                 title='Análise de Sentimento do Feedback',
                 labels={'Sentimento': 'Sentimento', 'Contagem': 'Contagem'})
    return fig

def messages_open_rate_over_time_chart(df):
    if df.empty:
        return {}
    df_sorted = df.sort_values('DateSent')
    fig = px.line(df_sorted, x='DateSent', y='OpenRate',
                  title='Taxa de Abertura de Mensagens ao Longo do Tempo')
    return fig

def conversion_rate_by_message_type_chart(df):
    if df.empty:
        return {}
    fig = px.scatter(df, x='MessageType', y='ConversionRate',
                     size='ConversionRate', color='MessageType',
                     title='Taxa de Conversão por Tipo de Mensagem')
    return fig

def preferred_contact_method_chart(df):
    if df.empty:
        return {}
    contact_counts = df['PreferredContactMethod'].value_counts().reset_index()
    contact_counts.columns = ['Método de Contato', 'Contagem']
    fig = px.bar(contact_counts,
                 x='Método de Contato', y='Contagem',
                 title='Distribuição do Método de Contato Preferido',
                 labels={'Método de Contato': 'Método de Contato', 'Contagem': 'Contagem'})
    return fig
