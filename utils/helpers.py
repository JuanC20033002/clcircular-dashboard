import pandas as pd
import streamlit as st

@st.cache_data
def load_comercio():
    return pd.read_csv("data/comercio_carne_limpio.csv", parse_dates=["fecha"])

@st.cache_data
def load_clima():
    return pd.read_csv("data/clima_riesgo_clcircular.csv", parse_dates=["fecha"])

@st.cache_data
def load_importaciones_estado():
    return pd.read_csv("data/importaciones_por_estado.csv")

@st.cache_data
def load_exportaciones_estado():
    return pd.read_csv("data/exportaciones_por_estado.csv")

COLORES_RIESGO = {
    "Alto": "#E63946",
    "Medio": "#F4A261",
    "Bajo": "#2A9D8F"
}

ZONAS_COLORES = {
    "Norte": "#E63946",
    "Noroeste": "#E76F51",
    "Occidente": "#F4A261",
    "Centro": "#2A9D8F",
    "Sur-Golfo": "#E9C46A"
}
