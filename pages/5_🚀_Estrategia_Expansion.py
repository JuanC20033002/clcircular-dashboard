import streamlit as st
from pathlib import Path
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import CL_AZUL_MARINO, CL_AZUL, CL_VERDE, CL_CYAN

st.set_page_config(page_title="Estrategia de Expansión | CL Circular", layout="wide")

# ── LOGO EN SIDEBAR ───────────────────────────────────────────────────────────
logo_path = Path("assets/Logo-Cl-Circular.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

# ── HERO ESTRATEGIA ───────────────────────────────────────────────────────────
st.markdown(f"""
<h1 style="color:{CL_AZUL_MARINO};margin-bottom:0.2rem;">
🚀 Estrategia de Expansión para CL Circular
</h1>
<p style="color:#425466;margin-top:0;">
De la consolidación en su mercado actual a la entrada ordenada al corredor cárnico México–Estados Unidos.
</p>
""", unsafe_allow_html=True)

st.divider()

# ── BLOQUE 1: ROADMAP EN DOS FASES ───────────────────────────────────────────
st.markdown("### 🧭 Roadmap en 2 fases")

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div style="
        background:#F8FAFC;
        border-left:4px solid {CL_AZUL};
        border-radius:10px;
        padding:14px 16px;
        height:100%;
    ">
        <p style="font-size:0.8rem;color:#64748B;margin:0 0 4px 0;">0–2 años</p>
        <h4 style="margin:0 0 6px 0;color:{CL_AZUL_MARINO};">
            Fase 1 — Consolidar mercado actual
        </h4>
        <p style="font-size:0.86rem;color:#475569;margin:0 0 6px 0;">
            Antes de entrar de forma agresiva a México, CL Circular fortalece su 
            presencia en su mercado principal y aumenta su base de clientes.
        </p>
        <ul style="padding-left:1.1rem;font-size:0.86rem;color:#475569;margin:0;">
            <li>Incrementar MRR y flujo de caja para financiar expansión.</li>
            <li>Escalar base instalada de sensores y madurar el producto.</li>
            <li>Documentar casos de uso y aprendizajes operativos.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="
        background:#F0FFF4;
        border-left:4px solid {CL_VERDE};
        border-radius:10px;
        padding:14px 16px;
        height:100%;
    ">
        <p style="font-size:0.8rem;color:#64748B;margin:0 0 4px 0;">3–5 años</p>
        <h4 style="margin:0 0 6px 0;color:{CL_AZUL_MARINO};">
            Fase 2 — Entrada al corredor cárnico MX–EE.UU.
        </h4>
        <p style="font-size:0.86rem;color:#475569;margin:0 0 6px 0;">
            Con mayor capital, equipo y sensores, CL Circular entra al corredor
            fronterizo enfocándose en el sector cárnico.
        </p>
        <ul style="padding-left:1.1rem;font-size:0.86rem;color:#475569;margin:0;">
            <li>Lanzar pilotos en rutas cárnicas de alto volumen.</li>
            <li>Concretar al menos 3 contratos activos en 12 meses.</li>
            <li>Escalar presencia en cruces estratégicos de la frontera.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── BLOQUE 2: OPORTUNIDAD EN CARNE RES / CERDO ───────────────────────────────
st.markdown("### 🥩 Oportunidad en carne de res y cerdo")

k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Res (exportación MX→EE.UU.)", "300k ton", "+10% vs año previo")
with k2:
    st.metric("Cerdo (importación EE.UU.→MX)", "1.15M ton", "+5% volumen")
with k3:
    st.metric("Relevancia sector cárnico", "Top flujo agro MX–USA", None)

st.markdown("""
El comercio de carne de **res** (exportaciones mexicanas) y **cerdo** (importaciones desde Estados Unidos) 
forma uno de los flujos logísticos más relevantes del corredor, con cadenas de frío altamente sensibles.
""")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    **🔒 Control de calidad**

    - Sensores permiten monitoreo de temperatura continuo.
    - Producto debe cumplir con decenas de requisitos regulatorios sanitarios.
    """)
with c2:
    st.markdown("""
    **🛡️ Reducción de pérdidas**

    - Alerta temprana vía conectividad 5G ante desviaciones térmicas.
    - Reduce rechazos por sanidad y mermas de producto.
    """)
with c3:
    st.markdown("""
    **📂 Trazabilidad y evidencia**

    - Reportes históricos respaldan auditorías y reclamos.
    - Prueba documental de cumplimiento de cadena de frío.
    """)

st.divider()

# ── BLOQUE 3: NUEVO LAREDO COMO PLAZA ANCLA ──────────────────────────────────
st.markdown("### 📍 Nuevo Laredo como punto de anclaje")

st.markdown(f"""
<div style="
    background:#F8FAFC;
    border-radius:10px;
    padding:14px 18px;
    border-left:4px solid {CL_AZUL_MARINO};
">
<p style="font-size:0.9rem;color:#475569;margin:0 0 6px 0;">
Nuevo Laredo concentra una porción crítica del tráfico de camiones entre México y Estados Unidos 
y es el principal corredor para embarques cárnicos hacia destinos como Monterrey y Ciudad de México.
</p>
<ul style="padding-left:1.1rem;font-size:0.88rem;color:#475569;margin:0;">
    <li>Alta densidad de clientes potenciales del sector cárnico y logístico.</li>
    <li>Recuperación física de sensores simplificada en comparación con otras plazas.</li>
    <li>Reducción de tiempos logísticos por sensor y mayor rotación de activos.</li>
    <li>Posibilidad de construir relaciones con freight forwarders y operadores locales.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── BLOQUE 4: ESTRATEGIA DE SENSORES ─────────────────────────────────────────
st.markdown("### 📡 Optimización del ciclo de sensores")

st.markdown("""
El principal cuello de botella actual es el envío de sensores de regreso a Europa para 
su restablecimiento o calibración. Se proponen dos líneas de acción complementarias:
""")

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div style="
        background:#F0FFF4;
        border-radius:10px;
        padding:14px 16px;
        border-top:3px solid {CL_VERDE};
        height:100%;
    ">
        <h4 style="margin:0 0 6px 0;color:{CL_AZUL_MARINO};font-size:0.98rem;">
            Solución 1 — Restablecimiento remoto
        </h4>
        <p style="font-size:0.86rem;color:#475569;margin:0 0 6px 0;">
            Desarrollar la capacidad de reinicio y calibración remota de sensores
            sin necesidad de regresarlos a España.
        </p>
        <ul style="padding-left:1.1rem;font-size:0.86rem;color:#475569;margin:0;">
            <li>Reduce costos logísticos internacionales.</li>
            <li>Minimiza tiempos muertos por sensor.</li>
            <li>Facilita escalar operaciones en México y EE.UU.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="
        background:#FFF7ED;
        border-radius:10px;
        padding:14px 16px;
        border-top:3px solid #F97316;
        height:100%;
    ">
        <h4 style="margin:0 0 6px 0;color:{CL_AZUL_MARINO};font-size:0.98rem;">
            Solución 2 — Centro regional en Tamaulipas
        </h4>
        <p style="font-size:0.86rem;color:#475569;margin:0 0 6px 0;">
            Si la opción remota no es viable de inmediato, establecer un centro
            de restablecimiento en México (Tamaulipas) cercano a Nuevo Laredo.
        </p>
        <ul style="padding-left:1.1rem;font-size:0.86rem;color:#475569;margin:0;">
            <li>Revisión y diagnóstico del estado de cada sensor.</li>
            <li>Recalibración y pruebas de funcionamiento.</li>
            <li>Preparación para su siguiente ciclo de uso.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── BLOQUE 5: SEGMENTOS Y PROPUESTA COMERCIAL ────────────────────────────────
st.markdown("### 🧩 Segmentos objetivo y mensaje comercial")

st.markdown("""
En lugar de liderar con sostenibilidad, la entrada al corredor cárnico debe anclar el 
mensaje en **beneficios económicos** y **decisiones basadas en datos**, usando la sostenibilidad como plus.
""")

st.markdown("""
| Segmento | Necesidad principal | Propuesta de valor CL Circular | Gancho comercial recomendado |
|---|---|---|---|
| Empresas cárnicas (importadoras/exportadoras) | Proteger cadena de frío, evitar rechazos y mermas | Sensores reutilizables con monitoreo continuo y evidencia para auditorías | **Ahorro por reducción de pérdidas** y menor riesgo de rechazo sanitario |
| Freight forwarders medianos/pequeños (refrigerado) | Diferenciarse frente a grandes operadores, ofrecer más valor a sus clientes | Plataforma de visibilidad que pueden revender como servicio agregado | **Nuevo ingreso por servicio premium** sin invertir en tecnología propia |
""")

st.markdown(f"""
<div style="
    background:#F8FAFC;
    border-radius:10px;
    padding:14px 18px;
    border-left:4px solid {CL_CYAN};
">
<p style="font-size:0.9rem;color:#475569;margin:0;">
<b>Giro del mensaje:</b> de “somos la opción más sostenible” a 
“te ayudamos a <b>reducir pérdidas, ahorrar en sensores desechables</b> y 
tomar <b>mejores decisiones logísticas con tus propios datos</b>, 
con sostenibilidad como beneficio adicional natural del modelo reutilizable.”
</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── BLOQUE 6: CIERRE ACCIONABLE ───────────────────────────────────────────────
st.markdown("### ✅ Próximos pasos recomendados")

st.markdown("""
- **0–2 años:** consolidar mercado actual y fortalecer finanzas antes de expansión agresiva.  
- **3–5 años:** lanzar pilotos en Nuevo Laredo con empresas cárnicas y forwarders medianos, buscando al menos 3 contratos activos.  
- **En paralelo:** definir estrategia de restablecimiento de sensores (remoto o centro regional) y alinear mensaje comercial a ahorro económico y analítica de datos.
""")

st.caption("Esta página resume cómo conectar los hallazgos analíticos del dashboard con una hoja de ruta accionable para CL Circular en el corredor cárnico México–Estados Unidos.")
