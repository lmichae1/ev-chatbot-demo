import streamlit as st
import pandas as pd
from chatbot_utils import ask_groq_openai

st.set_page_config(page_title="EV Car Sales Assistant", page_icon="🚗", layout="centered")

# Title and description
st.title("EV Car Sales Assistant")
st.markdown("This chatbot response is based on manual prompt construction.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "wants_test_drive" not in st.session_state:
    st.session_state.wants_test_drive = False

if "booking_success" not in st.session_state:
    st.session_state.booking_success = False

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box for new chat message
user_query = st.chat_input("Ask anything inside the chat box")

# Detect test drive keywords
def detect_test_drive_intent(text):
    keywords = ["test drive", "try it", "book a drive", "test the car", "drive it"]
    return any(k in text.lower() for k in keywords)

# On new message
if user_query:
    # Reset download button visibility
    st.session_state.booking_success = False

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Assistant response
    with st.chat_message("assistant"):
        response = ask_groq_openai(user_query)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Check for test drive interest
        if detect_test_drive_intent(user_query):
            st.session_state.wants_test_drive = True

# Show booking form if requested
if st.session_state.wants_test_drive:
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
            st.session_state.wants_test_drive = False
            st.session_state.booking_success = True

# Show download button only after successful booking
if st.session_state.booking_success:
    try:
        df = pd.read_csv("test_drive_bookings.csv")
        st.download_button(
            label="Download Test Drive Scheduled Bookings",
            data=df.to_csv(index=False),
            file_name="test_drive_bookings.csv",
            mime="text/csv"
        )
    except FileNotFoundError:
        st.error("Booking file not found.")