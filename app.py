import streamlit as st
from google import genai

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
    .stChatMessage p, .stChatMessage li, .stChatMessage span, .stChatMessage div {{ color: {text_color} !important; font-size: 1.05rem !important; line-height: 1.6 !important; }}
    [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {card_border}; }}
    .thinking-bubble {{ border: 2px solid {accent}; background: {card_bg}; border-radius: 10px; padding: 12px 24px; color: {accent}; font-weight: bold; width: fit-content; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.6; }} }}
    div.stButton > button {{ border-radius: 10px !important; font-weight: 600 !important; width: 100% !important; }}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar Tools
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")
    st.title("NicBot v3.0")
    st.button("☀️ Light Mode" if st.session_state.theme == "dark" else "🌙 Dark Mode", on_click=toggle_theme)
    st.write("---")
    
    st.subheader("🎯 Recruiter Tools")
    recruiter_mode = st.toggle("Enable Recruiter Mode")
    
    if recruiter_mode:
        st.info("💡 **Recruiter Guide Active**")
        with st.expander("Suggested Prompts"):
            st.markdown("* **Scale:** 'How did you double your portfolio ARR?'\n* **Retention:** 'Tell me about the major superannuation turnaround.'\n* **Technical:** 'How do you use AI to scale account discovery?'")
    
    if st.button("✨ Generate Exec Summary"):
        st.session_state.summary_trigger = True
    
    st.write("---")
    
    # Interest & Share
    contact_email = "your-email@example.com" 
    mailto_link = f"mailto:{contact_email}?subject=Interest from NicBot&body=Hi Nic, I'd like to chat."
    st.markdown(f'<a href="{mailto_link}" target="_blank" style="text-decoration:none;"><div style="background-color:{accent};color:white;padding:10px;border-radius:10px;text-align:center;font-weight:bold;">📧 I\'m Interested - Email Nic</div></a>', unsafe_allow_html=True)
    
    st.write("---")
    
    # Developer/Review Section
    with st.expander("🔐 Session Debug (Dev Only)"):
        st.caption("Review current conversation flow:")
        if "messages" in st.session_state:
            transcript = ""
            for msg in st.session_state.messages:
                transcript += f"{msg['role'].upper()}: {msg['content']}\n\n"
            st.text_area("Session Transcript", value=transcript, height=200)
    
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
    initial_greeting = "Hello! I'm NicBot. I've been trained on Nicholas's professional history as a Principal Strategic Advocate. How can I help you today?"
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

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
        think.markdown(f'<div class="thinking-bubble">Analyzing strategic data...</div>', unsafe_allow_html=True)
        
        persona = "You are NicBot. Never name specific customers. Use industry descriptors."
        if recruiter_mode:
            persona += " Focus intensely on ROI, revenue impact, and leadership scaling."
            
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'system_instruction': f"{persona} Context: {context}"}
        )
        
        think.empty()
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

        # --- NATIVE GENERATIVE UI: SKILLS CHART ---
        if any(w in prompt.lower() for w in ["skill", "expertise", "technical", "competency"]):
            st.write("---")
            st.markdown("### ⚡ Principal Competency Matrix")
            
            # Using standard Streamlit columns and progress bars for maximum stability
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Threat Intelligence (GCTI)**")
                st.progress(95)
                st.write("**Strategic Advocacy**")
                st.progress(90)
            with col2:
                st.write("**AI/LLM Workflows**")
                st.progress(88)
                st.write("**Account Retention**")
                st.progress(92)
            
            st.caption("Metrics based on verified career outcomes and GIAC certifications.")
