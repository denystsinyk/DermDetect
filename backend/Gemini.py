import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyD1cv3p_n_Ro3HXdI-OpupcTf5ptWnuyZY")

# Define text generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Function to get the response from the Gemini model
def get_gemini_response(user_input):
    try:
        # Start a new chat session
        chat_session = model.start_chat(history=[])

        # Send the user's input message and get a response from Gemini
        response = chat_session.send_message(user_input)

        # Log the full response object for debugging

        # Check if response has the expected 'text' attribute
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "No valid response from Gemini."
    
    except Exception as e:
        # Log the error if the API call fails
        print(f"Error in Gemini API call: {e}")
        return "Error processing request with Gemini."