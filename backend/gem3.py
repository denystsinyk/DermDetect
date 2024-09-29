import os
import google.generativeai as genai
from script import prediction

# Configure the API key (consider using environment variables for security)
genai.configure(api_key="AIzaSyD1cv3p_n_Ro3HXdI-OpupcTf5ptWnuyZY")

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Initialize the chat session with empty history
chat_session = model.start_chat(history=[])

# Initialize the history
history = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    try:
        # Send the message and get the response
        response = chat_session.send_message(user_input)

        model_response = response.text

        print("Gemini:", model_response)
        print()

        # Update history
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]})
        
    except Exception as e:
        print("Error:", e)

if prediction == "Acne":
    acne_remedies = "Avoid rubbing and touching skin lesions. Squeezing or picking blemishes can cause scars or dark blotches to develop."
    acne_products1 = "Differin Gel" #(https://www.kqzyfj.com/click-100700049-13848895?url=https%3A%2F%2Fwww.cvs.com%2Fshop%2Fdifferin-gel-prodid-1190782%3FskuId%3D213858%26WT.mc_id%3Dps_google_pla_213858&cjsku=213858)
    acne_products2 = "Neutrogena Gel" #(https://www.cvs.com/shop/neutrogena-rapid-clear-stubborn-acne-medicine-spot-treatment-gel-1-oz-prodid-1020022?cjdata=MXxOfDB8WXww&skuId=990146&WT.mc_id=ps_google_pla_990146&CID=aff_100700049-13848895&cjevent=25ddfe167e2511ef8028d6c40a82b821)
    acne_products3 = ""
elif prediction == "Warts":
    wart_remedies = "Both cryotherapy and salicylic acid are effective treatments for removing warts." +
     "Cryotherapy is often quicker but requires a visit to a healthcare provider while salicylic acid is more convenient for home use but may take several weeks for full results."
elif prediction == "Eczema":
    eczma_remedies = "Hydrocortisone cream is a mild corticosteroid that can help reduce inflammation, redness, and itching associated with eczema."
elif prediction == "Moles":
    mole_remedies = "Recommendation: Use products with salicylic acid."


    



