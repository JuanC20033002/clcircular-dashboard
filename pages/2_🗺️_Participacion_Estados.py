import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import (
    load_importaciones_estado, load_exportaciones_estado,
    CL_VERDE, CL_AZUL, CL_AZUL_MARINO, CL_CYAN
)

st.set_page_config(page_title="Participación por Estado | CL Circular", layout="wide")

# ── LOGO EN SIDEBAR ───────────────────────────────────────────────────────────
logo_path = Path("assets/Logo-Cl-Circular.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

st.title("🗺️ Participación por Estado — 2025")
st.markdown("Distribución del valor comercial de carne y despojos por entidad federativa.")
st.divider()

# ── MAPEO A NOMBRES GEOJSON ───────────────────────────────────────────────────
NOMBRE_GEOJSON = {
    "Aguascalientes":                  "Aguascalientes",
    "Baja California":                 "Baja California",
    "Baja California Sur":             "Baja California Sur",
    "Campeche":                        "Campeche",
    "Coahuila de Zaragoza":            "Coahuila",
    "Colima":                          "Colima",
    "Chiapas":                         "Chiapas",
    "Chihuahua":                       "Chihuahua",
    "Ciudad de México":                "Distrito Federal",
    "Durango":                         "Durango",
    "Guanajuato":                      "Guanajuato",
    "Guerrero":                        "Guerrero",
    "Hidalgo":                         "Hidalgo",
    "Jalisco":                         "Jalisco",
    "Estado de México":                "México",
    "Michoacán de Ocampo":             "Michoacán",
    "Morelos":                         "Morelos",
    "Nayarit":                         "Nayarit",
    "Nuevo León":                      "Nuevo León",
    "Oaxaca":                          "Oaxaca",
    "Puebla":                          "Puebla",
    "Querétaro":                       "Querétaro",
    "Quintana Roo":                    "Quintana Roo",
    "San Luis Potosí":                 "San Luis Potosí",
    "Sinaloa":                         "Sinaloa",
    "Sonora":                          "Sonora",
    "Tabasco":                         "Tabasco",
    "Tamaulipas":                      "Tamaulipas",
    "Tlaxcala":                        "Tlaxcala",
    "Veracruz de Ignacio de la Llave": "Veracruz",
    "Yucatán":                         "Yucatán",
    "Zacatecas":                       "Zacatecas",
}
TODOS_LOS_ESTADOS = list(NOMBRE_GEOJSON.keys())
GEOJSON_URL = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"

def completar_estados(df):
    df_completo = pd.DataFrame({"State": TODOS_LOS_ESTADOS})
    df_completo = df_completo.merge(df, on="State", how="left")
    df_completo["Trade Value"] = df_completo["Trade Value"].fillna(0)
    df_completo["Share"]       = df_completo["Share"].fillna(0)
    df_completo["State_GeoJSON"] = df_completo["State"].map(NOMBRE_GEOJSON)
    return df_completo

df_imp = completar_estados(load_importaciones_estado())
df_exp = completar_estados(load_exportaciones_estado())

# ── SELECTOR DE FLUJO ─────────────────────────────────────────────────────────
flujo = st.radio("Selecciona flujo:", ["Importaciones", "Exportaciones"], horizontal=True)
df = df_imp if flujo == "Importaciones" else df_exp

# Paleta del mapa según flujo
color_scale = (
    ["#FFFFFF", CL_CYAN, CL_AZUL, CL_AZUL_MARINO]   # azules para importaciones
    if flujo == "Importaciones"
    else ["#FFFFFF", "#B5E48C", CL_VERDE, "#1B5E20"]  # verdes para exportaciones
)

# ── KPIs rápidos ──────────────────────────────────────────────────────────────
top1      = df.nlargest(1, "Share").iloc[0]
total_usd = df["Trade Value"].sum()
estados_activos = (df["Share"] > 0).sum()

k1, k2, k3 = st.columns(3)
k1.metric("Estado líder",      top1["State"],               f"{top1['Share']:.1f}% del total")
k2.metric("Valor total",       f"${total_usd/1e9:.2f}B USD", f"{flujo} 2024")
k3.metric("Estados con flujo", f"{estados_activos} / 32",    "entidades registradas")

st.divider()

# ── MAPA + TOP 10 ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    fig_map = px.choropleth(
        df,
        geojson=GEOJSON_URL,
        locations="State_GeoJSON",
        featureidkey="properties.name",
        color="Share",
        color_continuous_scale=color_scale,
        range_color=[0, df["Share"].max()],
        hover_name="State",
        hover_data={"Trade Value": ":,.0f", "Share": ":.2f", "State_GeoJSON": False},
        labels={"Share": "% Participación", "Trade Value": "Valor USD"},
        title=f"{flujo} de Carne por Estado — % del total nacional (2024)"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="#FFFFFF",
        font=dict(color=CL_AZUL_MARINO),
        title_font=dict(size=14, color=CL_AZUL_MARINO),
        coloraxis_colorbar=dict(
            title="% Part.",
            tickfont=dict(color=CL_AZUL_MARINO)
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.markdown(f"### 🏆 Top 10 Estados — {flujo}")
    top10 = df.nlargest(10, "Share")[["State", "Trade Value", "Share"]].copy()
    top10["Trade Value"] = top10["Trade Value"].apply(lambda x: f"${x/1e6:.1f}M")
    top10["Share"]       = top10["Share"].apply(lambda x: f"{x:.1f}%")
    top10.columns        = ["Estado", "Valor (USD)", "% Nacional"]
    top10 = top10.reset_index(drop=True)
    top10.index += 1
    st.dataframe(top10, use_container_width=True, height=420)

st.divider()

# ── BARRAS HORIZONTALES ───────────────────────────────────────────────────────
st.markdown(f"### 📊 Top 10 Estados por {flujo} — 2025")
top10_bar = df[df["Share"] > 0].nlargest(10, "Share").copy()
top10_bar = top10_bar.sort_values("Share", ascending=True)  # ascendente para que el mayor quede arriba en horizontal

color_bar = CL_AZUL if flujo == "Importaciones" else CL_VERDE

fig_bar = px.bar(
    top10_bar,
    x="Share", y="State", orientation="h",
    color="Share",
    color_continuous_scale=(
        ["#E8F4FD", CL_CYAN, CL_AZUL, CL_AZUL_MARINO]
        if flujo == "Importaciones"
        else ["#F1F8E9", "#AED581", CL_VERDE, "#1B5E20"]
    ),
    labels={"Share": "% Participación", "State": "Estado"},
    title=f"Top 10 Estados por {flujo} de Carne — 2024",
    text="Share"
)
fig_bar.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)
fig_bar.update_layout(
    height=420,
    showlegend=False,
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(color=CL_AZUL_MARINO),
    title_font=dict(size=14, color=CL_AZUL_MARINO),
    xaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="% Participación"),
    yaxis=dict(showgrid=False),
    coloraxis_showscale=False
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.caption("Fuente: DataMéxico — Secretaría de Economía | Meat and Edible Offal, 2024 | Marzo 2026")
