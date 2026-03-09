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
    text_auto=".0f"
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
zona_max    = df_f.groupby("zona")["IRT"].mean().idxmax()
mes_max_num = df_f.groupby("month")["IRT"].mean().idxmax()
irt_max     = df_f.groupby("zona")["IRT"].mean().max()
dias_max    = int(df_f[df_f["zona"] == zona_max]["dias_calor"].max())
meses_nombres = {
    1:"enero", 2:"febrero", 3:"marzo", 4:"abril", 5:"mayo", 6:"junio",
    7:"julio", 8:"agosto", 9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"
}

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #FFF5F5 0%, #FFF0E6 100%);
    border-left: 4px solid #E63946;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 8px 0;
">
<span style="font-size:1.1rem; font-weight:700; color:#E63946;">
    🔴 Mayor riesgo térmico en {year_sel}
</span><br><br>
<span style="color:{CL_AZUL_MARINO}; font-size:0.95rem;">
    La zona <b>{zona_max}</b> durante <b>{meses_nombres[mes_max_num]}</b> representa el mayor 
    riesgo para la cadena de frío, con un IRT promedio de <b>{irt_max:.1f}/100</b> y hasta 
    <b>{dias_max} días</b> sobre 35°C en el mes. Los operadores logísticos en esta zona deben 
    reforzar monitoreo activo de temperatura en ese período.
</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── RIESGO POR CORREDOR FRONTERIZO ────────────────────────────────────────────
st.markdown("### 🛣️ Riesgo Térmico por Corredor Fronterizo")
st.caption(f"IRT promedio {year_sel} según zona climática de cada cruce. Usa el slider de año para actualizar.")

RUTAS = {
    "Laredo / Nuevo Laredo": {"zona": "Norte",    "estado": "Tamaulipas",      "productos": "Cerdo · Res · Aves",      "volumen": "+3M camiones/año"},
    "Cd. Juárez / El Paso":  {"zona": "Norte",    "estado": "Chihuahua",       "productos": "Res · Ganado en pie",     "volumen": "Top 3 cruces MX–EE.UU."},
    "Nogales / Nogales":     {"zona": "Noroeste", "estado": "Sonora",          "productos": "Pollo · Cerdo · Res",     "volumen": "41,833 MT/año"},
    "Reynosa / McAllen":     {"zona": "Norte",    "estado": "Tamaulipas",      "productos": "Cárnicos procesados",     "volumen": "Crecimiento sostenido"},
    "Tijuana / Otay Mesa":   {"zona": "Noroeste", "estado": "Baja California", "productos": "Res · Aves · Procesados", "volumen": "Alto tráfico BC"},
}

MESES_CORTOS = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
COLOR_BG     = {"Alto": "#FFF5F5", "Medio": "#FFFBF0", "Bajo": "#F0FFF4"}
ICONO_NIV    = {"Alto": "🔴", "Medio": "🟡", "Bajo": "🟢"}


def nivel_riesgo(irt):
    return "Alto" if irt >= 60 else "Medio" if irt >= 35 else "Bajo"

# IRT del año seleccionado por zona
irt_año_zona = (
    df[df["year"] == year_sel]
    .groupby(["zona", "month"])["IRT"]
    .mean()
    .reset_index()
)

def get_irt_zona_dict(zona):
    sub = irt_año_zona[irt_año_zona["zona"] == zona]
    return dict(zip(sub["month"], sub["IRT"]))

# Calcular métricas por ruta
rutas_calc = {}
for nombre, r in RUTAS.items():
    irt_dict = get_irt_zona_dict(r["zona"])
    if irt_dict:
        irt_prom    = round(sum(irt_dict.values()) / len(irt_dict), 1)
        mes_max     = max(irt_dict, key=irt_dict.get)
        irt_mes_max = round(irt_dict[mes_max], 1)
    else:
        irt_prom, mes_max, irt_mes_max = 0, 6, 0
    rutas_calc[nombre] = {**r, "irt": irt_prom, "mes_max": mes_max, "irt_mes_max": irt_mes_max}

# ── TARJETAS SIN RECOMENDACIÓN INDIVIDUAL ────────────────────────────────────
cols = st.columns(len(RUTAS))
for i, (nombre, r) in enumerate(rutas_calc.items()):
    nivel = nivel_riesgo(r["irt"])
    color = COLORES_RIESGO[nivel]
    with cols[i]:
        st.markdown(f"""
        <div style="
            background:{COLOR_BG[nivel]};
            border-top:4px solid {color};
            border-radius:10px;
            padding:14px 12px;
            box-shadow:0 2px 6px rgba(13,31,78,0.08);
        ">
            <p style="font-size:0.75rem;color:#888;margin:0 0 3px 0;">
                {r['estado']} → EE.UU.
            </p>
            <p style="font-size:0.82rem;font-weight:700;color:{CL_AZUL_MARINO};
                      margin:0 0 8px 0;line-height:1.3;">
                🛣️ {nombre}
            </p>
            <span style="font-size:1.8rem;font-weight:800;color:{color};">{r['irt']}</span>
            <span style="font-size:0.72rem;color:#666;"> IRT prom.</span><br><br>
            <span style="background:{color};color:white;padding:2px 8px;
                         border-radius:10px;font-size:10px;font-weight:600;">
                {ICONO_NIV[nivel]} Riesgo {nivel}
            </span>
            <hr style="border:none;border-top:1px solid #E0E0E0;margin:8px 0;">
            <p style="font-size:0.74rem;color:#555;margin:2px 0;">
                📅 <b>Mes crítico:</b> {MESES_CORTOS[r['mes_max']-1]} (IRT {r['irt_mes_max']})
            </p>
            <p style="font-size:0.74rem;color:#555;margin:2px 0;">📦 {r['productos']}</p>
            <p style="font-size:0.74rem;color:#555;margin:2px 0;">🚛 {r['volumen']}</p>
        </div>
        """, unsafe_allow_html=True)


st.divider()

# ── MATRIZ CORREDOR × MES ─────────────────────────────────────────────────────
st.markdown("### 🗓️ Matriz de Riesgo — Corredor × Mes")
st.caption(f"Nivel de riesgo térmico por corredor y mes — {year_sel}")

matrix_rows = []
for nombre, r in rutas_calc.items():
    irt_dict = get_irt_zona_dict(r["zona"])
    row = {"Corredor": nombre.split("/")[0].strip()}
    for m in range(1, 13):
        v = irt_dict.get(m, 0)
        row[MESES_CORTOS[m-1]] = f"{ICONO_NIV[nivel_riesgo(v)]} {v:.0f}"
    matrix_rows.append(row)

df_matrix = pd.DataFrame(matrix_rows).set_index("Corredor")
st.dataframe(df_matrix, use_container_width=True, height=225)

st.divider()

# ── METODOLOGÍA IRT ───────────────────────────────────────────────────────────
with st.expander("📐 ¿Cómo se calcula el Índice de Riesgo Térmico (IRT)?"):
    st.markdown("""
    El **IRT** es un índice compuesto de 0 a 100 que mide el nivel de riesgo climático 
    para operaciones de transporte refrigerado en cada zona y mes.
    ### Fórmula
    """)
    st.latex(r"IRT = (0.5 \times T_{norm}) + (0.3 \times D_{norm}) + (0.2 \times H_{norm})")
    st.markdown("""
    ### Variables
    | Variable | Peso | Descripción | Rango original |
    |---|---|---|---|
    | $T_{norm}$ | 50% | Temperatura promedio mensual normalizada | 0 – 45 °C |
    | $D_{norm}$ | 30% | Días con temperatura > 35 °C en el mes | 0 – 31 días |
    | $H_{norm}$ | 20% | Humedad relativa promedio mensual | 0 – 100% |

    Cada variable se normaliza al rango [0, 100] antes de aplicar los pesos:
    """)
    st.latex(r"X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}} \times 100")
    st.markdown("""
    ### Niveles de Riesgo
    | Nivel | Rango IRT | Implicación operativa |
    |---|---|---|
    | 🟢 **Bajo** | 0 – 34 | Condiciones favorables, monitoreo estándar |
    | 🟡 **Medio** | 35 – 59 | Requiere monitoreo activo y revisiones frecuentes |
    | 🔴 **Alto** | 60 – 100 | Riesgo crítico, protocolo de emergencia en cadena de frío |

    ### ¿Por qué estos pesos?
    - **Temperatura promedio (50%)** — determina la carga térmica base sobre el equipo de refrigeración
    - **Días extremos >35°C (30%)** — captura eventos pico que pueden romper la cadena de frío
    - **Humedad (20%)** — agrava el esfuerzo del sistema de enfriamiento en zonas costeras
    """)

st.divider()
