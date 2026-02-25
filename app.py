import streamlit as st
from google import genai

# 1. Page Config
st.set_page_config(page_title="NicBot", page_icon="🤖")
st.title("🤖 NicBot")

# 2. Setup Client (The 2026 Stable SDK)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Load Bio
try:
    with open("bio.txt", "r") as f:
        context = f.read()
except FileNotFoundError:
    context = "Bio info missing."

# 4. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Production Logic (Gemini 2.5)
if prompt := st.chat_input("Ask about Nic's experience..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # We are using 'gemini-2.5-flash' which is the 2026 stable version.
        # This replaces the retired 1.5-flash model.
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'system_instruction': f"You are NicBot. Context: {context}"
            }
        )
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
