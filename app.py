import streamlit as st
from openai import OpenAI

# 1. Page Setup & Branding
st.set_page_config(
    page_title="NicBot | AI Career Assistant", 
    page_icon="🤖", 
    layout="centered"
)

# Custom Header
st.title("🤖 Meet NicBot")
st.subheader("Your AI Guide to Nic's Professional Background")
st.markdown("""
    Welcome! I am a custom RAG (Retrieval-Augmented Generation) agent 
    built by Nic to demonstrate his hands-on AI development, 
    prompt engineering, and technical strategy skills.
""")

# 2. Sidebar Information
with st.sidebar:
    st.header("Quick Facts")
    st.info("""
    - **Target Role:** Principal Technical Account Manager
    - **Focus:** Cybersecurity & Threat Intel
    - **Current Goal:** CISSP Certification
    """)
    st.divider()
    st.markdown("Built with: **Streamlit + Gemini 1.5 Flash**")

# 3. Load the Knowledge Base (bio.txt)
try:
    with open("bio.txt", "r") as f:
        nic_context = f.read()
except FileNotFoundError:
    nic_context = "Bio information is currently being updated. Please check back soon!"

# 4. Initialize the Client (Using Gemini via OpenAI Compatibility)
# This looks for 'GEMINI_API_KEY' in your Streamlit Secrets
client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm NicBot. Ask me about Nic's experience with Technical Account Management, his Cybersecurity goals, or his latest AI projects."}
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Logic
if prompt := st.chat_input("Ask a question about Nic..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response from Gemini
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {
                    "role": "system", 
                    "content": f"""
                    You are 'NicBot', a professional career assistant. 
                    Your tone is helpful, strategic, and concise.
                    Use the following context to answer questions about Nic: {nic_context}
                    If a question is outside this context, politely suggest contacting Nic directly.
                    """
                },
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
