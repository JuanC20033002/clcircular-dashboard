import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import (
    load_clima, COLORES_RIESGO, ZONAS_COLORES,
    CL_VERDE, CL_AZUL, CL_AZUL_MARINO, CL_CYAN
)

st.set_page_config(page_title="Rutas & Riesgo | CL Circular", layout="wide")

# ── LOGO EN SIDEBAR ───────────────────────────────────────────────────────────
logo_path = Path("assets/Logo-Cl-Circular.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

st.title("🛣️ Rutas Fronterizas — Riesgo Térmico por Corredor")
st.markdown("Análisis del riesgo climático en los principales cruces México–EE.UU. para operaciones de cadena de frío.")
st.divider()

# ── DATOS ESTÁTICOS DE RUTAS ──────────────────────────────────────────────────
# Coordenadas: [origen MX, destino EE.UU.]
RUTAS = {
    "Laredo / Nuevo Laredo": {
        "coords": [(27.4760, -99.5075), (27.5064, -99.4870)],
        "zona":   "Norte",
        "estado_mx": "Tamaulipas",
        "volumen": ">3M camiones/año",
        "productos": "Cerdo, Res, Aves",
        "lat_label": 27.49, "lon_label": -99.50,
    },
    "Ciudad Juárez / El Paso": {
        "coords": [(31.7380, -106.4870), (31.7619, -106.4850)],
        "zona":   "Norte",
        "estado_mx": "Chihuahua",
        "volumen": "Top 3 cruces",
        "productos": "Res, Ganado en pie",
        "lat_label": 31.75, "lon_label": -106.49,
    },
    "Nogales / Nogales": {
        "coords": [(31.3236, -110.9343), (31.3404, -110.9343)],
        "zona":   "Noroeste",
        "estado_mx": "Sonora",
        "volumen": "41,833 MT anuales",
        "productos": "Pollo 19.9k MT · Cerdo 14.8k MT · Res 7.1k MT",
        "lat_label": 31.33, "lon_label": -110.93,
    },
    "Reynosa / McAllen": {
        "coords": [(26.0800, -98.2773), (26.2034, -98.2300)],
        "zona":   "Norte",
        "estado_mx": "Tamaulipas",
        "volumen": "Crecimiento sostenido",
        "productos": "Cárnicos procesados",
        "lat_label": 26.14, "lon_label": -98.25,
    },
    "Tijuana / Otay Mesa": {
        "coords": [(32.5149, -117.0382), (32.5530, -117.0470)],
        "zona":   "Noroeste",
        "estado_mx": "Baja California",
        "volumen": "Alto tráfico BC",
        "productos": "Res, Aves, Procesados",
        "lat_label": 32.53, "lon_label": -117.04,
    },
}

MESES = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

# ── CARGA DE DATOS CLIMÁTICOS ─────────────────────────────────────────────────
df_clima = load_clima()

# IRT promedio por zona y mes (promedio de todos los años disponibles)
irt_zona_mes = (
    df_clima.groupby(["zona", "month"])["IRT"]
    .mean()
    .reset_index()
    .rename(columns={"month": "mes_num"})
)

def get_irt_zona(zona: str) -> dict:
    """Devuelve dict {mes_num: IRT} para una zona."""
    sub = irt_zona_mes[irt_zona_mes["zona"] == zona]
    return dict(zip(sub["mes_num"], sub["IRT"]))

def irt_to_nivel(irt: float) -> str:
    if irt >= 60:   return "Alto"
    elif irt >= 35: return "Medio"
    else:           return "Bajo"

def irt_to_color(irt: float) -> str:
    return COLORES_RIESGO[irt_to_nivel(irt)]

# ── FILTRO DE AÑO ─────────────────────────────────────────────────────────────
año_sel = st.slider("Filtrar año de referencia climática:", 2018, 2025, 2024)
irt_año = (
    df_clima[df_clima["year"] == año_sel]
    .groupby(["zona", "month"])["IRT"]
    .mean()
    .reset_index()
    .rename(columns={"month": "mes_num"})
)

def get_irt_año(zona: str) -> dict:
    sub = irt_año[irt_año["zona"] == zona]
    return dict(zip(sub["mes_num"], sub["IRT"]))

# IRT anual promedio por ruta
for nombre, r in RUTAS.items():
    irt_dict = get_irt_año(r["zona"])
    r["irt_promedio"] = round(sum(irt_dict.values()) / len(irt_dict), 1) if irt_dict else 0
    r["mes_critico"]  = max(irt_dict, key=irt_dict.get) if irt_dict else 6
    r["irt_mes_max"]  = round(irt_dict.get(r["mes_critico"], 0), 1)

st.divider()

# ── SECCIÓN B: MAPA DE RUTAS ──────────────────────────────────────────────────
st.markdown("### 🗺️ Mapa de Corredores Fronterizos")
st.caption("Color de cada ruta según el IRT promedio anual de su zona climática.")

fig_map = go.Figure()

# Fondo del mapa
fig_map.update_layout(
    geo=dict(
        scope="north america",
        showland=True,     landcolor="#F5F5F5",
        showocean=True,    oceancolor="#E8F4FD",
        showlakes=True,    lakecolor="#E8F4FD",
        showrivers=False,
        showcountries=True, countrycolor="#CCCCCC",
        showsubunits=True,  subunitcolor="#E0E0E0",
        center=dict(lat=28, lon=-104),
        projection_scale=4.2,
        lonaxis_range=[-120, -85],
        lataxis_range=[20, 38],
    ),
    paper_bgcolor="#FFFFFF",
    margin=dict(l=0, r=0, t=10, b=0),
    height=500,
    showlegend=True,
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#DDDDDD",
        borderwidth=1,
        font=dict(color=CL_AZUL_MARINO)
    )
)

# Dibujar cada ruta
niveles_en_leyenda = set()
for nombre, r in RUTAS.items():
    irt   = r["irt_promedio"]
    nivel = irt_to_nivel(irt)
    color = irt_to_color(irt)
    lats  = [r["coords"][0][0], r["coords"][1][0]]
    lons  = [r["coords"][0][1], r["coords"][1][1]]
    show_legend = nivel not in niveles_en_leyenda
    niveles_en_leyenda.add(nivel)

    # Línea de ruta
    fig_map.add_trace(go.Scattergeo(
        lat=lats, lon=lons,
        mode="lines",
        line=dict(width=5, color=color),
        name=f"Riesgo {nivel}" if show_legend else nivel,
        showlegend=show_legend,
        hoverinfo="skip"
    ))

    # Punto del cruce con tooltip
    fig_map.add_trace(go.Scattergeo(
        lat=[r["lat_label"]],
        lon=[r["lon_label"]],
        mode="markers+text",
        marker=dict(size=12, color=color, line=dict(color="white", width=2)),
        text=[nombre.split("/")[0].strip()],
        textposition="top right",
        textfont=dict(size=10, color=CL_AZUL_MARINO),
        showlegend=False,
        hovertemplate=(
            f"<b>{nombre}</b><br>"
            f"Zona: {r['zona']}<br>"
            f"IRT Promedio {año_sel}: <b>{irt}</b> — {nivel}<br>"
            f"Mes más crítico: <b>{MESES[r['mes_critico']-1]}</b> (IRT {r['irt_mes_max']})<br>"
            f"Volumen: {r['volumen']}<br>"
            f"Productos: {r['productos']}"
            "<extra></extra>"
        )
    ))

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# ── SECCIÓN A: TARJETAS POR RUTA ──────────────────────────────────────────────
st.markdown("### 📋 Detalle por Corredor")

COLOR_BG = {"Alto": "#FFF5F5", "Medio": "#FFFBF0", "Bajo": "#F0FFF4"}
ICONO    = {"Alto": "🔴", "Medio": "🟡", "Bajo": "🟢"}
RECOMENDACION = {
    "Alto":  "Protocolo de emergencia activo. Monitoreo de temperatura cada 30 min. Sensores IoT críticos.",
    "Medio": "Monitoreo activo recomendado. Revisar alertas cada 2 horas durante tránsito.",
    "Bajo":  "Condiciones favorables. Monitoreo estándar suficiente.",
}

cols = st.columns(len(RUTAS))
for i, (nombre, r) in enumerate(RUTAS.items()):
    irt   = r["irt_promedio"]
    nivel = irt_to_nivel(irt)
    color = irt_to_color(irt)
    bg    = COLOR_BG[nivel]
    icono = ICONO[nivel]
    rec   = RECOMENDACION[nivel]
    mes_nombre = MESES[r["mes_critico"] - 1]

    with cols[i]:
        st.markdown(f"""
        <div style="
            background:{bg};
            border-top: 4px solid {color};
            border-radius: 10px;
            padding: 16px 14px;
            height: 100%;
            box-shadow: 0 2px 6px rgba(13,31,78,0.08);
        ">
            <p style="font-size:0.8rem; color:#888; margin:0 0 4px 0;">
                {r['estado_mx']} → EE.UU.
            </p>
            <h4 style="margin:0 0 10px 0; color:{CL_AZUL_MARINO}; font-size:0.9rem; line-height:1.3;">
                🛣️ {nombre}
            </h4>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="font-size:2rem; font-weight:800; color:{color};">{irt}</span>
                <span style="font-size:0.75rem; color:#666;">IRT<br>promedio</span>
            </div>
            <span style="
                background:{color}; color:white;
                padding:2px 10px; border-radius:12px;
                font-size:11px; font-weight:600;
            ">{icono} Riesgo {nivel}</span>
            <hr style="border:none; border-top:1px solid #E0E0E0; margin:10px 0;">
            <p style="font-size:0.78rem; color:#555; margin:0 0 4px 0;">
                📅 <b>Mes crítico:</b> {mes_nombre} (IRT {r['irt_mes_max']})
            </p>
            <p style="font-size:0.78rem; color:#555; margin:0 0 4px 0;">
                📦 {r['productos']}
            </p>
            <p style="font-size:0.78rem; color:#555; margin:0 0 8px 0;">
                🚛 {r['volumen']}
            </p>
            <p style="font-size:0.75rem; color:#444; background:white; 
                      padding:6px 8px; border-radius:6px; margin:0; line-height:1.4;">
                💡 {rec}
            </p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── SECCIÓN C: MATRIZ RUTA × MES ─────────────────────────────────────────────
st.markdown("### 🗓️ Matriz de Riesgo — Ruta × Mes")
st.caption(f"Nivel de riesgo térmico por corredor y mes — {año_sel}")

matrix_data = []
for nombre, r in RUTAS.items():
    irt_dict = get_irt_año(r["zona"])
    row = {"Corredor": nombre.split("/")[0].strip()}
    for m in range(1, 13):
        irt_val = irt_dict.get(m, 0)
        nivel   = irt_to_nivel(irt_val)
        row[MESES[m-1]] = f"{ICONO[nivel]} {irt_val:.0f}"
    matrix_data.append(row)

df_matrix = pd.DataFrame(matrix_data).set_index("Corredor")
st.dataframe(df_matrix, use_container_width=True, height=230)

st.divider()
st.caption("Nota: IRT calculado sobre datos climáticos representativos por zona geográfica | Marzo 2026")
