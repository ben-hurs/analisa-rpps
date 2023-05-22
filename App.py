### IMPORTACAO DAS BIBLIOTECAS

import pandas as pd
import streamlit as st
import numpy as np
import altair as alt


### LEITURA DOS DADOS 

cad = pd.read_csv('cad/cad_fi.csv',sep = ';', encoding='latin-1')
cad = cad[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'ADMIN', 'GESTOR', 'TAXA_ADM', 'TAXA_PERFM']]

pe = pd.read_excel('rpps/pe_rpps_0323.xlsx')
rj = pd.read_excel('rpps/rpps_rj.xlsx')

df = pd.concat([pe,rj])



### LIMPEZA
cad_cnpj_limpo = cad.copy()
cad_cnpj_limpo['CNPJ_FUNDO'] = cad_cnpj_limpo['CNPJ_FUNDO'].str.replace('.','').str.replace('/','').str.replace('-','') 


### PAGINA PRINCIPAL

st.set_page_config(
    layout="wide"
)

st.header(":bar_chart: RELATÓRIO DA CARTEIRA DOS RPPS")

dst1, dst2 = st.columns([1,1])
with dst1:
    uf = st.selectbox(
        'Selecione o Estado',
        (df['UF']).unique()
    )
filtro_uf = df[df['UF'] == uf]

with dst2:
    municipio = st.selectbox(
        'Selecione o Município',
        (filtro_uf['MUNICÍPIO']).unique()
    )

st.markdown('---')

filtro_municipio = df[df['MUNICÍPIO'] == municipio]

##############################################################################################

lamina = pd.merge(filtro_municipio, cad_cnpj_limpo, how='inner', left_on = 'ID ATIVO', right_on = 'CNPJ_FUNDO')
lamina = lamina.drop_duplicates('CNPJ_FUNDO').reset_index(drop=True)

nao_lamina = filtro_municipio[~filtro_municipio['ID ATIVO'].isin(lamina['ID ATIVO'])]
nao_lamina = nao_lamina[['NOME DO FUNDO', 'TIPO DO ATIVO', 'VALOR TOTAL ATUAL', '% DE RECURSOS DO RPPS']].sort_values('TIPO DO ATIVO').reset_index(drop=True)


relatorio = lamina[['NOME DO FUNDO', 'GESTOR', 'ADMIN', 'TAXA_ADM', 'TAXA_PERFM', '% DE RECURSOS DO RPPS',
                'VALOR TOTAL ATUAL','TIPO DO ATIVO']]





#Gráfico de tipo de ativo
tipo_ativo = relatorio.groupby('TIPO DO ATIVO')['NOME DO FUNDO'].count()
tipo_ativo = (tipo_ativo/tipo_ativo.sum()*100).round(2)
tipo_ativo = pd.DataFrame(tipo_ativo).reset_index()
tipo_ativo.columns = ['TIPO DO ATIVO', '%']


tipo_ativo = pd.DataFrame(tipo_ativo).reset_index()
#tipo_ativo


graf_pizza = alt.Chart(tipo_ativo).mark_bar(
    
).encode(
    x='%',
    y='TIPO DO ATIVO',
    color = 'TIPO DO ATIVO',
    #color=alt.Color(
    #    field='TIPO DO ATIVO', 
    #    #type='nominal',
    #    legend=None
    #),
    tooltip = ['TIPO DO ATIVO', '%'],
    #alt.Legend(orient='top'),    
)

rotuloNome = graf_pizza.mark_text(radius=200, size=14).encode(text='TIPO DO ATIVO')
rotuloValor = graf_pizza.mark_text(radius=165, size=14).encode(text='%')



total_investido = filtro_municipio['VALOR TOTAL ATUAL'].sum()
taxa_adm = relatorio['TAXA_ADM'].sum()
taxa_perfm = relatorio['TAXA_PERFM'].sum()
###
col1, col2, col3 = st.columns([0.5,0.5,1])

with col1:
    st.write('**TOTAL INVESTIDO**')
    st.info(f"R$ {total_investido:,.2f}")

    st.write('**TAXA TOTAL DE ADMINISTRAÇÃO**')
    st.info(f'R$ {taxa_adm:,.2f}')

    st.write('**TAXA TOTAL DE PERFORMANCE**')
    st.info(f'{taxa_perfm}%')


with col3:
    st.altair_chart(graf_pizza , use_container_width=True)


st.markdown('---')

st.subheader('Indicadores para cada fundo na carteira')
st.dataframe(relatorio, use_container_width=True)


st.subheader('Indicadores para tesouro direto e transações bancarias')
st.dataframe(nao_lamina)








