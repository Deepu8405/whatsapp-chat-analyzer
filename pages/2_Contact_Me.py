# =============================================================================
# 2_Contact_Me.py — Contact Me Page
# Redirects to portfolio website
# =============================================================================

import streamlit as st

st.set_page_config(
    page_title="Contact — WhatsApp Analyzer Pro",
    page_icon="🌐",
    layout="wide"
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Auto redirect to portfolio
st.markdown("""
    <script>
        window.open(
            'https://whimsical-conkies-ad5d60.netlify.app/',
            '_blank'
        );
    </script>
""", unsafe_allow_html=True)

# Top nav
st.markdown("""
    <div style="
        position:fixed; top:0; left:0; right:0;
        z-index:10000; background:#0D1117;
        border-bottom:1px solid #21262D;
        padding:0 24px; display:flex;
        align-items:center; justify-content:space-between;
        height:44px;
    ">
        <div style="color:#25D366; font-weight:800; font-size:1rem;">
            💬 WhatsApp Analyzer Pro
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
            <a href="/How_To_Use" target="_self" style="
                color:#8B949E; text-decoration:none; font-size:0.85rem;
                padding:6px 16px; border-radius:6px;
                border:1px solid #21262D;">
                📖 How To Use</a>
            <a href="https://whimsical-conkies-ad5d60.netlify.app/"
               target="_blank" style="
                color:#000000; background:#25D366;
                text-decoration:none; font-size:0.85rem;
                padding:6px 16px; border-radius:6px; font-weight:700;">
                🌐 Contact Me</a>
        </div>
    </div>
    <div style="height:44px;"></div>
""", unsafe_allow_html=True)


# Profile Card
st.markdown("""
    <div style="max-width:700px; margin:60px auto; text-align:center;">
        <div style="font-size:4rem; margin-bottom:16px;">👨‍💻</div>
        <h1 style="color:#25D366; font-size:1.8rem; font-weight:800;
                   margin-bottom:8px;">Deepu Kumar Rajak</h1>
        <p style="color:#8B949E; font-size:0.95rem; margin-bottom:4px;">
            Data Scientist & AI Enthusiast · IIT Kharagpur
        </p>
        <p style="color:#8B949E; font-size:0.88rem; line-height:1.8;
                  max-width:600px; margin:16px auto 32px auto;">
            I'm a dedicated Data Scientist with a strong foundation in
            machine learning, deep learning, and natural language processing.
            I combine technical expertise with creative problem-solving
            to deliver impactful AI solutions.
        </p>
        <a href="https://whimsical-conkies-ad5d60.netlify.app/"
           target="_blank" style="
            background:#25D366; color:#000000;
            text-decoration:none; font-weight:800;
            font-size:1rem; padding:14px 36px;
            border-radius:10px; display:inline-block;
            margin-bottom:32px;">
            🌐 Visit My Portfolio
        </a>
    </div>
""", unsafe_allow_html=True)

# Skills
st.markdown("""
    <div style="max-width:700px; margin:0 auto;">
        <div style="display:flex; flex-wrap:wrap; gap:10px;
                    justify-content:center; margin-bottom:32px;">
""", unsafe_allow_html=True)

skills = [
    "Machine Learning", "Deep Learning", "NLP",
    "Python", "Data Analytics", "Generative AI",
    "Computer Vision", "MLOps", "IIT Kharagpur"
]

skills_html = "".join([f"""
    <span style="background:#161B22; border:1px solid #25D366;
                 color:#25D366; padding:6px 14px; border-radius:20px;
                 font-size:0.82rem; font-weight:600;">{s}</span>
""" for s in skills])

st.markdown(f"""
    <div style="max-width:700px; margin:0 auto; text-align:center;">
        <div style="display:flex; flex-wrap:wrap; gap:10px;
                    justify-content:center; margin-bottom:32px;">
            {skills_html}
        </div>
    </div>
""", unsafe_allow_html=True)