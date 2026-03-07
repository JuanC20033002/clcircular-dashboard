import streamlit as st
from utils.helpers import (
    CL_VERDE, CL_VERDE_OSCURO, CL_AZUL, CL_AZUL_MARINO, CL_CYAN,
    COLORES_RIESGO
)

st.set_page_config(page_title="Socios Clave | CL Circular", layout="wide")

# ── LOGO EN SIDEBAR ───────────────────────────────────────────────────────────
from pathlib import Path
logo_path = Path("assets/Logo-Cl-Circular.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

st.title("🤝 Socios & Empresas Clave")
st.markdown("Actores estratégicos del corredor México–EE.UU. que representan oportunidades comerciales para CL Circular.")
st.divider()

# ── DATOS DE EMPRESAS ─────────────────────────────────────────────────────────
empresas = [
    {"nombre": "Cargill Food, S.A. de C.V.",                        "tipo": "Importador/Exportador", "ciudad": "Saltillo",     "categoria": "Procesador Cárnico",  "relevancia": "Alta"},
    {"nombre": "Sigma Foodservice Comercial",                        "tipo": "Importador",            "ciudad": "Varias",       "categoria": "Procesador Cárnico",  "relevancia": "Alta"},
    {"nombre": "Tyson México Trading Company",                       "tipo": "Importador",            "ciudad": "Varias",       "categoria": "Procesador Cárnico",  "relevancia": "Alta"},
    {"nombre": "Norson / Frigorífico Agropecuario Sonorense",        "tipo": "Importador/Exportador", "ciudad": "Hermosillo",   "categoria": "Productor Cárnico",   "relevancia": "Alta"},
    {"nombre": "Adams International S.A. de C.V.",                   "tipo": "Importador/Exportador", "ciudad": "Guadalajara",  "categoria": "Distribuidor",        "relevancia": "Media"},
    {"nombre": "Alimentos SBF de México",                            "tipo": "Importador",            "ciudad": "Reynosa",      "categoria": "Distribuidor",        "relevancia": "Media"},
    {"nombre": "Empacadora de Carnes de Fresnillo",                  "tipo": "Importador/Exportador", "ciudad": "Fresnillo",    "categoria": "Empacador",           "relevancia": "Media"},
    {"nombre": "Nova Agrotrade",                                     "tipo": "Importador/Exportador", "ciudad": "Culiacán",     "categoria": "Comercializador",     "relevancia": "Media"},
    {"nombre": "Cárnicos de Jerez",                                  "tipo": "Exportador",            "ciudad": "Jerez",        "categoria": "Productor Cárnico",   "relevancia": "Media"},
    {"nombre": "Comercializadora de Alimentos y Cárnicos Américas",  "tipo": "Importador/Exportador", "ciudad": "Monterrey",    "categoria": "Comercializador",     "relevancia": "Media"},
    {"nombre": "Carnes y Productos Avícolas de México",              "tipo": "Importador/Exportador", "ciudad": "Querétaro",    "categoria": "Productor Cárnico",   "relevancia": "Media"},
    {"nombre": "Comercial Targa",                                    "tipo": "Importador",            "ciudad": "Tijuana",      "categoria": "Distribuidor",        "relevancia": "Baja"},
    {"nombre": "Cargill Protein",                                    "tipo": "Importador/Exportador", "ciudad": "CDMX",         "categoria": "Procesador Cárnico",  "relevancia": "Baja"},
]

# ── FILTROS ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    cat_sel = st.multiselect(
        "Categoría:",
        options=sorted(set(e["categoria"] for e in empresas)),
        default=sorted(set(e["categoria"] for e in empresas))
    )
with col2:
    rel_sel = st.multiselect(
        "Relevancia:",
        options=["Alta", "Media", "Baja"],
        default=["Alta", "Media"]
    )

empresas_f = [e for e in empresas if e["categoria"] in cat_sel and e["relevancia"] in rel_sel]

st.markdown(f"**{len(empresas_f)} empresas** encontradas con los filtros seleccionados.")
st.divider()

# ── TARJETAS ──────────────────────────────────────────────────────────────────
# Color del borde y badge según relevancia (paleta CL Circular, fondo blanco)
COLOR_MAP = {
    "Alta":  {"borde": CL_VERDE,       "badge_bg": CL_VERDE,       "badge_txt": "#FFFFFF"},
    "Media": {"borde": CL_CYAN,        "badge_bg": CL_CYAN,        "badge_txt": "#FFFFFF"},
    "Baja":  {"borde": "#E63946",      "badge_bg": "#E63946",      "badge_txt": "#FFFFFF"},
}

cols = st.columns(3)
for i, emp in enumerate(empresas_f):
    c = COLOR_MAP[emp["relevancia"]]
    with cols[i % 3]:
        st.markdown(f"""
        <div style="
            border-left: 4px solid {c['borde']};
            padding: 14px 18px;
            background-color: #F8FAFC;
            border-radius: 6px;
            margin-bottom: 16px;
            box-shadow: 0 1px 4px rgba(13,31,78,0.08);
        ">
            <h4 style="margin:0 0 4px 0; color:{CL_AZUL_MARINO}; font-size:0.95rem;">
                {emp['nombre']}
            </h4>
            <p style="margin:2px 0; color:#555; font-size:0.85rem;">
                📍 {emp['ciudad']} &nbsp;|&nbsp; {emp['categoria']}
            </p>
            <p style="margin:2px 0; color:#555; font-size:0.85rem;">
                <b>Rol:</b> {emp['tipo']}
            </p>
            <span style="
                background-color:{c['badge_bg']};
                color:{c['badge_txt']};
                padding:2px 10px;
                border-radius:12px;
                font-size:11px;
                font-weight:600;
            ">● Relevancia {emp['relevancia']}</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── ACTORES LOGÍSTICOS ────────────────────────────────────────────────────────
st.markdown("### 🚛 Actores Logísticos Clave")
st.markdown("Puntos de entrada y operadores que CL Circular debe integrar en su red:")

l1, l2 = st.columns(2)
with l1:
    st.markdown(f"""
    <div style="background:#F0F7FF; border-radius:10px; padding:16px; border-top:3px solid {CL_AZUL};">
    <b style="color:{CL_AZUL_MARINO};">🛣️ Cruces Fronterizos Terrestres</b><br><br>
    🔵 <b>Laredo / Nuevo Laredo</b> — +3M camiones/año, ~50% tráfico total<br>
    🔵 <b>Ciudad Juárez / El Paso</b> — Ganado en pie, nearshoring agropecuario<br>
    🔵 <b>Nogales / Nogales</b> — Pollo 19,927 MT · Cerdo 14,798 MT · Res 7,108 MT<br>
    🔵 <b>Reynosa / McAllen</b> — Acceso rápido a Houston y Dallas<br>
    </div>
    """, unsafe_allow_html=True)
with l2:
    st.markdown(f"""
    <div style="background:#F0FFF4; border-radius:10px; padding:16px; border-top:3px solid {CL_VERDE};">
    <b style="color:{CL_AZUL_MARINO};">⚓ Puertos Marítimos Clave</b><br><br>
    🟢 <b>Manzanillo</b> — Principal entrada carne congelada centro MX<br>
    🟢 <b>Lázaro Cárdenas</b> — Alternativa Pacífico, buques post-panamax<br>
    🟢 <b>Veracruz</b> — Carne europea y sudamericana<br>
    🟢 <b>Altamira</b> — Conexión directa Monterrey y noreste<br>
    🟢 <b>Ensenada</b> — Complementario a cruce Otay Mesa<br>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── ORGANISMOS REGULADORES ────────────────────────────────────────────────────
st.markdown("### 🏛️ Organismos Reguladores Binacionales")
r1, r2 = st.columns(2)
with r1:
    st.markdown(f"""
    <div style="background:#EEF4FF; border-radius:10px; padding:16px; border-left:4px solid {CL_AZUL};">
    🇲🇽 <b style="color:{CL_AZUL_MARINO};">SENASICA</b><br>
    <span style="color:#444; font-size:0.9rem;">
    Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria. 
    Regula inspecciones en frontera del lado mexicano.
    </span>
    </div>
    """, unsafe_allow_html=True)
with r2:
    st.markdown(f"""
    <div style="background:#EEF4FF; border-radius:10px; padding:16px; border-left:4px solid {CL_CYAN};">
    🇺🇸 <b style="color:{CL_AZUL_MARINO};">APHIS (USDA)</b><br>
    <span style="color:#444; font-size:0.9rem;">
    Animal and Plant Health Inspection Service. 
    Controla las inspecciones sanitarias del lado estadounidense.
    </span>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("Fuente: Trade Map, ITC · USDA APHIS · SENASICA · Control Terrestre | Marzo 2026")
