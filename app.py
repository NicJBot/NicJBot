import streamlit as st
import requests

st.title("🤖 NicBot")

# Input
prompt = st.chat_input("Ask about Nic...")

if prompt:
    # 1. Get your key from secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # 2. Define the "Brain" (The Bio)
    with open("bio.txt", "r") as f:
        context = f.read()

    # 3. Talk to Google directly via Web (The "No-Library" Method)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Context: {context}\n\nUser: {prompt}"}]
        }]
    }

    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        answer = response.json()['candidates'][0]['content']['parts'][0]['text']
        st.write(answer)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
