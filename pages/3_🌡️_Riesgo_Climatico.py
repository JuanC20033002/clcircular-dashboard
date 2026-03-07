import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import (
    load_clima, COLORES_RIESGO, ZONAS_COLORES,
    CL_AZUL_MARINO, CL_VERDE, CL_AZUL, CL_CYAN
)

st.set_page_config(page_title="Riesgo Climático | CL Circular", layout="wide")

# ── LOGO EN SIDEBAR ───────────────────────────────────────────────────────────
logo_path = Path("assets/Logo-Cl-Circular.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

st.title("🌡️ Índice de Riesgo Térmico — Cadena de Frío")
st.markdown("Análisis del riesgo climático por zona geográfica para operaciones de transporte refrigerado.")
st.divider()

df = load_clima()

# ── FILTROS ───────────────────────────────────────────────────────────────────
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

# ── HEATMAP MES × ZONA ────────────────────────────────────────────────────────
st.markdown("### 🔥 Heatmap de Riesgo — Mes × Zona")
pivot = df_f.groupby(["zona", "month"])["IRT"].mean().reset_index()
pivot_wide = pivot.pivot(index="zona", columns="month", values="IRT")
pivot_wide.columns = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

fig_heat = px.imshow(
    pivot_wide,
    color_continuous_scale=["#3AACB8", "#F4A261", "#E63946"],
    zmin=0, zmax=100,
    labels=dict(color="IRT"),
    title=f"Índice de Riesgo Térmico promedio por Zona y Mes — {year_sel}",
    aspect="auto",
    text_auto=".0f"            # ← muestra el valor dentro de cada celda
)
fig_heat.update_layout(
    height=360,
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(color=CL_AZUL_MARINO),
    title_font=dict(size=15, color=CL_AZUL_MARINO)
)
st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

# ── TENDENCIA ANUAL ───────────────────────────────────────────────────────────
with col1:
    st.markdown("### 📈 Tendencia Anual del IRT por Zona")
    trend = (
        df[df["zona"].isin(zonas_sel)]
        .groupby(["year", "zona"])["IRT"]
        .mean()
        .reset_index()
    )
    fig_line = px.line(
        trend, x="year", y="IRT", color="zona",
        color_discrete_map=ZONAS_COLORES,
        markers=True,
        labels={"year": "Año", "IRT": "IRT Promedio", "zona": "Zona"},
        title="Evolución del Índice de Riesgo Térmico 2018–2025"
    )
    fig_line.update_layout(
        height=380,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color=CL_AZUL_MARINO),
        title_font=dict(size=14, color=CL_AZUL_MARINO),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    fig_line.update_xaxes(showgrid=True, gridcolor="#F0F0F0")
    fig_line.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
    st.plotly_chart(fig_line, use_container_width=True)

# ── DISTRIBUCIÓN DE NIVELES ───────────────────────────────────────────────────
with col2:
    st.markdown("### 🟢🟡🔴 Distribución de Niveles de Riesgo")
    nivel_counts = df_f.groupby(["zona", "nivel_riesgo"]).size().reset_index(name="meses")
    # Orden lógico de los niveles
    nivel_counts["nivel_riesgo"] = pd.Categorical(
        nivel_counts["nivel_riesgo"], categories=["Bajo", "Medio", "Alto"], ordered=True
    )
    nivel_counts = nivel_counts.sort_values("nivel_riesgo")

    fig_bar = px.bar(
        nivel_counts, x="zona", y="meses", color="nivel_riesgo",
        color_discrete_map=COLORES_RIESGO,
        labels={"zona": "Zona", "meses": "Meses", "nivel_riesgo": "Riesgo"},
        title=f"Meses por Nivel de Riesgo — {year_sel}",
        barmode="stack",
        category_orders={"nivel_riesgo": ["Bajo", "Medio", "Alto"]}
    )
    fig_bar.update_layout(
        height=380,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color=CL_AZUL_MARINO),
        title_font=dict(size=14, color=CL_AZUL_MARINO),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    fig_bar.update_xaxes(showgrid=False)
    fig_bar.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ── INSIGHT AUTOMÁTICO ────────────────────────────────────────────────────────
st.markdown("### 💡 Insight Automático")
zona_max   = df_f.groupby("zona")["IRT"].mean().idxmax()
mes_max_num = df_f.groupby("month")["IRT"].mean().idxmax()
meses_nombres = {
    1:"enero", 2:"febrero", 3:"marzo", 4:"abril", 5:"mayo", 6:"junio",
    7:"julio", 8:"agosto", 9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"
}
irt_max   = df_f.groupby("zona")["IRT"].mean().max()
dias_max  = int(df_f[df_f["zona"] == zona_max]["dias_calor"].max())

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #FFF5F5 0%, #FFF0E6 100%);
    border-left: 4px solid #E63946;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 8px 0;
">
<span style="font-size:1.1rem; font-weight:700; color:#E63946;">🔴 Mayor riesgo térmico en {year_sel}</span><br><br>
<span style="color:{CL_AZUL_MARINO}; font-size:0.95rem;">
La zona <b>{zona_max}</b> durante <b>{meses_nombres[mes_max_num]}</b> representa el mayor riesgo 
para la cadena de frío, con un IRT promedio de <b>{irt_max:.1f}/100</b> y hasta <b>{dias_max} días</b> 
sobre 35°C en el mes. Los operadores logísticos en esta zona deben reforzar monitoreo activo 
de temperatura en ese período.
</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── EXPANDER METODOLOGÍA ──────────────────────────────────────────────────────
with st.expander("📐 ¿Cómo se calcula el Índice de Riesgo Térmico (IRT)?"):
    st.markdown("""
    El **IRT** es un índice compuesto de 0 a 100 que mide el nivel de riesgo climático 
    para operaciones de transporte refrigerado en cada zona y mes.

    ### Fórmula
    """)

    st.latex(r"""
    IRT = (0.5 \times T_{norm}) + (0.3 \times D_{norm}) + (0.2 \times H_{norm})
    """)

    st.markdown("""
    ### Variables
    | Variable | Peso | Descripción | Rango original |
    |---|---|---|---|
    | $T_{norm}$ | 50% | Temperatura promedio mensual normalizada | 0 – 45 °C |
    | $D_{norm}$ | 30% | Días con temperatura > 35 °C en el mes | 0 – 31 días |
    | $H_{norm}$ | 20% | Humedad relativa promedio mensual | 0 – 100% |

    Cada variable se normaliza al rango [0, 100] antes de aplicar los pesos:
    """)

    st.latex(r"""
    X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}} \times 100
    """)

    st.markdown("""
    ### Niveles de Riesgo
    | Nivel | Rango IRT | Implicación operativa |
    |---|---|---|
    | 🟢 **Bajo** | 0 – 34 | Condiciones favorables, monitoreo estándar |
    | 🟡 **Medio** | 35 – 59 | Requiere monitoreo activo y revisiones frecuentes |
    | 🔴 **Alto** | 60 – 100 | Riesgo crítico, protocolo de emergencia en cadena de frío |

    ### ¿Por qué estos pesos?
    - **Temperatura promedio (50%)** — factor dominante; determina la carga térmica base sobre el equipo de refrigeración
    - **Días extremos >35°C (30%)** — captura eventos pico que pueden romper la cadena de frío aunque el promedio mensual sea moderado
    - **Humedad (20%)** — agrava el esfuerzo del sistema de enfriamiento, especialmente en zonas costeras como Noroeste y Sur-Golfo
    """)

st.divider()
st.caption("Nota: Datos climáticos basados en rangos representativos por zona para fines ilustrativos del prototipo | Marzo 2026")
