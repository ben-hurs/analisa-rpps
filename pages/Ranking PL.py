import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
import os

st.title("Ranking de PL")


cotas_cvm_bi1 = pd.read_csv('cotas/cotas_cvm_bi1.csv')
cotas_cvm_bi2 = pd.read_csv('cotas/cotas_cvm_bi2.csv')
cotas_cvm_bi3 = pd.read_csv('cotas/cotas_cvm_bi3.csv')
cotas_cvm = pd.concat([cotas_cvm_bi1, cotas_cvm_bi2,cotas_cvm_bi3]) 
cotas_cvm['CNPJ do Fundo'] = cotas_cvm['CNPJ do Fundo'].str.replace('.','').str.replace('/','').str.replace('-','')
cotas_cvm['CNPJ do Fundo'] = cotas_cvm['CNPJ do Fundo'].astype(object)
cotas_cvm['Data'] = pd.to_datetime(cotas_cvm['Data'], format = '%Y-%m-%d')


cad = pd.read_csv('cad/cad_fi.csv',sep = ';', encoding='latin-1')
cad = cad[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'ADMIN', 'GESTOR', 'TAXA_ADM', 'TAXA_PERFM']]

pasta = r'C:\Users\Ben-Hur\Documents\dashboar streamlit\rpps'

# Lista todos os arquivos na pasta
arquivos_xlsx = [arquivo for arquivo in os.listdir(pasta) if arquivo.endswith('.xlsx')]

# Crie uma lista para armazenar os DataFrames individuais
dataframes = []

# Loop pelos arquivos XLSX e leia-os em DataFrames individuais
for arquivo in arquivos_xlsx:
    caminho_arquivo = os.path.join(pasta, arquivo)
    df = pd.read_excel(caminho_arquivo)
    dataframes.append(df)

# Concatene todos os DataFrames em um único DataFrame
df = pd.concat(dataframes, ignore_index=True)


folha_pagamento = pd.read_excel('folha de pagamento/folha_pagamento_pe.xlsx')







with st.sidebar:
    st.title("Capital Ávila")
    st.subheader('Análise de RPPS')


    # FILTROS ==========================

    uf = st.selectbox(
    'Selecione o Estado',
    (df['UF']).unique()    
    )
    filtro_uf = df[df['UF'] == uf]





    #page_title="Multipage App"



ranking_pl = filtro_uf [['UF' ,'MUNICÍPIO', 'VALOR TOTAL ATUAL']].reset_index(drop=True)
ranking_pl = ranking_pl.groupby('MUNICÍPIO').sum('VALOR TOTAL ATUAL').reset_index()
ranking_pl = ranking_pl.sort_values('VALOR TOTAL ATUAL', ascending=False).reset_index(drop=True)
st.table(ranking_pl)