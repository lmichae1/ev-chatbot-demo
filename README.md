## EV Car Sales Assistant

A friendly electric vehicle (EV) chatbot assistant built using **Streamlit** and **GROQ OpenAI GPT-OSS**, designed to simulate a virtual sales assistant experience. It uses **manual prompt construction** and session-based chat memory to guide users through EV recommendations and test drive bookings.

---

## Features

- Chat UI powered by **Streamlit**
- Backend integration with **OpenAI OSS 20B (GPT model)**
- Manually constructed prompt with contextual system instructions
- Responds to:
  - EV model recommendations based on user preferences
  - Test drive scheduling requests
  - EV benefits and company USPs
- Session-based chat history
- Handles FAQ integration from `product_faq.md`
- Schedules test booking details and writes to test_drive_bookings.csv

---

## Tech Stack

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Groq OpenAI API][(https://console.groq.com/home)]
- Optional: `.env` management via `python-dotenv`

---

## Getting Started

1. Clone this repo
git clone https://github.com/yourusername/ev-car-sales-assistant.git
cd ev-car-sales-assistant

2. Create .env file
Create a .env file in the root directory and include your GROQ GPT credentials:
GROQ_API_KEY=your_groq_key_here

3. Install dependencies
pip install -r requirements.txt

4. Run the app
streamlit run app.py

5. Disclaimer
This version uses manual prompt construction only. It does not yet support vector search or persistent memory 

6. License
MIT License – feel free to modify and use for personal or educational projects.
