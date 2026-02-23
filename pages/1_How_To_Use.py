# =============================================================================
# 1_How_To_Use.py — How To Use Page
# Describes the project, objective and step by step usage guide
# =============================================================================

import streamlit as st

st.set_page_config(
    page_title="How To Use — WhatsApp Analyzer Pro",
    page_icon="📖",
    layout="wide"
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Top nav
st.markdown("""
    <div style="
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 10000;
        background: #0D1117;
        border-bottom: 1px solid #21262D;
        padding: 0 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 44px;
    ">
        <div style="color:#25D366; font-weight:800; font-size:1rem;">
            💬 WhatsApp Analyzer Pro
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
            <a href="/How_To_Use" target="_self" style="
                color:#25D366; text-decoration:none; font-size:0.85rem;
                padding:6px 16px; border-radius:6px;
                border:1px solid #25D366;">
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


# ------------------------------------------------------------------ #
#  Hero Section                                                        #
# ------------------------------------------------------------------ #
st.markdown("""
    <div style="text-align:center; padding:40px 20px 20px 20px;">
        <h1 style="color:#25D366; font-size:2.2rem; font-weight:800;">
            📖 How To Use WhatsApp Analyzer Pro
        </h1>
        <p style="color:#8B949E; font-size:1rem; max-width:700px;
                  margin:0 auto; line-height:1.8;">
            A complete guide to understanding the project,
            its objectives and how to get the most out of every feature.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  Helper Functions                                                    #
# ------------------------------------------------------------------ #

def section_header(title: str):
    st.markdown(
        f"<h2 style='color:#25D366; font-size:1.3rem; "
        f"font-weight:700; margin-bottom:4px;'>{title}</h2>"
        f"<hr style='border:1px solid #21262D; margin:6px 0 16px 0;'>",
        unsafe_allow_html=True
    )

def info_card(content: str):
    st.markdown(f"""
        <div style="
            background:#161B22;
            border:1px solid #21262D;
            border-left:3px solid #25D366;
            border-radius:0 8px 8px 0;
            padding:14px 18px;
            margin-bottom:12px;
            font-size:0.88rem;
            color:#8B949E;
            line-height:1.8;
        ">{content}</div>
    """, unsafe_allow_html=True)

def step_card(number: str, title: str, description: str):
    st.markdown(f"""
        <div style="
            background:#161B22;
            border:1px solid #21262D;
            border-radius:12px;
            padding:18px 20px;
            margin-bottom:12px;
            display:flex;
            gap:16px;
            align-items:flex-start;
        ">
            <div style="
                background:#25D366;
                color:#000000;
                font-weight:800;
                font-size:1rem;
                border-radius:50%;
                width:36px; height:36px;
                display:flex;
                align-items:center;
                justify-content:center;
                flex-shrink:0;
            ">{number}</div>
            <div>
                <div style="color:#FFFFFF; font-weight:700;
                            font-size:0.95rem; margin-bottom:4px;">
                    {title}</div>
                <div style="color:#8B949E; font-size:0.85rem;
                            line-height:1.7;">{description}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  About The Project                                                   #
# ------------------------------------------------------------------ #
section_header("🎯 About The Project")
info_card("""
    <b style="color:#FFFFFF;">WhatsApp Analyzer Pro</b> is an advanced data analytics and AI application
    built to transform raw WhatsApp chat exports into deep, meaningful insights.<br><br>
    Whether you want to understand communication patterns, track emotional dynamics,
    or even chat with an AI that mimics your contact's style —
    this tool does it all in one place.
""")

col1, col2, col3 = st.columns(3)

for col, icon, title, desc in zip(
    [col1, col2, col3],
    ["📊", "🧠", "🤖"],
    ["Deep Analytics", "Sentiment Analysis", "AI Chat Agent"],
    [
        "Uncover who talks the most, when the group is most active, what topics dominate and how people communicate.",
        "Track emotional tone across time, per user mood scores, and detect potentially toxic messages.",
        "Chat with an AI that has studied a person's writing style, vocabulary and emoji usage from real chat data."
    ]
):
    with col:
        st.markdown(f"""
            <div style="background:#161B22; border:1px solid #21262D;
                        border-radius:12px; padding:20px 16px;
                        text-align:center; height:160px;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="color:#25D366; font-weight:700;
                            margin:8px 0 6px 0;">{title}</div>
                <div style="color:#8B949E; font-size:0.82rem;
                            line-height:1.6;">{desc}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  Objective                                                           #
# ------------------------------------------------------------------ #
section_header("🏆 Project Objective")
info_card("""
    <b style="color:#FFFFFF;">Primary Goal:</b> Demonstrate advanced data science skills through
    real-world WhatsApp chat analysis — combining data processing, NLP,
    sentiment analysis and generative AI into a single polished application.<br><br>
    <b style="color:#25D366;">Key Objectives:</b><br>
    • Parse and process unstructured WhatsApp text data into structured insights<br>
    • Apply NLP techniques for sentiment scoring and mood tracking<br>
    • Build an LLM-powered agent that learns from real chat patterns<br>
    • Present findings through an interactive, visually appealing dashboard<br>
    • Deploy end-to-end using Docker, Kubernetes and Jenkins CI/CD pipeline
""")

st.markdown("<br>", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  How To Export WhatsApp Chat                                         #
# ------------------------------------------------------------------ #
section_header("📱 Step 1 — Export Your WhatsApp Chat")
info_card("""
    <b style="color:#FFFFFF;">How to export your chat from WhatsApp:</b><br><br>
    <b style="color:#25D366;">On Android:</b><br>
    1. Open the WhatsApp chat (individual or group)<br>
    2. Tap the three dots (⋮) in the top right<br>
    3. Select <b>More → Export Chat</b><br>
    4. Choose <b>Without Media</b><br>
    5. Save or share the .txt file to your device<br><br>
    <b style="color:#25D366;">On iPhone:</b><br>
    1. Open the WhatsApp chat<br>
    2. Tap the contact/group name at the top<br>
    3. Scroll down and tap <b>Export Chat</b><br>
    4. Choose <b>Without Media</b><br>
    5. Save the .txt file<br><br>
    <b style="color:#FF4B4B;">⚠️ Important:</b> Always choose
    <b>Without Media</b> — the app only needs the text file.
""")

st.markdown("<br>", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  Step By Step Usage Guide                                            #
# ------------------------------------------------------------------ #
section_header("🚀 Step By Step Usage Guide")

step_card("1", "Upload Your Chat File",
    "In the left sidebar, find the <b>📂 Upload Chat</b> section. "
    "Click the upload button and select your exported WhatsApp .txt file. "
    "The app supports both individual and group chat exports.")

step_card("2", "Click Analyze Chat",
    "After uploading, select a user from the <b>👤 Select User</b> dropdown "
    "— choose <b>Overall</b> for group-wide analysis or a specific person "
    "for individual insights. Then click the green <b>🔍 Analyze Chat</b> button.")

step_card("3", "Explore Analytics Dashboard",
    "The app will automatically navigate to the Analytics Dashboard. "
    "Here you will find Overview KPIs, Monthly and Daily Timelines, "
    "Activity Maps, Word Cloud, Emoji Analysis and Response Time insights. "
    "<b style='color:#25D366;'>You must visit this section first to unlock the AI Agent.</b>")

step_card("4", "Check Sentiment Analysis",
    "Switch to <b>🧠 Sentiment Analysis</b> in the sidebar navigation. "
    "View overall mood scores, sentiment trends over time, "
    "per-user emotional comparison and flagged toxic messages.")

step_card("5", "Set Up AI Chat Agent",
    "Switch to <b>🤖 AI Chat Agent</b> in the sidebar. "
    "Enter your free <b>Google Gemini API key</b> in the sidebar "
    "(get it free at aistudio.google.com). "
    "Select the Gemini model from the dropdown.")

step_card("6", "Start Chatting With AI Clone",
    "In the Agent section, use the two dropdowns to assign roles: "
    "<b>You are</b> (your role in the conversation) and "
    "<b>AI is</b> (who the AI will impersonate). "
    "The AI has studied this person's vocabulary, emoji usage, tone and "
    "writing style from the real chat data. Type a message and hit Send!")

st.markdown("<br>", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  Features Overview                                                   #
# ------------------------------------------------------------------ #
section_header("✨ Features Overview")

features = [
    ("📊", "Analytics Dashboard",
     "Total messages, words, media and links · Monthly and daily timelines · "
     "Activity heatmap · Most active users · Word cloud · Emoji analysis · "
     "Response time analysis · Conversation starters"),
    ("🧠", "Sentiment Analysis",
     "Per message VADER sentiment scoring · Overall mood score out of 10 · "
     "Monthly sentiment timeline · Sentiment heatmap by hour and day · "
     "Per user sentiment comparison · Toxic message detection"),
    ("🤖", "AI Chat Agent",
     "Dynamic personality extraction from real chat data · "
     "Two role conversation setup (you vs AI) · "
     "Hinglish aware LLM responses · "
     "Chat memory for multi-turn conversations · "
     "RPM and RPD usage counter with warnings"),
]

for icon, title, desc in features:
    st.markdown(f"""
        <div style="background:#161B22; border:1px solid #21262D;
                    border-radius:12px; padding:18px 20px;
                    margin-bottom:12px; display:flex; gap:16px;">
            <div style="font-size:2rem; flex-shrink:0;">{icon}</div>
            <div>
                <div style="color:#25D366; font-weight:700;
                            font-size:1rem; margin-bottom:6px;">
                    {title}</div>
                <div style="color:#8B949E; font-size:0.85rem;
                            line-height:1.8;">{desc}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  Tech Stack                                                          #
# ------------------------------------------------------------------ #
section_header("🛠️ Tech Stack")

col1, col2, col3, col4 = st.columns(4)

tech = [
    ("🎨", "Frontend", "Streamlit · Custom CSS · Plotly"),
    ("⚙️", "Backend",  "Python · Pandas · NLTK · VADER"),
    ("🤖", "AI/NLP",   "Google Gemini API · VADER Sentiment · WordCloud"),
    ("🐳", "DevOps",   "Docker · Kubernetes · Jenkins"),
]

for col, (icon, title, desc) in zip([col1, col2, col3, col4], tech):
    with col:
        st.markdown(f"""
            <div style="background:#161B22; border:1px solid #21262D;
                        border-radius:12px; padding:16px;
                        text-align:center;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="color:#25D366; font-weight:700;
                            margin:8px 0 4px 0;">{title}</div>
                <div style="color:#8B949E; font-size:0.8rem;
                            line-height:1.6;">{desc}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)