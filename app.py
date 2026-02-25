import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="NicBot | AI Career Assistant", page_icon="🤖")
st.title("🤖 Meet NicBot")

# 2. Setup Gemini Native (The "Fix")
# This bypasses the OpenAI bridge entirely
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Load Knowledge Base
try:
    with open("bio.txt", "r") as f:
        nic_context = f.read()
except FileNotFoundError:
    nic_context = "Bio info missing."

# 4. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The "Model Section" (The Chat Logic)
if prompt := st.chat_input("Ask about Nic's experience..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        # We build the instruction right here
        system_instruction = f"You are NicBot. Use this bio to answer: {nic_context}. Be professional."
        
        # This is where the model is called!
        response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
