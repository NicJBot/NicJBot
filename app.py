import streamlit as st
import google.generativeai as genai

# 1. Page Setup
st.set_page_config(page_title="NicBot | AI Career Assistant", page_icon="🤖")
st.title("🤖 Meet NicBot")

# 2. Setup Gemini (Direct Native Implementation)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load Bio for context
with open("bio.txt", "r") as f:
    nic_context = f.read()

# 3. Initialize Model with a clear System Instruction
# We use 'gemini-1.5-flash' but we'll try the 'models/' prefix if it fails
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=f"You are NicBot, a professional career assistant. Use this context: {nic_context}"
)

# 4. Chat logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about Nic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # The 'stream=True' can sometimes cause 404s on fresh projects, 
        # so we'll use a standard call for stability first.
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
