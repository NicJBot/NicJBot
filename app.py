import streamlit as st
import requests

st.set_page_config(page_title="NicBot", page_icon="🤖")
st.title("🤖 NicBot")

# Load Bio context
try:
    with open("bio.txt", "r") as f:
        context = f.read()
except FileNotFoundError:
    context = "Bio info missing."

# Input from user
if prompt := st.chat_input("Ask about Nic's experience..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    # 1. Get your key from secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # 2. Use the 'gemini-1.5-flash-latest' alias which is more stable for v1beta
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"You are NicBot. Context: {context}\n\nUser Question: {prompt}"}]
        }]
    }

    with st.chat_message("assistant"):
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            answer = response.json()['candidates'][0]['content']['parts'][0]['text']
            st.markdown(answer)
        else:
            # If 404 persists, we'll know exactly why
            st.error(f"API Error {response.status_code}: {response.text}")
