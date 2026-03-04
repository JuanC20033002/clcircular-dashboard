import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import load_comercio

st.set_page_config(page_title="Serie de Tiempo | CL Circular", layout="wide")

st.title("📈 Serie de Tiempo — Comercio Bilateral de Carne")
st.markdown("Histórico mensual y pronóstico ARIMA del valor de importaciones y exportaciones México–EE.UU.")
st.divider()

df = load_comercio()

# Filtros
col1, col2 = st.columns(2)
with col1:
    flujo = st.radio("Flujo:", ["Importaciones", "Exportaciones"], horizontal=True)
with col2:
    horizonte = st.slider("Meses a pronosticar:", min_value=6, max_value=36, value=12, step=6)

# Filtrar serie
serie = df[df['flujo'] == flujo].set_index('fecha')['valor_comercio'].asfreq('MS')

# Modelo ARIMA
order = (1, 1, 2) if flujo == "Importaciones" else (3, 1, 3)
model = ARIMA(serie, order=order).fit()
forecast = model.get_forecast(steps=horizonte)
pred = forecast.predicted_mean
ci = forecast.conf_int()

# Gráfica
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=serie.index, y=serie.values / 1e6,
    name="Histórico", line=dict(color="#4C9BE8", width=2)
))
fig.add_trace(go.Scatter(
    x=pred.index, y=pred.values / 1e6,
    name="Pronóstico", line=dict(color="#E63946", width=2.5, dash="dash")
))
fig.add_trace(go.Scatter(
    x=list(pred.index) + list(pred.index[::-1]),
    y=list(ci.iloc[:, 1] / 1e6) + list(ci.iloc[:, 0] / 1e6)[::-1],
    fill="toself", fillcolor="rgba(230,57,70,0.15)",
    line=dict(color="rgba(0,0,0,0)"),
    name="IC 95%", hoverinfo="skip"
))

fig.update_layout(
    height=500,
    xaxis_title="Fecha",
    yaxis_title="USD Millones",
    legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

# Métricas del modelo
st.divider()
st.markdown("### 📊 Métricas del Modelo")
m1, m2, m3 = st.columns(3)
order_label = f"ARIMA{order}"
m1.metric("Modelo", order_label)
m2.metric("MAPE", "11.32%" if flujo == "Importaciones" else "9.94%")
m3.metric("Horizonte", f"{horizonte} meses")
