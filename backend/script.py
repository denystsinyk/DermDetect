import torch
import torch.nn as nn
from torchvision import models, transforms
from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
from flask_cors import CORS

app = Flask(__name__)

device = "cpu"

model = models.efficientnet_b0(weights=None).to(device)  # No pretrained weights
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 4).to(device)  # Modify output layer

# Load the saved state dictionary
model.load_state_dict(torch.load('efficientnet_b0_skin.pth',map_location=torch.device('cpu'),weights_only=True))

# Set the model to evaluation mode
model.eval()

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

CORS(app, resources={r"/*": {"origins": "*"}})

def preprocess_image(image_data):
    """Convert base64-encoded image to a PyTorch tensor."""
    image = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
    image = preprocess(image).unsqueeze(0)  # Add batch dimension
    return image

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data['image']

    # Preprocess the image
    image_tensor = preprocess_image(image_data)

    # Run the model and get the prediction
    with torch.no_grad():
        output = model(image_tensor)
        _, predicted_class = torch.max(output, 1)
    
    # Map prediction index to class name
    class_mapping = {0: 'Acne', 1: 'Eczema', 2: 'Moles', 3: 'Warts'}  # Adjust based on your dataset classes
    prediction = class_mapping.get(predicted_class.item(), 'Unknown')

    return jsonify({'result': prediction})

if __name__ == '__main__':
    app.run(debug=True)
