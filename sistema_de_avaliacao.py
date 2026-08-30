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
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
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

def predicao(data_futuro, modelo):
    if modelo == "Dengue":
        resultado_casos = previsao_sarimax(modelos["Dengue"], data_futuro, './dados/dengue_tratado.csv')
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
        resultado_casos = previsao_sarimax(modelos["Zika"], data_futuro, './dados/zika_tratado.csv')
        with row1:
            st.write("Casos")
            st.line_chart(resultado_casos)
        resultado_casos['incidencia'] = (resultado_casos['previsao'] / 102380) * 100000
        with row2:
            st.write("Incidência por 100.000 habitantes")
            st.line_chart(resultado_casos['incidencia'])

    if modelo == "Chikungunya":
        resultado_casos = previsao_sarimax(modelos["Chikungunya"], data_futuro, './dados/chikungunya_tratado.csv')
        with row1:
            st.write("Casos")
            st.line_chart(resultado_casos)
        resultado_casos['incidencia'] = (resultado_casos['previsao'] / 102380) * 100000
        with row2:
            st.write("Incidência por 100.000 habitantes")
            st.line_chart(resultado_casos['incidencia'])

opcao = st.selectbox("Escolha uma Arbovirose", list(modelos.keys()))
modelo_selecionado = modelos[opcao]

st.write(f"Data inicial: 2026-08-23")
data_selecionada = st.date_input("Selecione uma data futura para a previsão", date.today(), min_value=date(2026, 8, 23))

st.button("Fazer previsão", type="primary", on_click=predicao, args=(data_selecionada, opcao))

row1 = st.container()
row2 = st.container()


