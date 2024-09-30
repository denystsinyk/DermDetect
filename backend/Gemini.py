import google.generativeai as genai

genai.configure(api_key="AIzaSyD1cv3p_n_Ro3HXdI-OpupcTf5ptWnuyZY")

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

def get_gemini_response(user_input):
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)

        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "No valid response from Gemini."
    
    except Exception as e:
        print(f"Error in Gemini API call: {e}")
        return "Error processing request with Gemini."
