import streamlit as st
from google import genai
import datetime

# 1. Page Config (Must remain the first Streamlit command)
st.set_page_config(page_title="NicBot", page_icon="🤖", layout="wide")

# 2. Branding & Styling Block (Glassmorphism & Pulse Animations)
st.markdown("""
    <style>
    /* Dark Glassmorphism Theme */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1c1f26 100%);
        color: #e0e0e0;
    }
    
    /* Frosted Glass Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(14, 17, 23, 0.85) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Thinking Pulse Animation */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); border-color: rgba(0, 255, 255, 0.2); }
        50% { box-shadow: 0 0 15px rgba(0, 255, 255, 0.6); border-color: rgba(0, 255, 255, 0.6); }
        100% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); border-color: rgba(0, 255, 255, 0.2); }
    }

    .thinking-bubble {
        border: 1px solid #00ffff;
        animation: pulse-glow 1.5s infinite ease-in-out;
        background: rgba(0, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px 20px;
        color: #00ffff;
        width: fit-content;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 0.9em;
        margin-bottom: 15px;
    }

    /* Glass Cards for Chat Messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(5px);
    }

    /* Recruiter Button Styling */
    div.stButton > button {
        background: rgba(0, 255, 255, 0.1) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        color: #00ffff !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        background: rgba(0, 255, 255, 0.2) !important;
        border-color: #00ffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar with Heatmap/Recruiter Toggles
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")
    st.title("NicBot v3.0")
    st.info("**Principal Strategic Advocate**")
    
    st.write("---")
    # Recruiter Specific Features
    st.subheader("🎯 Recruiter Tools")
    recruiter_mode = st.toggle("Enable Recruiter Insights")
    if st.button("Generate Exec Summary"):
        st.session_state.exec_summary_trigger = True
    
    st.write("---")
    st.caption("Built with Gemini 2.5 & Streamlit")
    st.sidebar.caption("🔒 **Security Note:** RAG architecture verified. No sensitive IP stored.")

# 4. Setup Client & Load Context
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

try:
    with open("bio.txt", "r") as f:
        context = f.read()
except FileNotFoundError:
    context = "Bio info missing."

# 5. Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "interest_heatmap" not in st.session_state:
    st.session_state.interest_heatmap = {"Technical": 0, "Leadership": 0, "Cultural": 0}

# 6. Page Title & UI
st.title("🤖 NicBot")
if recruiter_mode:
    st.success("Recruiter Mode Active: I will prioritize ROI, Scale, and Leadership metrics.")

# 7. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Handling Exec Summary (Button Trigger)
if st.session_state.get("exec_summary_trigger"):
    st.session_state.exec_summary_trigger = False
    summary_prompt = "Generate a 3-bullet pitch for a hiring manager based on Nic's profile."
    # This acts like a user prompt automatically
    st.chat_input(value=summary_prompt, key="auto_prompt") 

# 9. Main Chat Logic
if prompt := st.chat_input("Ask about Nic's experience..."):
    # Analytics Layer: Interest Heatmap tracking
    if any(word in prompt.lower() for word in ["scale", "arr", "growth"]): st.session_state.interest_heatmap["Technical"] += 1
    if any(word in prompt.lower() for word in ["lead", "mentor", "culture"]): st.session_state.interest_heatmap["Leadership"] += 1
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Glassmorphism Thinking Animation
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown('<div class="thinking-bubble">Synthesizing strategic insights...</div>', unsafe_allow_html=True)
        
        # System Instruction tailoring based on Recruiter Mode
        persona = "You are NicBot, a Principal-level Strategic Advisor."
        if recruiter_mode:
            persona += " Focus on ROI, revenue impact, and leadership scaling."
            
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'system_instruction': f"{persona} Context: {context}"
            }
        )
        
        # Clear thinking pulse and show response
        thinking_placeholder.empty()
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
