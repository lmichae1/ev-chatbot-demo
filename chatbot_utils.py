import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()  # This loads the .env file variables into environment


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


# Load product FAQ content (fallback to empty string if file not found)
def load_faq_context(file_path="product_faq.md"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

# Build structured prompt
def build_prompt(user_query, user_profile=None, faq_context=None):
    messages = [
        {
            "role": "system",
            "content": """
[ROLE]
You are a smart and friendly electric vehicle (EV) sales assistant working for a leading EV manufacturer.

[TASKS]
1. Recommend EV models based on customer preferences such as type (SUV, sedan, coupe), color, budget, or tier (luxury, performance, family).
2. Explain the benefits of EVs including eco-friendliness, performance, cost savings, and integrated AI features.
3. Emphasize why buying from our company is a smart choice: innovation, excellent support, warranty, and AI driving experience.

[GUIDELINES]
Be warm, concise, informative, and engaging.
"""
        }
    ]

    if user_profile:
        messages.append({
            "role": "system",
            "content": f"[CUSTOMER PROFILE]\n{user_profile}"
        })

    if faq_context:
        messages.append({
            "role": "system",
            "content": f"[PRODUCT FAQ]\n{faq_context}"
        })

    messages.append({
        "role": "user",
        "content": user_query
    })

    return messages

# Main function to query Azure OpenAI
def ask_azure_openai(query, user_profile=None):
    faq_context = load_faq_context()

    prompt_messages = build_prompt(
        user_query=query,
        user_profile=user_profile,
        faq_context=faq_context
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=prompt_messages,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()