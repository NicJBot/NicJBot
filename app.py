import streamlit as st
from google import genai

# 1. Page Setup
st.set_page_config(page_title="NicBot | AI Career Assistant", page_icon="🤖")
st.title("🤖 Meet NicBot")

# 2. Setup New Gemini Client
# This uses the latest SDK to avoid 404 versioning errors
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Load Bio
with open("bio.txt", "r") as f:
    nic_context = f.read()

# 3. Chat Logic
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
        # We use the most stable model name 'gemini-2.0-flash'
        # and pass the bio as a System Instruction
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config={
                'system_instruction': f"You are NicBot, a career assistant. Use this bio: {nic_context}"
            }
        )
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
