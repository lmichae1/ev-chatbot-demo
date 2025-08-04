import os
import re
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


# Load product FAQ and extract model names
def load_faq_context_and_models(file_path="product_faqs.md"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Extract model names from headers (assuming ## Model Name format)
            model_names = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)

            # Debug: Print extracted models
           # print(f"DEBUG: Extracted models from FAQ: {model_names}")

            return content, model_names
    except FileNotFoundError:
        print(f"ERROR: Could not find {file_path}")
        return "", []


# Construct prompt with stricter model enforcement
def build_prompt(user_query, user_profile=None, faq_context=None, model_list=None):
    messages = []

    # Add FAQ context first
    if faq_context:
        messages.append({
            "role": "system",
            "content": f"[PRODUCT FAQ - YOUR KNOWLEDGE BASE]\n{faq_context}\n\n"
                       "IMPORTANT: This FAQ contains ALL the information about our available models. "
                       "Do not reference any models or information outside of this FAQ."
        })

    # Add strict model constraints
    if model_list and len(model_list) > 0:
        models_formatted = "\n".join([f"- {model}" for model in model_list])
        messages.append({
            "role": "system",
            "content": f"""[STRICT MODEL CONSTRAINTS]
AVAILABLE MODELS ONLY:
{models_formatted}

CRITICAL RULES:
1. You can ONLY mention models from the above list
2. If asked about any other model, respond: "I'm sorry, that model is not available in our current lineup. Our available models are: {', '.join(model_list)}"
3. Do not invent, assume, or hallucinate any model names
4. Base all responses strictly on the FAQ content provided above
5. If you don't have information about something in the FAQ, say "I don't have that information in our current documentation"
"""
        })
    else:
        messages.append({
            "role": "system",
            "content": "WARNING: No models were extracted from the FAQ. Please check the FAQ format."
        })

    # Main role and instructions
    messages.append({
        "role": "system",
        "content": """
[ROLE]
You are a smart and friendly electric vehicle (EV) sales assistant working for a leading EV manufacturer.

[TASKS]
1. ONLY recommend EV models from the STRICT MODEL CONSTRAINTS list above
2. Answer questions using ONLY information from the PRODUCT FAQ
3. If asked about models not in your list, use the exact response format specified above
4. For general EV benefits, keep responses concise and factual
5. For test drive requests, collect:
   - Preferred date and time
   - Contact number or email
   - Preferred model from available list

[RESPONSE STYLE]
- Warm, concise, and helpful
- Always verify model names against your approved list
- Reference the FAQ when providing specific details
"""
    })

    # Add user profile if provided
    if user_profile:
        messages.append({
            "role": "system",
            "content": f"[CUSTOMER PROFILE]\n{user_profile}"
        })

    # Add user query
    messages.append({
        "role": "user",
        "content": user_query
    })

    return messages


# Main function to ask GPT with enhanced error handling
def ask_azure_openai(query, user_profile=None):
    try:
        # Load FAQ and models
        faq_context, model_list = load_faq_context_and_models()

        # Validate that we have models
        if not model_list:
            return "Error: No models found in FAQ. Please check the product_faqs.md file format."

        # Build prompt with strict constraints
        prompt_messages = build_prompt(
            user_query=query,
            user_profile=user_profile,
            faq_context=faq_context,
            model_list=model_list
        )

        # Debug: Print the system messages (remove in production)
        # print("DEBUG: System messages being sent:")
        #for i, msg in enumerate(prompt_messages[:-1]):  # Exclude user message
        #    if msg["role"] == "system":
        #        print(f"System message {i}: {msg['content'][:200]}...")

        # Make API call with lower temperature for more consistent responses
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=prompt_messages,
            temperature=0.3,  # Reduced from 0.7 for more consistent responses
            max_tokens=500,  # Limit response length
            top_p=0.9  # Add top_p for more focused responses
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"


# Additional helper function to validate responses
def validate_model_mentions(response_text, allowed_models):
    """Check if the response mentions any models not in the allowed list"""
    response_lower = response_text.lower()
    allowed_lower = [model.lower() for model in allowed_models]

    # Simple validation - you might want to make this more sophisticated
    for word in response_text.split():
        clean_word = re.sub(r'[^\w]', '', word.lower())
        if len(clean_word) > 3 and clean_word not in allowed_lower:
            # Check if this might be a model name (contains numbers, capitals, etc.)
            if re.search(r'[0-9]', word) or word.istitle():
                print(f"WARNING: Potential hallucinated model detected: {word}")

    return True


# Test function to verify your FAQ parsing
def test_faq_parsing(file_path="product_faqs.md"):
    content, models = load_faq_context_and_models(file_path)
    print(f"FAQ file exists: {len(content) > 0}")
    print(f"Number of models found: {len(models)}")
    print(f"Models: {models}")
    if content:
        print(f"First 200 characters of FAQ:\n{content[:200]}...")
    return models