import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import load_clima, COLORES_RIESGO, ZONAS_COLORES

st.set_page_config(page_title="Riesgo Climático | CL Circular", layout="wide")

st.title("🌡️ Índice de Riesgo Térmico — Cadena de Frío")
st.markdown("Análisis del riesgo climático por zona geográfica para operaciones de transporte refrigerado.")
st.divider()

df = load_clima()

# Filtros
col1, col2 = st.columns(2)
with col1:
    year_sel = st.slider("Año:", min_value=2018, max_value=2025, value=2024)
with col2:
    zonas_sel = st.multiselect(
        "Zonas:",
        options=df["zona"].unique().tolist(),
        default=df["zona"].unique().tolist()
    )

df_f = df[(df["year"] == year_sel) & (df["zona"].isin(zonas_sel))]

# --- Heatmap mes x zona ---
st.markdown("### 🔥 Heatmap de Riesgo — Mes × Zona")
pivot = df_f.groupby(["zona", "month"])["IRT"].mean().reset_index()
pivot_wide = pivot.pivot(index="zona", columns="month", values="IRT")
pivot_wide.columns = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

fig_heat = px.imshow(
    pivot_wide,
    color_continuous_scale=["#2A9D8F", "#F4A261", "#E63946"],
    zmin=0, zmax=100,
    labels=dict(color="IRT"),
    title=f"Índice de Riesgo Térmico promedio por Zona y Mes — {year_sel}",
    aspect="auto"
)
fig_heat.update_layout(height=350)
st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

# --- Línea temporal IRT anual ---
with col1:
    st.markdown("### 📈 Tendencia Anual del IRT por Zona")
    trend = df[df["zona"].isin(zonas_sel)].groupby(["year","zona"])["IRT"].mean().reset_index()
    fig_line = px.line(
        trend, x="year", y="IRT", color="zona",
        color_discrete_map=ZONAS_COLORES,
        markers=True,
        labels={"year": "Año", "IRT": "IRT Promedio", "zona": "Zona"},
        title="Evolución del Índice de Riesgo Térmico 2018–2025"
    )
    fig_line.update_layout(height=380)
    st.plotly_chart(fig_line, use_container_width=True)

# --- Distribución de niveles ---
with col2:
    st.markdown("### 🟢🟡🔴 Distribución de Niveles de Riesgo")
    nivel_counts = df_f.groupby(["zona","nivel_riesgo"]).size().reset_index(name="meses")
    fig_bar = px.bar(
        nivel_counts, x="zona", y="meses", color="nivel_riesgo",
        color_discrete_map=COLORES_RIESGO,
        labels={"zona": "Zona", "meses": "Meses", "nivel_riesgo": "Riesgo"},
        title=f"Meses por Nivel de Riesgo — {year_sel}",
        barmode="stack"
    )
    fig_bar.update_layout(height=380)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# --- KPI insight automático ---
st.markdown("### 💡 Insight Automático")
zona_max = df_f.groupby("zona")["IRT"].mean().idxmax()
mes_max_num = df_f.groupby("month")["IRT"].mean().idxmax()
meses = {1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",
         7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}
dias_max = int(df_f[df_f["zona"]==zona_max]["dias_calor"].max())

st.info(f"""
🔴 **Mayor riesgo térmico en {year_sel}:** La zona **{zona_max}** durante **{meses[mes_max_num]}** 
representa el mayor riesgo para la cadena de frío, con hasta **{dias_max} días** sobre 35°C en el mes. 
Los operadores logísticos en esta zona deben reforzar monitoreo activo de temperatura en ese período.
""")
