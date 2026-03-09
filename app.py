import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="CL Circular | Dashboard",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── LOGO EN SIDEBAR ───────────────────────────────────────────────────────────
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
        background: linear-gradient(to right, rgba(13,31,78,0.80) 0%, rgba(13,31,78,0.20) 100%);
        border-radius: 0 0 1.5rem 1.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 2.2rem 2.5rem;
    }}
    .hero-title {{
        color: #FFFFFF;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
    }}
    .hero-subtitle {{
        color: #8DC63F;
        font-size: 1.05rem;
        margin-top: 0.4rem;
        font-weight: 500;
    }}
    </style>

    <div class="hero-banner">
      <div class="hero-overlay">
        <p class="hero-title">CL Circular — Dashboard Estratégico</p>
        <p class="hero-subtitle">
          Corredor Comercial México–Estados Unidos · Sector Cárnico
        </p>
      </div>
    </div>
    """, unsafe_allow_html=True)

header_con_foto()

# ── INTRODUCCIÓN ─────────────────────────────────────────────────────────────
st.markdown("### ¿Qué es CL Circular?")

st.markdown("""
**CL Circular** ofrece visibilidad en tiempo real del estado de los embarques en operaciones 
de importación y exportación mediante sensores IoT reutilizables.  
Este dashboard sirve como plataforma analítica para evaluar la **viabilidad de expansión** de CL Circular 
al corredor México–Estados Unidos en el sector cárnico y construir una **estrategia de entrada por fases**.
""")

st.divider()

# ── OBJETIVO DEL PROYECTO ────────────────────────────────────────────────────
st.markdown("### 🎯 Objetivo del estudio")

st.markdown("""
Evaluar, con base en datos, si existe una lógica económica y operativa para que CL Circular 
entre al mercado cárnico México–EE.UU., y proponer una estrategia de expansión que:
- Seleccione segmentos y corredores prioritarios.
- Cuantifique la oportunidad y los riesgos logísticos.
- Alinee el roadmap de sensores y el mensaje comercial de la empresa.
""")

st.divider()

# ── EQUIPO DEL PROYECTO ──────────────────────────────────────────────────────
st.markdown("### 👥 Equipo de proyecto")

col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("""
    **Integrantes**

    - Pablo Marin  
    - Luis Armando Domínguez  
    - Juan Cepeda  
    - Joaquin Cano  
    - Geraldine Dominguez  
    - David Balas  
    """)

with col2:
    st.markdown("""
    Este dashboard se elaboró como parte del reto con **CL Circular** y el 
    **Tecnológico de Monterrey**, integrando análisis de comercio exterior, 
    logística y riesgo climático para respaldar recomendaciones estratégicas.
    """)

st.divider()

# ── NAVEGACIÓN ───────────────────────────────────────────────────────────────
st.markdown("### 🗂️ ¿Qué puedes explorar en el dashboard?")

st.markdown("""
- 📈 **Serie de Tiempo** – Histórico y pronóstico del comercio cárnico bilateral.  
- 🗺️ **Participación por Estado** – Concentración geográfica de importaciones y exportaciones.  
- 🌡️ **Riesgo Climático** – Índice de riesgo térmico por zona y corredores fronterizos.  
- 🤝 **Socios Clave** – Empresas y actores logísticos prioritarios.  
- 🚀 **Estrategia de Expansión** – Hoja de ruta propuesta para la entrada de CL Circular.
""")

st.divider()
st.caption("Datos: DataMéxico · USDA · Trade Map · SMN | Marzo 2026")
