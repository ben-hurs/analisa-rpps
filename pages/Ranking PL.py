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

pe = pd.read_excel('rpps/pe_rpps_0623.xlsx')
rj = pd.read_excel('rpps/rj_rpps_0623.xlsx')
pb = pd.read_excel('rpps/pb_rpps_0623.xlsx')
al = pd.read_excel('rpps/al_rpps_0623.xlsx')
am = pd.read_excel('rpps/am_rpps_0623.xlsx')
ce = pd.read_excel('rpps/ce_rpps_0623.xlsx')
ma = pd.read_excel('rpps/ma_rpps_0623.xlsx')
pi = pd.read_excel('rpps/pi_rpps_0623.xlsx')
se = pd.read_excel('rpps/se_rpps_0523.xlsx')
sc = pd.read_excel('rpps/sc_rpps_0623.xlsx')
rs = pd.read_excel('rpps/rs_rpps_0623.xlsx')
pr = pd.read_excel('rpps/pr_rpps_0623.xlsx')
pa = pd.read_excel('rpps/pa_rpps_0623.xlsx')
mt = pd.read_excel('rpps/mt_rpps_0623.xlsx')
ms = pd.read_excel('rpps/ms_rpps_0623.xlsx')
mg = pd.read_excel('rpps/mg_rpps_0623.xlsx')
go = pd.read_excel('rpps/go_rpps_0623.xlsx')


df = pd.concat([pe, rj, pb, al, am, ce, ma, pi,se, sc, rs, pr, pa, mt, ms, mg, go])


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