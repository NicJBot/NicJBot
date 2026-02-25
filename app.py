import streamlit as st
import google.generativeai as genai

# 1. Setup
st.set_page_config(page_title="NicBot", page_icon="🤖")
st.title("🤖 NicBot")

# 2. Configure API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Load Context
with open("bio.txt", "r") as f:
    nic_context = f.read()

# 4. Initialize the Model (Using 1.5-Flash as the most compatible)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=f"You are NicBot. Context: {nic_context}"
)

# 5. Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Nic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We use a standard generation call for maximum stability
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"NicBot is sleeping. Error: {e}")
