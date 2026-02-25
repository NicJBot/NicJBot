# Change the client initialization to this:
client = OpenAI(
    api_key=st.secrets["Token goes here"], 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# And change the model name in the completion section to:
model="gemini-1.5-flash"
