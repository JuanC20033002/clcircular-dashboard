import streamlit as st
import base64
from pathlib import Path

# ── DEBE SER LO PRIMERO ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="CL Circular | Dashboard",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── LOGO EN SIDEBAR ──────────────────────────────────────────────────────────
logo_path = Path("assets/Logo-Cl-Circular.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

# ── HEADER CON FOTO ──────────────────────────────────────────────────────────
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
        height: 240px;
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        border-radius: 0 0 1.5rem 1.5rem;
        position: relative;
    }}
    .hero-overlay {{
        position: absolute;
        inset: 0;
        background: linear-gradient(to right, rgba(13,31,78,0.75) 0%, rgba(13,31,78,0.2) 100%);
        border-radius: 0 0 1.5rem 1.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 2rem 2.5rem;
    }}
    .hero-title {{
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.5);
    }}
    .hero-subtitle {{
        color: #8DC63F;
        font-size: 1.1rem;
        margin-top: 0.4rem;
        font-weight: 500;
    }}
    </style>

    <div class="hero-banner">
        <div class="hero-overlay">
            <p class="hero-title">CL Circular — Dashboard Estratégico</p>
            <p class="hero-subtitle">Corredor Comercial México–Estados Unidos | Sector Cárnico</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

header_con_foto()   # ← aquí se llama

# ── INTRODUCCIÓN ─────────────────────────────────────────────────────────────
st.markdown("""
### ¿Qué es CL Circular?
**CL Circular** ofrece visibilidad en tiempo real del estado de los embarques en operaciones 
de importación y exportación. Este dashboard analiza la viabilidad estratégica de introducir 
sus servicios en el corredor bilateral México–EE.UU. dentro del **sector cárnico**.
""")

st.divider()

# ── KPIs ─────────────────────────────────────────────────────────────────────
st.markdown("### 📊 El Mercado en Números")
k1, k2, k3, k4 = st.columns(4)

k1.metric(label="Volumen Anual",       value="2.3M ton",       delta="métricas en ambas direcciones")
k2.metric(label="Valor del Corredor",  value="$5B+ USD",       delta="exportaciones + importaciones")
k3.metric(label="Cruces Fronterizos",  value="4 principales",  delta="Laredo, Tijuana, Juárez, Reynosa")
k4.metric(label="Empresas Potenciales",value="17 identificadas",delta="importadores y exportadores")

st.divider()

# ── NAVEGACIÓN ───────────────────────────────────────────────────────────────
st.markdown("### 🗂️ Secciones del Dashboard")
st.markdown("""
Usa el **menú lateral izquierdo** para navegar entre secciones:

- 📈 **Serie de Tiempo** — Histórico y pronóstico Prophet del comercio bilateral
- 🗺️ **Participación por Estado** — Mapa de importaciones y exportaciones por entidad
- 🌡️ **Riesgo Climático** — Índice de riesgo térmico por zona y mes
- 🤝 **Socios Clave** — Empresas y actores logísticos prioritarios
""")

st.divider()
st.caption("Datos: DataMéxico · USDA · Trade Map · SMN | Marzo 2026")
