import streamlit as st
import base64
from pathlib import Path

def header_con_foto():
    img_path = Path("assets/hero.jpeg")
    if not img_path.exists():
        st.warning(f"No encuentro la imagen en {img_path}")
        return

    img_bytes = img_path.read_bytes()
    img_base64 = base64.b64encode(img_bytes).decode()

    st.markdown(f"""
    <style>
    .hero-banner {{
        margin: -1rem -1rem 2rem -1rem;
        height: 220px;
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        border-radius: 0 0 1.5rem 1.5rem;
    }}
    </style>

    <div class="hero-banner"></div>
    """, unsafe_allow_html=True)

import streamlit as st

st.set_page_config(
    page_title="CL Circular | Dashboard",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header principal
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🔴 CL Circular — Dashboard Estratégico")
    st.subheader("Corredor Comercial México–Estados Unidos | Sector Cárnico")

st.divider()

# Introducción
st.markdown("""
### ¿Qué es CL Circular?
**CL Circular** ofrece visibilidad en tiempo real del estado de los embarques en operaciones 
de importación y exportación. Este dashboard analiza la viabilidad estratégica de introducir 
sus servicios en el corredor bilateral México–EE.UU. dentro del **sector cárnico**.
""")

st.divider()

# KPIs Hero
st.markdown("### 📊 El Mercado en Números")
k1, k2, k3, k4 = st.columns(4)

k1.metric(label="Volumen Anual", value="2.3M ton", delta="métricas en ambas direcciones")
k2.metric(label="Valor del Corredor", value="$5B+ USD", delta="exportaciones + importaciones")
k3.metric(label="Cruces Fronterizos", value="4 principales", delta="Laredo, Tijuana, Juárez, Reynosa")
k4.metric(label="Empresas Potenciales", value="17 identificadas", delta="importadores y exportadores")

st.divider()

# Navegación
st.markdown("### 🗂️ Secciones del Dashboard")
st.markdown("""
Usa el **menú lateral izquierdo** para navegar entre secciones:

- 📈 **Serie de Tiempo** — Histórico y pronóstico ARIMA del comercio bilateral
- 🗺️ **Participación por Estado** — Mapa de importaciones y exportaciones por entidad
- 🌡️ **Riesgo Climático** — Índice de riesgo térmico por zona y mes
- 🤝 **Socios Clave** — Empresas y actores logísticos prioritarios
""")

st.divider()
st.caption("Datos: INEGI · Banco de México · USDA · Trade Map · SMN | Marzo 2026")
