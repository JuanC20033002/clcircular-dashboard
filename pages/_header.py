import streamlit as st

# Encabezado con gradiente CL Circular
st.markdown("""
<style>
[data-testid="stAppViewContainer"] > .main .block-container {
    padding-top: 2rem;
}

.header-banner {
    background: linear-gradient(135deg, #8DC63F 0%, #3AACB8 50%, #1B6CA8 100%);
    padding: 1.5rem;
    border-radius: 0 0 2rem 2rem;
    margin: -1.5rem -1.5rem 2rem -1.5rem;
    text-align: center;
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>

<div class="header-banner">
    <h1 style="margin: 0; font-size: 2.5rem;">📊 CL Circular Dashboard</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.95;">
        Visibilidad en tiempo real de tu cadena logística
    </p>
</div>
""", unsafe_allow_html=True)
