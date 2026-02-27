import streamlit as st
from google import genai
import plotly.express as px
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="NicBot", page_icon="🤖", layout="wide")

# 2. Theme State
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# 3. High-Contrast CSS
if st.session_state.theme == "dark":
    bg_color, text_color, card_bg = "#0d1117", "#FFFFFF", "#1c2128"
    card_border, sidebar_bg, accent = "#444c56", "#161b22", "#58a6ff"
else:
    bg_color, text_color, card_bg = "#ffffff", "#1f2328", "#f6f8fa"
    card_border, sidebar_bg, accent = "#d0d7de", "#f3f4f6", "#0969da"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Inter', sans-serif; transition: all 0.3s ease; }}
    [data-testid="stChatMessageContainer"] {{ padding-left: 10% !important; padding-right: 10% !important; max-width: 1100px; margin: 0 auto; }}
    .stChatMessage {{ background-color: {card_bg} !important; border: 1px solid {card_border} !important; border-radius: 12px !important; padding: 24px !important; margin-bottom: 25px !important; }}
    .stChatMessage p, .stChatMessage li, .stChatMessage span {{ color: {text_color} !important; font-size: 1.05rem !important; line-height: 1.6 !important; }}
    [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {card_border}; }}
    .thinking-bubble {{ border: 2px solid {accent}; background: {card_bg}; border-radius: 10px; padding: 12px 24px; color: {accent}; font-weight: bold; width: fit-content; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.6; }} }}
    div.stButton > button {{ border-radius: 10px !important; font-weight: 600 !important; width: 100% !important; }}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")
    st.title("NicBot v3.0")
    st.button("☀️ Light Mode" if st.session_state.theme == "dark" else "🌙 Dark Mode", on_click=toggle_theme)
    st.write("---")
    st.subheader("🎯 Recruiter Tools")
    recruiter_mode = st.toggle("Enable Recruiter Insights")
    if st.button("✨ Generate Exec Summary"):
        st.session_state.summary_trigger = True
    st.write("---")
    st.caption("2026 Edition | Generative UI Enabled")

# 5. Client & Context
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
try:
    with open("bio.txt", "r") as f:
        context = f.read()
except FileNotFoundError:
    context = "Professional context unavailable."

# 6. Chat Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Input Handling
prompt = st.chat_input("Ask Nicholas anything...")

if st.session_state.get("summary_trigger"):
    st.session_state.summary_trigger = False
    prompt = "Generate a 3-bullet executive summary for a hiring manager."
    st.session_state.messages.append({"role": "user", "content": "*(System Request)* Generate Executive Summary"})

if prompt:
    if not prompt.startswith("Generate a 3-bullet"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    with st.chat_message("assistant"):
        think = st.empty()
        think.markdown(f'<div class="thinking-bubble">Synthesizing strategic data...</div>', unsafe_allow_html=True)
        
        persona = "You are NicBot. CRITICAL: Never name specific customers. Use industry descriptors."
        if recruiter_mode:
            persona += " Focus on ROI, revenue impact, and leadership scaling."
            
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Updated to latest stable
            contents=prompt,
            config={'system_instruction': f"{persona} Context: {context}"}
        )
        
        think.empty()
        full_text = response.text
        st.markdown(full_text)
        st.session_state.messages.append({"role": "assistant", "content": full_text})

        # --- GENERATIVE UI COMPONENTS ---

        # A. Technical Skill Radar Chart
        if any(word in prompt.lower() for word in ["skill", "expertise", "technical", "competency"]):
            st.write("---")
            st.caption("⚡ Technical Proficiency Radar")
            df = pd.DataFrame(dict(
                r=[95, 90, 85, 92, 88],
                theta=['Threat Intel (GCTI)', 'Strategic Advocacy', 'AI/LLM Workflows', 'Cyber Ops', 'Product Vision']
            ))
            fig = px.line_polar(df, r='r', theta='theta', line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color=accent)
            fig.update_layout(
                polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False)),
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=text_color,
                margin=dict(l=20, r=20, t=20, b=20),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

        # B. Product Milestone Cards
        if any(word in prompt.lower() for word in ["calendar", "product", "project"]):
            st.write("---")
            st.caption("🛠️ Product Roadmap: Living Family Calendar")
            c1, c2, c3 = st.columns(3)
            c1.metric("Status", "Prototyping")
            c2.metric("Concept", "Ambient UI")
            c3.metric("Goal", "Launch Q4")

        # C. Strategic Roadmap Table
        if any(word in prompt.lower() for word in ["timeline", "roadmap", "plan"]):
            st.write("---")
            st.caption("📅 Engagement Lifecycle Roadmap")
            st.table({
                "Phase": ["Discovery", "Architecture Review", "Optimization", "Principal Advisory"],
                "Focus": ["Gap Analysis", "Maturity Mapping", "Risk Mitigation", "Strategic Value"]
            })
