import streamlit as st
from google import genai

# 1. Page Config (Must remain the first Streamlit command)
st.set_page_config(page_title="NicBot", page_icon="🤖", layout="wide")

# 2. Branding & Styling Block
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    [data-testid="stSidebar"] {
        background-color: #0e1117;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    h1 {
        color: #0e1117;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")
    st.title("NicBot v3.0")
    st.info("**Principal Strategic Advocate**")
    st.write("---")
    st.caption("Built with Gemini 2.5 & Streamlit")
    st.sidebar.caption("🔒 **Security Note:** This bot uses RAG architecture with curated professional data. No sensitive internal IP is stored within this model.")

# 3. Setup Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 4. Load Bio
try:
    with open("bio.txt", "r") as f:
        context = f.read()
except FileNotFoundError:
    context = "Bio info missing."

# 5. Page Title
st.title("🤖 NicBot")

# 6. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Production Logic
if prompt := st.chat_input("Ask about Nic's experience..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'system_instruction': f"You are NicBot. Context: {context}"
            }
        )
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
