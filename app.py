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
    bg_color, text_color, card_bg = "#0d1117", "#f0f6fc", "rgba(255, 255, 255, 0.07)"
    card_border, sidebar_bg, accent = "rgba(255, 255, 255, 0.15)", "#161b22", "#58a6ff"
else:
    bg_color, text_color, card_bg = "#ffffff", "#1f2328", "#f6f8fa"
    card_border, sidebar_bg, accent = "#d0d7de", "#f3f4f6", "#0969da"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Inter', sans-serif; transition: all 0.3s ease; }}
    [data-testid="stChatMessageContainer"] {{ padding-left: 12% !important; padding-right: 12% !important; max-width: 1200px; margin: 0 auto; }}
    .stChatMessage {{ background-color: {card_bg} !important; border: 1px solid {card_border} !important; border-radius: 16px !important; padding: 24px !important; margin-bottom: 20px !important; }}
    [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {card_border}; }}
    .thinking-bubble {{ border: 1.5px solid {accent}; background: {card_bg}; border-radius: 12px; padding: 12px 24px; color: {accent}; font-weight: 600; width: fit-content; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.5; }} }}
    div.stButton > button {{ border-radius: 10px !important; font-weight: 600 !important; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar Tools
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")
    st.title("NicBot v3.0")
    
    # Theme Toggle
    theme_btn_text = "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode"
    st.button(theme_btn_text, on_click=toggle_theme)
    
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
        st.markdown(message["content"])

# 8. Main Logic Flow
# Check for button-triggered summary first
current_prompt = None
if st.session_state.get("exec_summary_trigger"):
    st.session_state.exec_summary_trigger = False
    current_prompt = "Generate a 3-bullet executive summary for a hiring manager based on the bio."
    st.session_state.messages.append({"role": "user", "content": "*(System)* Generate Executive Summary"})
else:
    current_prompt = st.chat_input("Ask Nicholas anything...")

# 9. Execution
if current_prompt:
    # If it's a manual user input, show it in the UI
    if not current_prompt.startswith("Generate a 3-bullet"):
        st.session_state.messages.append({"role": "user", "content": current_prompt})
        with st.chat_message("user"):
            st.markdown(current_prompt)

    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(f'<div class="thinking-bubble">Consulting strategic context...</div>', unsafe_allow_html=True)
        
        persona = "You are NicBot, a Principal-level Strategic Advisor."
        if recruiter_mode:
            persona += " Focus on ROI, high-level leadership, and revenue scaling."
            
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=current_prompt,
            config={'system_instruction': f"{persona} Context: {context}"}
        )
        
        thinking_placeholder.empty()
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
