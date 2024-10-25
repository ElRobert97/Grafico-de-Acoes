# dark mode
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import timedelta
import math

# Titulo
st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações brasileiras ao longo dos anos
""")

# Carregando os dados de financias
@st.cache_data
def carregar_dados(empresas):
    dados_acao = yf.Tickers(empresas)
    precos_acao = dados_acao.history(period='1d', start='2015-01-01', end='2024-07-01')
    precos_acao = precos_acao["Close"]
    return precos_acao

@st.cache_data
def carregar_tickers_acoes():
    df = pd.read_csv('IBOV (1).csv', sep = ';')
    tickers = list(df['Código'])
    tickers = [item + ".SA" for item in tickers]
    return tickers

dados  = carregar_dados(carregar_tickers_acoes())

# Filtrando as datas
st.sidebar.header("Filtro de Datas")


# Filtro de ações
lista_acoes = st.sidebar.multiselect("Escolha as ações para exibir no gráfico", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns = {acao_unica: "Close"})


# Filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo = st.sidebar.slider("Selecione a Data", 
                              min_value= data_inicial, 
                              max_value= data_final,
                              value=(data_inicial, data_final),
                              step= timedelta(days = 1)
                              )

dados = dados.loc[intervalo[0]:intervalo[1]]

# Grafico 
grafico = st.line_chart(dados)



texto_performance = ''

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes) == 1:
    dados = dados.rename(columns = {"Close": acao_unica})
    

# Calculando a performance
valor = 1000
carteira = [valor for acao in lista_acoes]
total_inicial_carteira = sum(carteira) 


for i, acao in enumerate(lista_acoes):
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)

    carteira[i] *= (1 + performance_ativo) 
    
    # Adicionando as cores
    # padrão :cor[texto]
    if performance_ativo > 0:    
        texto_performance += f'  \n{acao} : :green[{performance_ativo:.2%}]'
        
    elif performance_ativo < 0:
        texto_performance += f'  \n{acao} : :red[{performance_ativo:.2%}]'
    
    elif performance_ativo  == 0:
        texto_performance += f'  \n{acao} : :grey[{performance_ativo:.2%}]'
    

#total_final_carteira = sum(carteira)
total_final_carteira = sum([x for x in carteira if not math.isnan(x)])

print(total_final_carteira)
performance_carteira = total_final_carteira / total_inicial_carteira - 1
#print(f'Valor final da carteira {total_final_carteira}')

texto_performance_carteira = ''

if performance_carteira > 0:    
    texto_performance_carteira = f'  \nA Perfomance da Carteira foi de :green[{performance_carteira:.2%}]'
    
elif performance_carteira < 0:
    texto_performance_carteira = f'  \nA Perfomance da Carteira foi de :red[{performance_carteira:.2%}]'

elif performance_carteira  == 0:
    texto_performance_carteira = f' \nA Perfomance da Carteira foi de :grey[{performance_carteira:.2%}]'






st.write(f"""
## Performance dos ativos
###{texto_performance}
##{texto_performance_carteira}
""")
