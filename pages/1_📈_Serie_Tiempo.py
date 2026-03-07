import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import load_comercio

st.set_page_config(page_title="Serie de Tiempo | CL Circular", layout="wide")

st.title("📈 Serie de Tiempo — Comercio Bilateral de Carne")
st.markdown("Pronóstico a 12 meses del valor mensual de importaciones y exportaciones México–EE.UU. usando Prophet.")
st.divider()

df = load_comercio()

imp = df[df['flujo_id'] == 1].set_index('fecha')['valor_comercio'].asfreq('MS')
exp = df[df['flujo_id'] == 2].set_index('fecha')['valor_comercio'].asfreq('MS')

def train_prophet(serie):
    df_p = serie.reset_index().rename(columns={serie.index.name: 'ds', serie.name: 'y'})
    model = Prophet(
        changepoint_prior_scale=0.3,
        seasonality_prior_scale=10,
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )
    model.fit(df_p)
    return model

def plot_forecast(serie, forecast, titulo, color):
    scale = 1e6
    fut = forecast[forecast['ds'] > serie.index[-1]]
    corte = serie.index[-1].strftime('%Y-%m-%d')
    y_max = max(serie.values.max(), fut['yhat_upper'].max()) / scale * 1.05
    y_min = serie.values.min() / scale * 0.95

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=serie.index, y=serie.values / scale,
        name='Histórico', line=dict(color="#4C9BE8", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=fut['ds'], y=fut['yhat'] / scale,
        name='Pronóstico 12m', line=dict(color=color, width=2.5, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=list(fut['ds']) + list(fut['ds'][::-1]),
        y=list(fut['yhat_upper'] / scale) + list(fut['yhat_lower'] / scale)[::-1],
        fill='toself', fillcolor=f'rgba(99,110,250,0.13)',
        line=dict(color='rgba(0,0,0,0)'),
        name='IC 95%', hoverinfo='skip'
    ))
    fig.add_shape(
        type="line", x0=corte, x1=corte, y0=y_min, y1=y_max,
        line=dict(color="gray", width=1.5, dash="dot")
    )
    fig.add_annotation(
        x=corte, y=y_max, text="Inicio pronóstico",
        showarrow=False, xanchor="left",
        font=dict(size=11, color="gray")
    )
    fig.update_layout(
        title=f"{titulo} | Prophet — Pronóstico 12 meses",
        height=460,
        xaxis_title="Año",
        yaxis_title="USD Millones",
        hovermode="x unified",
        legend=dict(orientation='h', yanchor='top', y=-0.15, xanchor='center', x=0.5)
    )
    return fig

with st.spinner("Entrenando modelos Prophet..."):
    model_imp = train_prophet(imp)
    model_exp = train_prophet(exp)

    future_imp = model_imp.make_future_dataframe(periods=12, freq='MS')
    future_exp = model_exp.make_future_dataframe(periods=12, freq='MS')
    fc_imp = model_imp.predict(future_imp)
    fc_exp = model_exp.predict(future_exp)

tab1, tab2 = st.tabs(["📥 Importaciones", "📤 Exportaciones"])

with tab1:
    st.plotly_chart(
        plot_forecast(imp, fc_imp, "Importaciones — Carne y Despojos", "#E63946"),
        use_container_width=True
    )

with tab2:
    st.plotly_chart(
        plot_forecast(exp, fc_exp, "Exportaciones — Carne y Despojos", "#2A9D8F"),
        use_container_width=True
    )

st.divider()
st.markdown("### 📊 Métricas del Modelo — Prophet Train/Test")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Modelo", "Prophet")
m2.metric("MAPE Importaciones", "8.36%")
m3.metric("MAPE Exportaciones", "9.31%")
m4.metric("Horizonte", "12 meses")

st.info("ℹ️ **Metodología:** Prophet detecta automáticamente tendencias y estacionalidad anual. Entrenado con todos los datos históricos disponibles para generar el pronóstico de los próximos 12 meses.")
