#---------------------------------------
#  streamlit run sistema_de_avaliacao.py
#---------------------------------------

import streamlit as st
import pandas as pd
from datetime import date
from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from sarimax_process import previsao_sarimax

st.set_page_config(
    page_title="Sistema de Avaliação de Arboviroses",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="./assets/mosquito.png"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }

    div.stButton > button:first-child {
        background-color: #203366;
        color: white;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #909ed0;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

dengue = SARIMAXResults.load('./modelos/sarimax_dengue.pkl')
chikugunya = SARIMAXResults.load('./modelos/sarimax_chik.pkl')
zika = SARIMAXResults.load('./modelos/sarimax_zika.pkl')

modelos = {
    "Dengue": dengue,
    "Chikungunya": chikugunya,
    "Zika": zika,
}

datas_inicios = {
    "Dengue": pd.Timestamp('2026-08-30'),
    "Chikungunya": pd.Timestamp('2026-08-23'),
    "Zika": pd.Timestamp('2024-02-18'),
}

def limitar_data(arbo):
    pass

def predicao(data_futuro, modelo):
    if modelo == "Dengue":
        resultado_casos = previsao_sarimax(modelos["Dengue"], data_futuro, './dados/dengue_tratado.csv', '2026-08-30')
        print(resultado_casos["previsao"])
        with row1:
            st.write("Casos")
            st.line_chart(resultado_casos)
        resultado_casos['incidencia'] = (resultado_casos['previsao'] / 102380) * 100000
        with row2:
            st.write("Incidência por 100.000 habitantes")
            st.line_chart(resultado_casos['incidencia'])
        print(resultado_casos["incidencia"])

    if modelo == "Zika":
        resultado_casos = previsao_sarimax(modelos["Zika"], data_futuro, './dados/zika_tratado.csv','2024-02-18')
        with row1:
            st.write("Casos")
            st.line_chart(resultado_casos)
        resultado_casos['incidencia'] = (resultado_casos['previsao'] / 102380) * 100000
        with row2:
            st.write("Incidência por 100.000 habitantes")
            st.line_chart(resultado_casos['incidencia'])

    if modelo == "Chikungunya":
        resultado_casos = previsao_sarimax(modelos["Chikungunya"], data_futuro, './dados/chikungunya_tratado.csv', '2026-08-23')
        with row1:
            st.write("Casos")
            st.line_chart(resultado_casos)
        resultado_casos['incidencia'] = (resultado_casos['previsao'] / 102380) * 100000
        with row2:
            st.write("Incidência por 100.000 habitantes")
            st.line_chart(resultado_casos['incidencia'])


col1, col2, col3 = st.columns([1.5, 1, 1])
with col2:
    st.image("./assets/mosquito.png", width=200)

opcao = st.selectbox("Escolha uma Arbovirose", list(modelos.keys()))
modelo_selecionado = modelos[opcao]

data_selecionada = st.date_input("Selecione uma data futura para a previsão", date.today(), min_value=datas_inicios[opcao])

st.button("Fazer previsão", type="primary", on_click=predicao, args=(data_selecionada, opcao))

row1 = st.container()
row2 = st.container()


