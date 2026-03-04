import pandas as pd
import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_comercio():
    return pd.read_csv(os.path.join(BASE_DIR, "comercio_carne_limpio.csv"), parse_dates=["fecha"])

@st.cache_data
def load_clima():
    return pd.read_csv(os.path.join(BASE_DIR, "clima_riesgo_clcircular.csv"), parse_dates=["fecha"])

@st.cache_data
def load_importaciones_estado():
    return pd.read_csv(os.path.join(BASE_DIR, "importaciones_por_estado.csv"), encoding="latin1")

@st.cache_data
def load_exportaciones_estado():
    return pd.read_csv(os.path.join(BASE_DIR, "exportaciones_por_estado.csv"), encoding="latin1")

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
