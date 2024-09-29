import os
import google.generativeai as genai
import creds
# !!!!!!JOIN DEVPOST!!!!!: https://nam12.safelinks.protection.outlook.com/?url=https%3A%2F%2Fdevpost.com%2Fsoftware%2F719074%2Fjoins%2FPv9v9-vwvAOKzNgxg06mTw&data=05%7C02%7CJUG132%40pitt.edu%7Ce900bf57b70a43d8334408dcdff2c106%7C9ef9f489e0a04eeb87cc3a526112fd0d%7C1%7C0%7C638631480928201085%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=b55h8NHZlhSnjuBgESnYFkASwpDNXmYPHuxifaLdnkg%3D&reserved=0
genai.configure(creds.api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

history = []

def get_model_response(user_input):
    """This function takes user input and returns the model's response."""
    # Start a chat session with history
    chat_session = model.start_chat(
        history=history
    )

    # Send the user's message to the model
    response = chat_session.send_message(user_input)

    # Extract the model's response text
    model_response = response.text

    # Update the conversation history
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})

    # Return the model's response
    return model_response
