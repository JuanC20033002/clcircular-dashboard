import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import load_importaciones_estado, load_exportaciones_estado

st.set_page_config(page_title="Participación por Estado | CL Circular", layout="wide")

st.title("🗺️ Participación por Estado — 2024")
st.markdown("Distribución del valor comercial de carne y despojos por entidad federativa.")
st.divider()

# Nombres exactos del GeoJSON angelnmara
NOMBRE_GEOJSON = {
    "Aguascalientes": "Aguascalientes",
    "Baja California": "Baja California",
    "Baja California Sur": "Baja California Sur",
    "Campeche": "Campeche",
    "Coahuila de Zaragoza": "Coahuila",
    "Colima": "Colima",
    "Chiapas": "Chiapas",
    "Chihuahua": "Chihuahua",
    "Ciudad de México": "Distrito Federal",
    "Durango": "Durango",
    "Guanajuato": "Guanajuato",
    "Guerrero": "Guerrero",
    "Hidalgo": "Hidalgo",
    "Jalisco": "Jalisco",
    "Estado de México": "México",
    "Michoacán de Ocampo": "Michoacán",
    "Morelos": "Morelos",
    "Nayarit": "Nayarit",
    "Nuevo León": "Nuevo León",
    "Oaxaca": "Oaxaca",
    "Puebla": "Puebla",
    "Querétaro": "Querétaro",
    "Quintana Roo": "Quintana Roo",
    "San Luis Potosí": "San Luis Potosí",
    "Sinaloa": "Sinaloa",
    "Sonora": "Sonora",
    "Tabasco": "Tabasco",
    "Tamaulipas": "Tamaulipas",
    "Tlaxcala": "Tlaxcala",
    "Veracruz de Ignacio de la Llave": "Veracruz",
    "Yucatán": "Yucatán",
    "Zacatecas": "Zacatecas"
}

TODOS_LOS_ESTADOS = list(NOMBRE_GEOJSON.keys())

def completar_estados(df):
    df_completo = pd.DataFrame({"State": TODOS_LOS_ESTADOS})
    df_completo = df_completo.merge(df, on="State", how="left")
    df_completo["Trade Value"] = df_completo["Trade Value"].fillna(0)
    df_completo["Share"] = df_completo["Share"].fillna(0)
    df_completo["State_GeoJSON"] = df_completo["State"].map(NOMBRE_GEOJSON)
    return df_completo

df_imp = completar_estados(load_importaciones_estado())
df_exp = completar_estados(load_exportaciones_estado())

flujo = st.radio("Selecciona flujo:", ["Importaciones", "Exportaciones"], horizontal=True)
df = df_imp if flujo == "Importaciones" else df_exp

col1, col2 = st.columns([3, 2])

with col1:
    fig_map = px.choropleth(
        df,
        geojson="https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json",
        locations="State_GeoJSON",
        featureidkey="properties.name",
        color="Share",
        color_continuous_scale=["#3a3a3a", "#2A9D8F", "#F4A261", "#E63946"],
        range_color=[0, df["Share"].max()],
        hover_name="State",
        labels={"Share": "% Participación"},
        title=f"{flujo} de Carne por Estado (% del total nacional)"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.markdown(f"### 🏆 Top 10 Estados — {flujo}")
    top10 = df.nlargest(10, "Share")[["State", "Trade Value", "Share"]].copy()
    top10["Trade Value"] = top10["Trade Value"].apply(lambda x: f"${x/1e6:.1f}M")
    top10["Share"] = top10["Share"].apply(lambda x: f"{x:.1f}%")
    top10.columns = ["Estado", "Valor (USD)", "% Nacional"]
    top10 = top10.reset_index(drop=True)
    top10.index += 1
    st.dataframe(top10, use_container_width=True, height=380)

st.divider()

fig_bar = px.bar(
    df[df["Share"] > 0].nlargest(10, "Share"),
    x="Share", y="State", orientation="h",
    color="Share",
    color_continuous_scale=["#2A9D8F", "#F4A261", "#E63946"],
    labels={"Share": "% Participación", "State": "Estado"},
    title=f"Top 10 Estados por {flujo} de Carne — 2024"
)
fig_bar.update_layout(height=400, showlegend=False, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_bar, use_container_width=True)
