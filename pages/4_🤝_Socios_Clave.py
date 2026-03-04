import streamlit as st

st.set_page_config(page_title="Socios Clave | CL Circular", layout="wide")

st.title("🤝 Socios & Empresas Clave")
st.markdown("Actores estratégicos del corredor México–EE.UU. que representan oportunidades comerciales para CL Circular.")
st.divider()

# Datos de empresas
empresas = [
    {"nombre": "Cargill Food, S.A. de C.V.", "tipo": "Importador/Exportador", "pais": "🇲🇽 México", "categoria": "Procesador Cárnico", "relevancia": "Alta"},
    {"nombre": "Sigma Foodservice Comercial", "tipo": "Importador", "pais": "🇲🇽 México", "categoria": "Procesador Cárnico", "relevancia": "Alta"},
    {"nombre": "Tyson México Trading Company", "tipo": "Importador", "pais": "🇲🇽 México", "categoria": "Procesador Cárnico", "relevancia": "Alta"},
    {"nombre": "Norson / Frigorífico Agropecuario Sonorense", "tipo": "Importador/Exportador", "pais": "🇲🇽 México", "categoria": "Productor Cárnico", "relevancia": "Alta"},
    {"nombre": "Adams International Morelia", "tipo": "Importador", "pais": "🇲🇽 México", "categoria": "Distribuidor", "relevancia": "Media"},
    {"nombre": "Alimentos SBF de México", "tipo": "Importador", "pais": "🇲🇽 México", "categoria": "Distribuidor", "relevancia": "Media"},
    {"nombre": "Empacadora de Carnes de Fresnillo", "tipo": "Importador/Exportador", "pais": "🇲🇽 México", "categoria": "Empacador", "relevancia": "Media"},
    {"nombre": "Nova Agrotrade", "tipo": "Importador/Exportador", "pais": "🇲🇽 México", "categoria": "Comercializador", "relevancia": "Media"},
    {"nombre": "Disbalca TGT", "tipo": "Importador/Exportador", "pais": "🇲🇽 México", "categoria": "Distribuidor", "relevancia": "Media"},
    {"nombre": "Cárnicos de Jerez", "tipo": "Exportador", "pais": "🇲🇽 México", "categoria": "Productor Cárnico", "relevancia": "Media"},
    {"nombre": "Comercializadora de Alimentos y Cárnicos Américas", "tipo": "Importador/Exportador", "pais": "🇲🇽 México", "categoria": "Comercializador", "relevancia": "Media"},
    {"nombre": "Carnes y Productos Avícolas de México", "tipo": "Importador/Exportador", "pais": "🇲🇽 México", "categoria": "Productor Cárnico", "relevancia": "Media"},
]

# Filtros
col1, col2 = st.columns(2)
with col1:
    cat_sel = st.multiselect(
        "Categoría:",
        options=list(set([e["categoria"] for e in empresas])),
        default=list(set([e["categoria"] for e in empresas]))
    )
with col2:
    rel_sel = st.multiselect(
        "Relevancia:",
        options=["Alta", "Media", "Baja"],
        default=["Alta", "Media"]
    )

empresas_f = [e for e in empresas if e["categoria"] in cat_sel and e["relevancia"] in rel_sel]

st.divider()

# Tarjetas
cols = st.columns(3)
for i, emp in enumerate(empresas_f):
    color = "#E63946" if emp["relevancia"] == "Alta" else "#F4A261"
    with cols[i % 3]:
        st.markdown(f"""
        <div style="border-left: 4px solid {color}; padding: 12px 16px; 
                    background-color: #161B22; border-radius: 6px; margin-bottom: 16px;">
            <h4 style="margin:0; color:#F0F6FC;">{emp['nombre']}</h4>
            <p style="margin:4px 0; color:#8B949E;">
                {emp['pais']} &nbsp;|&nbsp; {emp['categoria']}
            </p>
            <p style="margin:4px 0; color:#8B949E;">
                <b>Rol:</b> {emp['tipo']}
            </p>
            <span style="background-color:{color}; color:white; padding:2px 10px; 
                         border-radius:12px; font-size:12px;">
                Relevancia {emp['relevancia']}
            </span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Actores logísticos
st.markdown("### 🚛 Actores Logísticos Clave")
st.markdown("Puntos de entrada y operadores que CL Circular debe integrar en su red:")

l1, l2 = st.columns(2)
with l1:
    st.markdown("""
    **🛣️ Cruces Fronterizos Terrestres**
    - Laredo / Nuevo Laredo — >40% del comercio terrestre
    - Tijuana / Otay Mesa — Mayor tráfico de personas y carga BC
    - Ciudad Juárez / El Paso — Estratégico para ganado en pie
    - Reynosa / McAllen — Alternativa confiable al norte
    """)
with l2:
    st.markdown("""
    **⚓ Puertos Marítimos Clave**
    - Manzanillo — Principal entrada carne congelada centro MX
    - Lázaro Cárdenas — Alternativa Pacífico, buques post-panamax
    - Veracruz — Carne europea y sudamericana
    - Altamira — Conexión directa con Monterrey y noreste
    - Ensenada — Complementario a cruce Otay Mesa
    """)

st.divider()
st.markdown("### 🏛️ Organismos Reguladores")
r1, r2 = st.columns(2)
with r1:
    st.info("🇲🇽 **SENASICA** — Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria. Regula inspecciones en frontera del lado mexicano.")
with r2:
    st.info("🇺🇸 **APHIS (USDA)** — Animal and Plant Health Inspection Service. Controla las inspecciones sanitarias del lado estadounidense.")
