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
    
    .stChatMessage {{ 
        background-color: {card_bg} !important; 
        border: 1px solid {card_border} !important; 
        border-radius: 12px !important; 
        padding: 24px !important; 
        margin-bottom: 25px !important; 
    }}
    
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

    div.stButton > button {{ border-radius: 10px !important; font-weight: 600 !important; width: 100% !important; }}
    
    /* Share Button Hover Effect */
    .share-btn:hover {{ opacity: 0.8; transform: translateY(-1px); }}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar with Recruiter Mode Guide & Feedback
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")
    st.title("NicBot v3.0")
    st.button("☀️ Light Mode" if st.session_state.theme == "dark" else "🌙 Dark Mode", on_click=toggle_theme)
    st.write("---")
    
    st.subheader("🎯 Recruiter Tools")
    recruiter_mode = st.toggle("Enable Recruiter Mode")
    
    if recruiter_mode:
        st.info("💡 **Recruiter Guide Active**\n\nPrompts are now optimized for ROI and Leadership metrics.")
        with st.expander("Suggested Prompts"):
            st.markdown("""
            * **Scale:** 'How did you double your portfolio ARR?'
            * **Retention:** 'Tell me about the major superannuation turnaround.'
            * **Technical:** 'How do you use AI to scale account discovery?'
            * **Leadership:** 'Describe your collegiate leadership style.'
            """)
    
    if st.button("✨ Generate Exec Summary"):
        st.session_state.summary_trigger = True
    
    st.write("---")
    
    # --- Recruiter Interest Button ---
    st.subheader("📩 Immediate Interest")
    contact_email = "your-email@example.com" 
    mailto_link = f"mailto:{contact_email}?subject=Interest from NicBot&body=Hi Nic, I've been interacting with NicBot and would like to schedule a time to chat."
    
    st.markdown(f"""
        <a href="{mailto_link}" target="_blank" style="text-decoration: none;">
            <div style="background-color: {accent}; color: white; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold;">
                📧 I'm Interested - Email Nic
            </div>
        </a>
    """, unsafe_allow_html=True)

    # --- NEW: Share NicBot Button ---
    st.write("")
    # Get the URL of the app (Streamlit Cloud usually uses this)
    app_url = "https://nicjbot.streamlit.app" 
    share_text = "Check out NicBot—a custom AI built by Nicholas to showcase his experience as a Principal Strategic Advocate."
    
    # Simple JavaScript copy-to-clipboard button
    st.components.v1.html(f"""
        <button onclick="copyLink()" style="
            width: 100%; 
            background-color: transparent; 
            color: {accent}; 
            border: 1px solid {accent}; 
            padding: 8px; 
            border-radius: 10px; 
            font-weight: bold; 
            cursor: pointer;
            font-family: sans-serif;
        ">
            🔗 Share NicBot Link
        </button>
        <script>
        function copyLink() {{
            navigator.clipboard.writeText('{app_url}');
            alert('NicBot link copied to clipboard!');
        }}
        </script>
    """, height=50)
    
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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Input Handling
prompt = st.chat_input("Ask Nicholas anything...")

if st.session_state.get("summary_trigger"):
    st.session_state.summary_trigger = False
    prompt = "Generate a 3-bullet executive summary for a hiring manager based on the context."
    st.session_state.messages.append({"role": "user", "content": "*(System Request)* Generate Executive Summary"})

if prompt:
    if not prompt.startswith("Generate a 3-bullet"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # 8. Assistant Response logic
    with st.chat_message("assistant"):
        think = st.empty()
        think.markdown(f'<div class="thinking-bubble">Analyzing strategic data...</div>', unsafe_allow_html=True)
        
        persona = "You are NicBot, a Principal-level Strategic Advisor. CRITICAL: Never name specific customers."
        
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
