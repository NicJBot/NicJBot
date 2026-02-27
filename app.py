import streamlit as st
from google import genai

# 1. Page Config
st.set_page_config(page_title="NicBot", page_icon="🤖", layout="wide")

# 2. Theme State
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# 3. Enhanced Contrast CSS
if st.session_state.theme == "dark":
    # High-contrast white text for dark mode
    bg_color, text_color, card_bg = "#0d1117", "#FFFFFF", "rgba(255, 255, 255, 0.12)"
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
        margin-bottom: 20px !important; 
        color: {text_color} !important; 
    }}
    
    /* Ensure markdown text inside bubbles is also white */
    .stChatMessage p, .stChatMessage li {{ color: {text_color} !important; font-size: 1.05rem !important; }}
    
    [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {card_border}; }}
    
    .thinking-bubble {{ border: 2px solid {accent}; background: {card_bg}; border-radius: 10px; padding: 12px 24px; color: {accent}; font-weight: bold; width: fit-content; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.6; }} }}
    
    /* Action Chips */
    div.stButton > button {{ border-radius: 20px !important; font-weight: 600 !important; width: 100% !important; border: 1px solid {accent} !important; }}
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
        st.session_state.chip_input = "Generate a 3-bullet executive summary for a hiring manager."
    st.write("---")
    st.caption("2026 Edition | Privacy Protected")

# 5. Client & Context
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
try:
    with open("bio.txt", "r") as f:
        # SCRUBBING CUSTOMER NAMES ON THE FLY FOR EXTRA SAFETY
        context = f.read().replace("UniSuper", "Major Superannuation Fund").replace("Medibank", "Major Private Health Insurer").replace("Mastercard", "Global Financial Services Corporation")
except FileNotFoundError:
    context = "Professional history unavailable."

# 6. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chip_input" not in st.session_state:
    st.session_state.chip_input = None

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Unified Input Logic (Manual or Chip)
user_input = st.chat_input("Ask Nicholas anything...")
if st.session_state.chip_input:
    user_input = st.session_state.chip_input
    st.session_state.chip_input = None # Reset chip

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        think = st.empty()
        think.markdown(f'<div class="thinking-bubble">Analyzing strategic data...</div>', unsafe_allow_html=True)
        
        persona = "You are NicBot. CRITICAL: Never name specific customers like UniSuper or Medibank. Use industry descriptors instead."
        if recruiter_mode: persona += " Prioritize ROI and leadership scaling."
            
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_input,
            config={'system_instruction': f"{persona} Context: {context}"}
        )
        
        think.empty()
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # 8. Functional Action Chips
        st.write("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📈 Retention Case"): st.session_state.chip_input = "Tell me about your strategy for saving the major superannuation account." ; st.rerun()
        with c2: 
            if st.button("🚀 Portfolio Scale"): st.session_state.chip_input = "How did you double your portfolio during the acquisition?" ; st.rerun()
        with c3:
            if st.button("💡 AI Discovery"): st.session_state.chip_input = "Explain your AI-augmented discovery process." ; st.rerun()
