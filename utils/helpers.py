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

# Paleta CL Circular
CL_VERDE = "#8DC63F"
CL_VERDE_OSCURO = "#2E7D32"
CL_AZUL = "#1B6CA8"
CL_AZUL_MARINO = "#0D1F4E"
CL_CYAN = "#3AACB8"

COLORES_RIESGO = {
    "Alto":  "#E63946",
    "Medio": "#F4A261",
    "Bajo":  "#8DC63F"
}

ZONAS_COLORES = {
    "Norte":     "#1B6CA8",
    "Noroeste":  "#3AACB8",
    "Occidente": "#8DC63F",
    "Centro":    "#2E7D32",
    "Sur-Golfo": "#0D1F4E"
}

