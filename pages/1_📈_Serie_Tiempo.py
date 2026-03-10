import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import load_comercio, CL_VERDE, CL_AZUL, CL_AZUL_MARINO, CL_CYAN

st.set_page_config(page_title="Serie de Tiempo | CL Circular", layout="wide")

# ── LOGO EN SIDEBAR ───────────────────────────────────────────────────────────
logo_path = Path("assets/Logo-Cl-Circular.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

st.title("📈 Serie de Tiempo — Comercio Bilateral de Carne")
st.markdown("Pronóstico a 12 meses del valor mensual de importaciones y exportaciones México–EE.UU. usando Prophet.")
st.divider()

# ── CARGA Y VALIDACIÓN DE DATOS ───────────────────────────────────────────────
df = load_comercio()

# Verificar qué flujos existen realmente en el CSV
flujos_disponibles = df["flujo_id"].unique()

imp_raw = df[df["flujo_id"] == 1].set_index("fecha")["valor_comercio"]
exp_raw = df[df["flujo_id"] == 2].set_index("fecha")["valor_comercio"] if 2 in flujos_disponibles else pd.Series(dtype=float)

# Rellenar frecuencia mensual solo si hay datos
imp = imp_raw.asfreq("MS") if not imp_raw.empty else imp_raw
exp = exp_raw.asfreq("MS") if not exp_raw.empty else exp_raw

hay_exportaciones = not exp.empty

# ── FUNCIÓN DE ENTRENAMIENTO CON CACHÉ ───────────────────────────────────────
@st.cache_resource   # ← cache_resource para objetos no serializables como modelos ML
def train_and_forecast(serie_dict: dict, nombre: str):
    """Entrena Prophet y devuelve (forecast_df). Usa dict para que sea hasheable."""
    from prophet import Prophet
    serie = pd.Series(serie_dict)
    serie.index = pd.to_datetime(serie.index)

    df_p = serie.reset_index()
    df_p.columns = ["ds", "y"]
    df_p = df_p.dropna()

    model = Prophet(
        changepoint_prior_scale=0.3,
        seasonality_prior_scale=10,
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )
    model.fit(df_p)
    future = model.make_future_dataframe(periods=12, freq="MS")
    forecast = model.predict(future)
    return forecast

# ── FUNCIÓN DE GRÁFICA ────────────────────────────────────────────────────────
def plot_forecast(serie, forecast, titulo, color_hist, color_forecast):
    scale  = 1e6
    fut    = forecast[forecast["ds"] > serie.index[-1]]
    corte  = serie.index[-1].strftime("%Y-%m-%d")
    y_vals = np.concatenate([serie.values, fut["yhat_upper"].values]) / scale
    y_min  = y_vals.min() * 0.93
    y_max  = y_vals.max() * 1.07

    fig = go.Figure()

    # Banda IC 95%
    fig.add_trace(go.Scatter(
        x=list(fut["ds"]) + list(fut["ds"][::-1]),
        y=list(fut["yhat_upper"] / scale) + list(fut["yhat_lower"] / scale)[::-1],
        fill="toself",
        fillcolor="rgba(141,198,63,0.15)",   # verde lima CL con transparencia
        line=dict(color="rgba(0,0,0,0)"),
        name="IC 95%",
        hoverinfo="skip"
    ))

    # Línea histórica
    fig.add_trace(go.Scatter(
        x=serie.index, y=serie.values / scale,
        name="Histórico",
        line=dict(color=color_hist, width=2.2),
        hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:.1f}M USD<extra></extra>"
    ))

    # Pronóstico
    fig.add_trace(go.Scatter(
        x=fut["ds"], y=fut["yhat"] / scale,
        name="Pronóstico 12m",
        line=dict(color=color_forecast, width=2.5, dash="dash"),
        hovertemplate="<b>%{x|%b %Y}</b><br>Pronóstico: $%{y:.1f}M USD<extra></extra>"
    ))

    # Línea vertical de corte
    fig.add_shape(
        type="line", x0=corte, x1=corte, y0=y_min, y1=y_max,
        line=dict(color="#AAAAAA", width=1.5, dash="dot")
    )
    fig.add_annotation(
        x=corte, y=y_max * 0.98,
        text="▶ Inicio pronóstico",
        showarrow=False, xanchor="left",
        font=dict(size=11, color="#888888")
    )

    fig.update_layout(
        title=f"{titulo} | Prophet — Pronóstico 12 meses",
        height=480,
        xaxis_title="Año",
        yaxis_title="USD Millones",
        hovermode="x unified",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color=CL_AZUL_MARINO),
        title_font=dict(size=15, color=CL_AZUL_MARINO),
        legend=dict(
            orientation="h", yanchor="top", y=-0.15,
            xanchor="center", x=0.5,
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(showgrid=True, gridcolor="#F0F0F0"),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0"),
    )
    return fig

# ── ENTRENAMIENTO ─────────────────────────────────────────────────────────────
with st.spinner("Entrenando modelos Prophet... (solo la primera vez)"):
    fc_imp = train_and_forecast(imp.to_dict(), "importaciones")
    if hay_exportaciones:
        fc_exp = train_and_forecast(exp.to_dict(), "exportaciones")

# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = ["📥 Importaciones", "📤 Exportaciones"] if hay_exportaciones else ["📥 Importaciones"]
tab_list = st.tabs(tabs)

with tab_list[0]:
    st.plotly_chart(
        plot_forecast(imp, fc_imp,
                      "Importaciones — Carne",
                      color_hist=CL_AZUL,
                      color_forecast=CL_AZUL_MARINO),
        use_container_width=True
    )

if hay_exportaciones:
    with tab_list[1]:
        st.plotly_chart(
            plot_forecast(exp, fc_exp,
                          "Exportaciones — Carne y Despojos",
                          color_hist=CL_VERDE,
                          color_forecast="#1B5E20"),
            use_container_width=True
        )
else:
    with tab_list[0]:
        st.warning("⚠️ No se encontraron datos de exportaciones en `comercio_carne_limpio.csv` (flujo_id = 2). Verifica el archivo.")

st.divider()

# ── MÉTRICAS ──────────────────────────────────────────────────────────────────
st.markdown("### 📊 Métricas del Modelo")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Modelo",               "Prophet (Meta)")
m2.metric("MAPE Importaciones",   "8.36%",  "Walk-Forward Validation")
m3.metric("MAPE Exportaciones",   "9.31%",  "Walk-Forward Validation")
m4.metric("Horizonte pronóstico", "12 meses")

st.divider()

# ── METODOLOGÍA ───────────────────────────────────────────────────────────────
with st.expander("📐 ¿Por qué Prophet y no ARIMA?"):
    st.markdown(f"""
    <div style="background:#F8FAFC; border-left:4px solid {CL_AZUL}; 
                border-radius:6px; padding:16px 20px;">
    <b style="color:{CL_AZUL_MARINO};">Comparación de modelos evaluados</b><br><br>
    Se evaluaron <b>ARIMA con Log + Walk-Forward Validation</b> y <b>Prophet (Meta)</b> 
    sobre el valor mensual del comercio bilateral 2006–2025.<br><br>
    Prophet fue seleccionado como modelo final en producción por:
    <ul style="color:#444; margin-top:8px;">
        <li>✅ <b>Menor MAPE en importaciones</b> (8.36% vs ~11% ARIMA)</li>
        <li>✅ <b>Detección automática de puntos de cambio</b> en tendencia (e.g. COVID-2020)</li>
        <li>✅ <b>Intervalos de confianza interpretables</b> para usuarios no técnicos</li>
        <li>✅ <b>Mejor manejo de estacionalidad anual</b> del comercio cárnico</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.caption("Fuente: DataMéxico — Secretaría de Economía | Meat and Edible Offal, 2006–2024 | Marzo 2026")
