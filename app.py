import streamlit as st

st.markdown("""
<style>
.hero-banner {
    position: relative;
    margin: -1.5rem -1.5rem 2rem -1.5rem;
    height: 260px;
    background-image: url("https://blog.naturlider.com/celebra-el-dia-mundial-de-la-naturaleza-llevando-una-vida-sostenible/");
    background-size: cover;
    background-position: center;
    border-radius: 0 0 2rem 2rem;
    overflow: hidden;
}
.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(13,31,78,0.75), rgba(0,0,0,0.15));
}
.hero-content {
    position: relative;
    z-index: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 3rem;
    color: #FFFFFF;
}
</style>

<div class="hero-banner">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <h1 style="margin:0;font-size:2.4rem;">CL Circular Dashboard</h1>
    <p style="margin-top:0.4rem;font-size:1.1rem;max-width:420px;">
      Del sensor al dato, del dato a la acción.
    </p>
  </div>
</div>
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
