import os
from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables


import streamlit as st
from groq import Groq


# streamlit page configuration
st.set_page_config(
    page_title="LLAMA 3.1. Chat",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(working_dir, ".env"))

# Retrieve the API key from Streamlit secrets
GROQ_API_KEY = st.secrets["api_keys"]["GROQ_API_KEY"]

# Optionally set the environment variable if needed
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


client = Groq()

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# streamlit page title
st.title("ChatBot Powered By LLAMA 3.1 🦙")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message:
user_prompt = st.chat_input("Ask LLAMA...")

if user_prompt:

    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # sens user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

