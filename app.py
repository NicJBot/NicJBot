import streamlit as st
from google import genai

# 1. Page Config
st.set_page_config(page_title="NicBot", page_icon="🤖", layout="wide")

# 2. Theme State
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# 3. High-Contrast CSS (No Chips, Improved Readability)
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
    
    /* High Visibility Chat Bubbles */
    .stChatMessage {{ 
        background-color: {card_bg} !important; 
        border: 1px solid {card_border} !important; 
        border-radius: 12px !important; 
        padding: 24px !important; 
        margin-bottom: 25px !important; 
    }}
    
    /* Force high contrast for all text elements */
    .stChatMessage p, .stChatMessage li, .stChatMessage span, .stChatMessage div {{ 
        color: {text_color} !important; 
        font-size: 1.05rem !important; 
        line-height: 1.6 !important;
    }}
    
    [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {card_border}; }}
    
    .thinking-bubble {{ 
        border: 2px solid {accent}; 
        background: {card_bg}; 
        border-radius: 10px; 
        padding: 12px 24px; 
        color: {accent}; 
        font-weight: bold; 
        width: fit-content; 
        animation: pulse 2s infinite; 
    }}
    @keyframes pulse {{ 0% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.6; }} }}

    /* Button Styling */
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
    st.caption("2026 Edition | Privacy-First Architecture")

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

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Input Handling
prompt = st.chat_input("Ask Nicholas anything...")

# Check if summary button was pressed
if st.session_state.get("summary_trigger"):
    st.session_state.summary_trigger = False
    prompt = "Generate a 3-bullet executive summary for a hiring manager based on the context."
    st.session_state.messages.append({"role": "user", "content": "*(System Request)* Generate Executive Summary"})

if prompt:
    # Append user message to state and UI (if not system request)
    if not prompt.startswith("Generate a 3-bullet"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # Assistant Response logic
    with st.chat_message("assistant"):
        think = st.empty()
        think.markdown(f'<div class="thinking-bubble">Analyzing strategic data...</div>', unsafe_allow_html=True)
        
        # System instructions enforcing anonymity
        persona = "You are NicBot, a Principal-level Strategic Advisor. CRITICAL: Never name specific customers. Use industry descriptors (e.g., 'Major Superannuation Fund', 'Tier-1 Bank')."
        if recruiter_mode:
            persona += " Focus on ROI, revenue impact, and leadership scaling."
            
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'system_instruction': f"{persona} Context: {context}"}
        )
        
        think.empty()
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
