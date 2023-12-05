from PIL import Image
from dotenv import load_dotenv
import pandas as pd
import shutil
import openai
import os
import streamlit as st
import sys


ss = st.session_state

# Set width of sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 450px;
        max-width: 600px;
    }
    """,
    unsafe_allow_html=True,
)


def on_api_key_change():
    api_key = ss.get('api_key') or os.getenv('OPENAI_API_KEY')
    os.environ["OPENAI_API_KEY"] = api_key
    openai.api_key = api_key

st.write("## Lit Chat : A chatbot for literature Q&A")

with st.sidebar:
    st.markdown('### First input your OpenAI API key :key:')
    api_key = st.text_input(
        'OpenAI API key',
        type='password',
        key='api_key',
        on_change=on_api_key_change,
        label_visibility="hidden")
    
if api_key:
    from lit_chat.chat import ask_gpt_with_docs

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", 
                                  "content": "Hi, I will help you find answers to your questions based on literature. \nHow can I help you?"}] 
    
# display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
#if prompt := st.chat_input():
prompt = st.chat_input("Type your question here")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_gpt_with_docs(question=prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)