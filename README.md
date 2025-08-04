## EV Car Sales Assistant

A friendly electric vehicle (EV) chatbot assistant built using **Streamlit** and **Azure OpenAI**, designed to simulate a virtual sales assistant experience. It uses **manual prompt construction** and session-based chat memory to guide users through EV recommendations and test drive bookings.

---

## Features

- Chat UI powered by **Streamlit**
- Backend integration with **Azure OpenAI (GPT model)**
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
- [Azure OpenAI](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- Optional: `.env` management via `python-dotenv`

---

## Getting Started

1. Clone this repo
git clone https://github.com/yourusername/ev-car-sales-assistant.git
cd ev-car-sales-assistant

2. Create .env file
Create a .env file in the root directory and include your Azure OpenAI credentials:
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name  # e.g. gpt-35-turbo

3. Install dependencies
pip install -r requirements.txt

4. Run the app
streamlit run app.py

5. Disclaimer
This version uses manual prompt construction only. It does not yet support vector search or persistent memory 

6. License
MIT License – feel free to modify and use for personal or educational projects.