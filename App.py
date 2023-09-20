### IMPORTACAO DAS BIBLIOTECAS

import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
import os


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


#pe = pd.read_excel('rpps/pe_rpps_0623.xlsx')
#rj = pd.read_excel('rpps/rj_rpps_0623.xlsx')
#pb = pd.read_excel('rpps/pb_rpps_0623.xlsx')
#al = pd.read_excel('rpps/al_rpps_0623.xlsx')
#am = pd.read_excel('rpps/am_rpps_0623.xlsx')
#ce = pd.read_excel('rpps/ce_rpps_0623.xlsx')
#ma = pd.read_excel('rpps/ma_rpps_0623.xlsx')
#pi = pd.read_excel('rpps/pi_rpps_0623.xlsx')
#se = pd.read_excel('rpps/se_rpps_0523.xlsx')



#se1 = pd.read_excel('rpps/se_rpps_0523.xlsx')
#cotas = pd.read_csv('cotas/cotas.csv')

folha_pagamento = pd.read_excel('folha de pagamento/folha_pagamento_pe.xlsx')



#df = pd.concat([pe, rj, pb, al, am, ce, ma, pi,se])





### LIMPEZA
cad_cnpj_limpo = cad.copy()
cad_cnpj_limpo['CNPJ_FUNDO'] = cad_cnpj_limpo['CNPJ_FUNDO'].str.replace('.','').str.replace('/','').str.replace('-','') 


### PAGINA PRINCIPAL

st.set_page_config(
    layout="wide"
    #page_title="Multipage App"
)


    

# SIDEBAR ===========================
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
    filtro_municipio = filtro_uf[filtro_uf['MUNICÍPIO'] == municipio]



    #page_title="Multipage App"

    
    
#filtro_municipio1 = filtro_municipio.copy()
#filtro_municipio1 = filtro_municipio1[['ID ATIVO', 'NOME DO FUNDO']]

##############################################################################################

lamina = pd.merge(filtro_municipio, cad_cnpj_limpo, how='inner', left_on = 'ID ATIVO', right_on = 'CNPJ_FUNDO')
lamina = lamina.drop_duplicates('CNPJ_FUNDO').reset_index(drop=True)
##
nao_lamina = filtro_municipio[~filtro_municipio['ID ATIVO'].isin(lamina['ID ATIVO'])]
nao_lamina = nao_lamina[['NOME DO FUNDO', 'TIPO DO ATIVO', 'VALOR TOTAL ATUAL', '% DE RECURSOS DO RPPS']].sort_values('TIPO DO ATIVO').reset_index(drop=True)
##
cotas_rpps = pd.merge(filtro_municipio, cotas_cvm, how='inner', left_on = 'ID ATIVO', right_on = 'CNPJ do Fundo' )
cotas_rpps = cotas_rpps[['Data','NOME DO FUNDO', 'Cota']]
#cotas_rpps['Data'] = pd.to_datetime(cotas_rpps['Data'], format = '%Y-%m-%d')
#cotas_rpps['Cota'] = cotas_rpps['Cota'].replace('-', 'NaN')
#cotas_rpps['Cota'] = cotas_rpps['Cota'].astype(float)
cotas_rpps = cotas_rpps.drop_duplicates(['Data','NOME DO FUNDO'])

cotas_pivo = cotas_rpps.pivot(index = 'Data' ,columns = 'NOME DO FUNDO', values = 'Cota')

retorno = (cotas_pivo/cotas_pivo.shift(1)) -1
retorno_anual = round(retorno.mean() * (22*5 + 21) * 100,2).reset_index()
retorno_anual.columns = ['NOME DO FUNDO', 'RETORNO PURO']


##
#relatorio = lamina[['CNPJ_FUNDO','NOME DO FUNDO','RETORNO PURO', 'GESTOR', 'ADMIN', 'TAXA_ADM', 'TAXA_PERFM', '% DE RECURSOS DO RPPS',
#                'VALOR TOTAL ATUAL','TIPO DO ATIVO']]
relatorio = pd.merge(retorno_anual, lamina, how='inner', on = 'NOME DO FUNDO')
relatorio = relatorio[['CNPJ_FUNDO','NOME DO FUNDO','RETORNO PURO', 'GESTOR', 'ADMIN', 'TAXA_ADM', 'TAXA_PERFM', '% DE RECURSOS DO RPPS',
                'VALOR TOTAL ATUAL','TIPO DO ATIVO']]
relatorio.columns = ['CNPJ DO FUNDO','NOME DO FUNDO','RETORNO PURO', 'GESTOR', 'ADMIN', 'TAXA DE ADM', 'TAXA DE PERFM', '% DE RECURSOS DO RPPS',
                'VALOR TOTAL ATUAL','TIPO DO ATIVO']
relatorio['RETORNO NA CARTEIRA'] = (relatorio['RETORNO PURO'] * relatorio['% DE RECURSOS DO RPPS'])/100
relatorio = relatorio[['CNPJ DO FUNDO','NOME DO FUNDO','RETORNO PURO','RETORNO NA CARTEIRA', 'GESTOR', 'ADMIN', 'TAXA DE ADM', 'TAXA DE PERFM', '% DE RECURSOS DO RPPS',
                'VALOR TOTAL ATUAL','TIPO DO ATIVO']]








#Gráfico de tipo de ativo
tipo_ativo = filtro_municipio.groupby('TIPO DO ATIVO')['NOME DO FUNDO'].count()
tipo_ativo = (tipo_ativo/tipo_ativo.sum()*100).round(2)
tipo_ativo = pd.DataFrame(tipo_ativo).reset_index()
tipo_ativo.columns = ['TIPO DO ATIVO', '%']


tipo_ativo = pd.DataFrame(tipo_ativo).reset_index()
#tipo_ativo


graf_pizza = alt.Chart(tipo_ativo).mark_bar(
    
).encode(
    x='%',
    y='TIPO DO ATIVO',
    #color = 'TIPO DO ATIVO',
    color=alt.Color(
        field='TIPO DO ATIVO', 
        type='nominal',
        legend=None
    ),
    tooltip = ['TIPO DO ATIVO', '%'],
    #legend = None    
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
#retorno_total_carteira = relatorio['RETORNO PURO'].dot(relatorio['% DE RECURSOS DO RPPS']/100)
retorno_total_carteira = relatorio['RETORNO NA CARTEIRA'].sum()

###
col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    st.metric(
        label="TOTAL INVESTIDO",
        value= f"R$ {total_investido:,.2f}"
    )




with col2:
    st.metric(
        label="TAXA TOTAL DE ADMINISTRAÇÃO",
        value= f"{taxa_adm:,.2f}%"
    )




with col3:
    st.metric(
        label="RETORNO DA CARTEIRA",
        value= f"{retorno_total_carteira:,.2f}%"
    )

with col4:
    st.metric(
        label="FOLHA DE PAGAMENTO",
        value= f"{f'R${pagamento_2023:,.2f}'}"
    )

st.markdown('---')

# Grafico de linha =================================
retorno1 = retorno.copy()
retorno1['Retorno'] = retorno1.sum(axis=1)
retorno1 = retorno1[ 'Retorno'].reset_index()
retorno1 = pd.DataFrame(retorno1)
retorno1['Retorno'] = retorno1['Retorno'].round(2)
retorno1 = retorno1.groupby(pd.Grouper(key='Data', freq='M')).sum().reset_index()

st.subheader('Taxa de retorno da carteira ao longo de 2023')

graf_retorno = alt.Chart(retorno1).mark_line(
    point = True
).encode(
    alt.Y('Retorno', title='Retorno (%)'),
    alt.X('Data', title='Mês')  
    #color='b:N'
)

st.altair_chart(graf_retorno, use_container_width=True)

#st.line_chart(retorno1)




st.markdown('---')

# TIPO DO ATIVO =====================================================
st.altair_chart(graf_pizza , use_container_width=True)



st.markdown('---')


# Indicadores ==============================
st.subheader('Indicadores para cada fundo na carteira')
st.dataframe(relatorio, use_container_width=True)


st.subheader('Indicadores para tesouro direto e transações bancarias')
st.dataframe(nao_lamina)

#st.subheader('Retornos')














