import streamlit as st
from chatbot_utils import ask_azure_openai

st.set_page_config(page_title="EV Car Sales Assistant", page_icon="🚗", layout="centered")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box — like ChatGPT
user_query = st.chat_input("Ask anything inside the chat box")

# When user submits a message
if user_query:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Call backend
    with st.chat_message("assistant"):
        response = ask_azure_openai(user_query)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})