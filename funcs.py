import pandas as pd
import datetime as dt
import locale as lc
from streamlit_gsheets import GSheetsConnection
import streamlit as st

try:
    lc.setlocale(lc.LC_ALL, 'pt_BR.UTF-8')
except lc.Error:
    # Se o locale 'pt_BR.UTF-8' não estiver disponível, tenta usar o padrão do sistema
    lc.setlocale(lc.LC_ALL, '')

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_tratar_dados(nome_aba):

    df = conn.read(spreadsheet="planilhamika", worksheet=nome_aba)

    # Tratar a coluna 'valor'
    df['valor'] = df['valor'].replace({',': '.'}, regex=True).astype(float)
    
    # Tentar converter a coluna 'data', ignorando erros
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce').dt.date
    
    # Verificar se há datas inválidas
    invalid_dates = df[df['data'].isna()]
    if not invalid_dates.empty:
        print("Datas inválidas encontradas:")
        print(invalid_dates)
    
    return df

def fatura_atual(df):
    # Obter a data atual
    data_atual = dt.datetime.today().date()

    # Definir a data de início (dia 2 do mês atual)
    data_inicial = data_atual.replace(day=2)
    
    # Definir a data final (dia 2 do mês seguinte)
    if data_atual.month == 12:
        data_final = data_atual.replace(year=data_atual.year + 1, month=1, day=2)
    else:
        data_final = data_atual.replace(month=data_atual.month + 1, day=2)

    # Filtrar os dados entre as datas
    df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] < data_final)]

    # Calcular a soma da coluna 'valor'
    soma_valores = df_filtrado['valor'].sum()
    
    return soma_valores

def fatura_anterior(df):

    # Obter a data atual
    data_atual = dt.datetime.today().date()

    # Definir a data de início (dia 2 do mês passado)
    if data_atual.month == 1:
        data_inicial = data_atual.replace(year=data_atual.year - 1, month=12, day=2)
    else:
        data_inicial = data_atual.replace(month=data_atual.month - 1, day=2)
    
    # Definir a data final (dia 2 do mês atual)
    data_final = data_atual.replace(day=2)

    # Filtrar os dados entre as datas
    df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] < data_final)]

    # Calcular a soma da coluna 'valor'
    soma_valores = df_filtrado['valor'].sum()
    
    return soma_valores

def fatura_proxima(df):
    # Obter a data atual
    data_atual = dt.datetime.today().date()

    # Definir a data de início (dia 2 do mês atual)
    data_inicial = data_atual.replace(day=2, month=data_atual.month + 1)
    
    # Definir a data final (dia 2 do mês seguinte)
    if data_atual.month == 12:
        data_final = data_inicial.replace(year=data_atual.year + 1, month=1, day=2)
    else:
        data_final = data_inicial.replace(month=data_inicial.month + 1, day=2)

    # Filtrar os dados entre as datas
    df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] < data_final)]
    
    # Calcular a soma da coluna 'valor'
    soma_valores = df_filtrado['valor'].sum()
    return soma_valores

def valor_formatado(valor):
    return lc.format_string('%.2f', valor, grouping=True)

def soma_valores_por_mes(df):
    # Group the data by month and year
    df['mes'] = pd.to_datetime(df['data']).dt.to_period('M')
    df_grouped = df.groupby('mes')['valor'].sum()

    return df_grouped

def soma_valores_por_classificacao(df):
    # Group the data by month and year
    #df['mes'] = pd.to_datetime(df['data']).dt.to_period('M')
    df_grouped = df.groupby('classificacao')['valor'].sum()

    return df_grouped

print(carregar_tratar_dados("gastomika"))