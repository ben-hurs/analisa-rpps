### IMPORTACAO DAS BIBLIOTECAS

import pandas as pd
import streamlit as st
import numpy as np
import altair as alt


### LEITURA DOS DADOS 

cotas_cvm_bi1 = pd.read_csv('cotas/cotas_cvm_bi1.csv')
cotas_cvm_bi2 = pd.read_csv('cotas/cotas_cvm_bi2.csv')
cotas_cvm_bi3 = pd.read_csv('cotas/cotas_cvm_bi3.csv')
cotas_cvm = pd.concat([cotas_cvm_bi1, cotas_cvm_bi2,cotas_cvm_bi3]) 
cotas_cvm['CNPJ do Fundo'] = cotas_cvm['CNPJ do Fundo'].str.replace('.','').str.replace('/','').str.replace('-','')
cotas_cvm['CNPJ do Fundo'] = cotas_cvm['CNPJ do Fundo'].astype(object)
cotas_cvm['Data'] = pd.to_datetime(cotas_cvm['Data'], format = '%Y-%m-%d')



cad = pd.read_csv('cad/cad_fi.csv',sep = ';', encoding='latin-1')
cad = cad[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'ADMIN', 'GESTOR', 'TAXA_ADM', 'TAXA_PERFM']]

pe = pd.read_excel('rpps/pe_rpps_0323.xlsx')
rj = pd.read_excel('rpps/rpps_rj.xlsx')

folha_pagamento = pd.read_excel('folha de pagamento/folha_pagamento_pe.xlsx')



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
##
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
taxa_adm = relatorio['TAXA DE ADM'].sum()
taxa_perfm = relatorio['TAXA DE PERFM'].sum()

filtro_pagamento_2022 = folha_pagamento[(folha_pagamento['dt_exercicio']== 2022) & (folha_pagamento['no_ente'] == municipio)]
pagamento_2022 = filtro_pagamento_2022['vl_pagamentos'].sum()

filtro_pagamento_2023 = folha_pagamento[(folha_pagamento['dt_exercicio']== 2023) & (folha_pagamento['no_ente'] == municipio)]
pagamento_2023 = filtro_pagamento_2023['vl_pagamentos'].sum()
ultima_att = filtro_pagamento_2023['dt_envio'].max()
retorno_total_carteira = relatorio['RETORNO PURO'].dot(relatorio['% DE RECURSOS DO RPPS'])

###
col1, col2, col3 = st.columns([0.5,0.5,1])

with col1:
    st.write('**TOTAL INVESTIDO**')
    st.info(f"R$ {total_investido:,.2f}")

    st.write('**TAXA TOTAL DE ADMINISTRAÇÃO**')
    st.info(f'{taxa_adm:,.2f}%')

    st.write('**TAXA TOTAL DE PERFORMANCE**')
    st.info(f'{taxa_perfm}%')


with col2:
    st.write('**FOLHA DE PAGAMENTO 2022**')
    st.info(f'R${pagamento_2022:,.2f}')

    st.write('**FOLHA DE PAGAMENTO 2023**')
    st.info(f'R${pagamento_2023:,.2f}')
    #st.write(f'Data de última atualização: {ultima_att}')

    st.write('**RETORNO DA CARTEIRA**')
    st.info(f'{retorno_total_carteira:,.2f} %')


with col3:
    st.altair_chart(graf_pizza , use_container_width=True)


st.markdown('---')

st.subheader('Indicadores para cada fundo na carteira')
st.dataframe(relatorio, use_container_width=True)


st.subheader('Indicadores para tesouro direto e transações bancarias')
st.dataframe(nao_lamina)










