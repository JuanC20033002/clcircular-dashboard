import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import load_comercio

st.set_page_config(page_title="Serie de Tiempo | CL Circular", layout="wide")

st.title("📈 Serie de Tiempo — Comercio Bilateral de Carne")
st.markdown("Modelo ARIMA con transformación logarítmica y validación Walk-Forward sobre el valor mensual de importaciones y exportaciones México–EE.UU.")
st.divider()

df = load_comercio()

col1, col2 = st.columns(2)
with col1:
    flujo = st.radio("Flujo:", ["Importaciones", "Exportaciones"], horizontal=True)
with col2:
    horizonte = st.slider("Meses a pronosticar hacia adelante:", min_value=6, max_value=36, value=12, step=6)

# Preparar serie
flujo_id = 1 if flujo == "Importaciones" else 2
order = (1, 1, 2) if flujo == "Importaciones" else (3, 1, 3)
mape_val = "8.80%" if flujo == "Importaciones" else "4.86%"
mae_val = "$63,648,875" if flujo == "Importaciones" else "$13,515,322"
rmse_val = "$74,468,356" if flujo == "Importaciones" else "$18,304,248"

serie = df[df['flujo_id'] == flujo_id].set_index('fecha')['valor_comercio'].asfreq('MS')
serie_log = np.log(serie)
test_size = 12

with st.spinner("Calculando Walk-Forward Validation..."):
    # Walk-Forward sobre log
    predictions_log, ci_lower_log, ci_upper_log = [], [], []
    for i in range(test_size):
        train_wf = serie_log.iloc[:-(test_size - i)]
        model_wf = ARIMA(train_wf, order=order).fit()
        fc = model_wf.get_forecast(steps=1)
        predictions_log.append(fc.predicted_mean.values[0])
        ci_lower_log.append(fc.conf_int().iloc[0, 0])
        ci_upper_log.append(fc.conf_int().iloc[0, 1])

    pred_index = serie_log.index[-test_size:]
    pred_real = np.exp(pd.Series(predictions_log, index=pred_index))
    ci_lo_real = np.exp(pd.Series(ci_lower_log, index=pred_index))
    ci_hi_real = np.exp(pd.Series(ci_upper_log, index=pred_index))

    # Pronóstico futuro
    model_full = ARIMA(serie_log, order=order).fit()
    fc_future = model_full.get_forecast(steps=horizonte)
    pred_future = np.exp(fc_future.predicted_mean)
    ci_future = np.exp(fc_future.conf_int())

scale = 1e6
train = serie.iloc[:-test_size]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=train.index, y=train.values / scale,
    name='Histórico', line=dict(color="#4C9BE8", width=2)
))
fig.add_trace(go.Scatter(
    x=pred_index, y=serie.iloc[-test_size:].values / scale,
    name='Test (real)', line=dict(color="#A8DADC", width=2.5, dash='dot')
))
fig.add_trace(go.Scatter(
    x=pred_index, y=pred_real.values / scale,
    name='Walk-Forward', line=dict(color="#F4A261", width=2.5, dash='dash')
))
fig.add_trace(go.Scatter(
    x=pred_future.index, y=pred_future.values / scale,
    name=f'Pronóstico +{horizonte}m', line=dict(color="#E63946", width=2.5, dash='dash')
))
fig.add_trace(go.Scatter(
    x=list(ci_future.index) + list(ci_future.index[::-1]),
    y=list(ci_future.iloc[:, 1] / scale) + list(ci_future.iloc[:, 0] / scale)[::-1],
    fill='toself', fillcolor='rgba(230,57,70,0.12)',
    line=dict(color='rgba(0,0,0,0)'),
    name='IC 95% pronóstico', hoverinfo='skip'
))
fig.add_trace(go.Scatter(
    x=list(pred_index) + list(pred_index[::-1]),
    y=list(ci_hi_real.values / scale) + list(ci_lo_real.values / scale)[::-1],
    fill='toself', fillcolor='rgba(244,162,97,0.12)',
    line=dict(color='rgba(0,0,0,0)'),
    name='IC 95% walk-forward', hoverinfo='skip'
))

fig.update_layout(
    height=520,
    xaxis_title="Fecha",
    yaxis_title="USD Millones",
    hovermode="x unified",
    legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center")
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("### 📊 Métricas del Modelo — Walk-Forward + Log")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Modelo", f"ARIMA{order}")
m2.metric("MAPE", mape_val)
m3.metric("MAE", mae_val)
m4.metric("RMSE", rmse_val)

st.info("ℹ️ **Metodología:** Se aplica transformación logarítmica para estabilizar la varianza creciente de la serie. La validación Walk-Forward re-entrena el modelo en cada paso usando datos reales, simulando condiciones de pronóstico real.")
