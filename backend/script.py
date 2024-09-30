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
model = models.efficientnet_b0(weights=None).to(device)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 4).to(device)

model.load_state_dict(torch.load('efficientnet_b0_skin.pth', map_location=torch.device('cpu'), weights_only=True))
model.eval()

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

CORS(app, resources={r"/*": {"origins": "*"}})

def preprocess_image(image_data):
    image = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
    image = preprocess(image).unsqueeze(0)
    return image

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data['image']
    image_tensor = preprocess_image(image_data)

    with torch.no_grad():
        output = model(image_tensor)
        _, predicted_class = torch.max(output, 1)

    class_mapping = {0: 'Acne', 1: 'Eczema', 2: 'Moles', 3: 'Warts'}
    prediction = class_mapping.get(predicted_class.item(), 'Unknown')

    return jsonify({'result': prediction})

if __name__ == '__main__':
    app.run(debug=True)
