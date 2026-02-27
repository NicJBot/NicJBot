import streamlit as st
from google import genai

# 1. Page Config
st.set_page_config(page_title="NicBot", page_icon="🤖", layout="wide")

# 2. Theme State Initialization
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# 3. Dynamic CSS Injection
if st.session_state.theme == "dark":
    # --- DARK MODE (Deep Slate) ---
    bg_color = "#0d1117"
    text_color = "#f0f6fc"
    card_bg = "rgba(255, 255, 255, 0.07)"
    card_border = "rgba(255, 255, 255, 0.15)"
    sidebar_bg = "#161b22"
    accent = "#58a6ff"
else:
    # --- LIGHT MODE (Professional Clean) ---
    bg_color = "#ffffff"
    text_color = "#1f2328"
    card_bg = "#f6f8fa"
    card_border = "#d0d7de"
    sidebar_bg = "#f3f4f6"
    accent = "#0969da"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        font-family: 'Inter', -apple-system, sans-serif;
        transition: all 0.3s ease;
    }}
    
    /* Layout Spacing */
    [data-testid="stChatMessageContainer"] {{
        padding-left: 12% !important;
        padding-right: 12% !important;
        max-width: 1200px;
        margin: 0 auto;
    }}

    /* Message Bubble Refinement */
    .stChatMessage {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {card_border};
    }}

    /* Pulse Thinking Animation */
    .thinking-bubble {{
        border: 1.5px solid {accent};
        background: {card_bg};
        border-radius: 12px;
        padding: 12px 24px;
        color: {accent};
        font-weight: 600;
        width: fit-content;
        animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
        0% {{ opacity: 0.5; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.5; }}
    }}

    /* Interaction Elements */
    div.stButton > button {{
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar Tools
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")
    st.title("NicBot v3.0")
    
    # Theme Toggle
    theme_label = "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode"
    st.button(theme_label, on_click=toggle_theme)
    
    st.write("---")
    st.subheader("🎯 Recruiter Tools")
    recruiter_mode = st.toggle("Enable Recruiter Insights")
    if st.button("✨ Generate Exec Summary"):
        st.session_state.exec_summary_trigger = True
    
    st.write("---")
    st.caption("2026 Edition | Principal Strategy Bot")

# 5. Client & Context
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
try:
    with open("bio.txt", "r") as f:
        context = f.read()
except FileNotFoundError:
    context = "Professional history context unavailable."

# 6. UI Header
st.title("🤖 NicBot")
st.markdown(f"<p style='color:{accent}; font-weight:bold;'>Strategic Advisory & Cyber Intelligence</p>", unsafe_allow_html=True)

# 7. Chat Display
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
