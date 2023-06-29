### IMPORTACAO DAS BIBLIOTECAS

import pandas as pd
import streamlit as st
import numpy as np
import altair as alt


cad = pd.read_csv('cad/cad_fi.csv',sep = ';', encoding='latin-1')
cad = cad[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'ADMIN', 'GESTOR', 'TAXA_ADM', 'TAXA_PERFM']]
### LIMPEZA
cad_cnpj_limpo = cad.copy()
cad_cnpj_limpo['CNPJ_FUNDO'] = cad_cnpj_limpo['CNPJ_FUNDO'].str.replace('.','').str.replace('/','').str.replace('-','') 

pe = pd.read_excel('rpps/pe_rpps_0323.xlsx')
rj = pd.read_excel('rpps/rpps_rj.xlsx')
pb = pd.read_excel('rpps/pb_rpps_0323.xlsx')
al = pd.read_excel('rpps/al_rpps_0323.xlsx')
am = pd.read_excel('rpps/am_rpps_0323.xlsx')
ce = pd.read_excel('rpps/ce_rpps_0323.xlsx')
ma = pd.read_excel('rpps/ma_rpps_0323.xlsx')
pi = pd.read_excel('rpps/pi_rpps_0323.xlsx')
se = pd.read_excel('rpps/se_rpps_0323.xlsx')

#cotas = pd.read_csv('cotas/cotas.csv')

folha_pagamento = pd.read_excel('folha de pagamento/folha_pagamento_pe.xlsx')



df = pd.concat([pe, rj, pb, al, am, ce, ma, pi,se])


with st.sidebar:
    st.title("Capital Ávila")
    st.subheader('Análise de RPPS')


    # FILTROS ==========================
    uf = st.selectbox(
    'Selecione o Estado',
    (df['UF']).unique()    
    )
    filtro_uf = df[df['UF'] == uf]

    municipio = st.selectbox(
    'Selecione o Município',
    (filtro_uf['MUNICÍPIO']).unique()
    )
    filtro_municipio = df[df['MUNICÍPIO'] == municipio]

lamina = pd.merge(filtro_municipio, cad_cnpj_limpo, how='inner', left_on = 'ID ATIVO', right_on = 'CNPJ_FUNDO')
lamina = lamina.drop_duplicates('CNPJ_FUNDO').reset_index(drop=True)


st.title("Indicadores da carteira do RPPS")
st.table(lamina)


