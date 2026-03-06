import streamlit as st
import base64
from pathlib import Path

def header_con_foto():
    img_path = Path("assets/hero.jpeg")
    if not img_path.exists():
        st.warning("No encuentro la imagen del header en assets/hero.jpeg")
        return

    img_bytes = img_path.read_bytes()
    img_base64 = base64.b64encode(img_bytes).decode()

    st.markdown(f"""
    <style>
    .hero-banner {{
        position: relative;
        margin: -1.5rem -1.5rem 2rem -1.5rem;
        height: 260px;
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        border-radius: 0 0 2rem 2rem;
        overflow: hidden;
    }}
    .hero-overlay {{
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, rgba(13,31,78,0.7), rgba(0,0,0,0.05));
    }}
    .hero-content {{
        position: relative;
        z-index: 1;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-left: 3rem;
        color: #FFFFFF;
    }}
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
