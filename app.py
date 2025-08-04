import streamlit as st
from chatbot_utils import ask_azure_openai

st.set_page_config(page_title="EV Car Sales Assistant", page_icon="🚗", layout="centered")

# This displays a large heading on the page
st.title("EV Car Sales Assistant")

# Simple markdown text below title
st.markdown("This chatbot response is based on manual prompt construction.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box — like ChatGPT
user_query = st.chat_input("Ask anything inside the chat box")

# Intent detection
def detect_test_drive_intent(text):
    keywords = ["test drive", "try it", "book a drive", "test the car", "drive it"]
    return any(k in text.lower() for k in keywords)

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

      # Trigger form if intent is detected
        if detect_test_drive_intent(user_query):
            st.session_state["wants_test_drive"] = True

# Display form if needed
if st.session_state.get("wants_test_drive"):
    with st.form("schedule_drive"):
        name = st.text_input("Your Name")
        contact = st.text_input("Contact (Phone/Email)")
        date = st.date_input("Preferred Date")
        time = st.time_input("Preferred Time")
        submitted = st.form_submit_button("Book Test Drive")

        if submitted:
            from store_test_drive import save_test_drive
            save_test_drive(name, contact, str(date), str(time))
            st.success("Your test drive has been scheduled! We'll contact you soon.")
            st.session_state["wants_test_drive"] = False