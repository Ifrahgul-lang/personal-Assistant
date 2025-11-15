import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
api_key = os.getenv("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")

st.set_page_config(page_title="Personal Assistant Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 Personal Assistant Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
prompt = st.chat_input("Ask me anything...")

if prompt:
    if not api_key:
        st.error("API key missing! Add it inside your .env file.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        assistant_reply = response.choices[0].message["content"]

    except Exception as e:
        assistant_reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.write(assistant_reply)
