from flask import Flask, request, jsonify
from flask_cors import CORS
from Gem2 import get_model_response

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()

        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        user_input = data['text']
        print(f"Received text from frontend: {user_input}")

        model_response = get_model_response(user_input)

        print(f"Response from Model: {model_response}")
        return jsonify({'result': model_response})

    except Exception as e:
        print(f"Error in /process: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
