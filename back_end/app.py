import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image

app = Flask(__name__)
CORS(app, origins=['https://sofa314.github.io'], supports_credentials=True)

# Load the models
heart_model = joblib.load("heart_breast/gradin_boost_model.pkl")
breast_model = joblib.load("heart_breast/decision_tree_model.pkl")
scaler = joblib.load("heart_breast/scaler (1).pkl")
skin_model = load_model('skin/skin_cancer_model20.h5')

# Define skin class labels
skin_class_labels = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

# Route for heart prediction
@app.route('/predict-heart', methods=['POST'])
def predict_heart():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    selected_indices = [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12]
    selected_features = features[:, selected_indices]
    selected_features_scaled = scaler.transform(selected_features)
    prediction = heart_model.predict(selected_features_scaled)
    return jsonify({'prediction': int(prediction[0])})

# Route for breast prediction
@app.route('/predict-breast', methods=['POST', 'OPTIONS'])
def predict_breast():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    prediction = breast_model.predict(features)[0]
    result = "Malignant" if prediction == 4 else "Benign"
    return jsonify({"prediction": result})

# Route for skin prediction
@app.route('/predict-skin', methods=['POST'])
def predict_skin():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image = Image.open(image_file).resize((28, 28))
    image = image.convert("RGB")
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array /= 255.0

    prediction = skin_model.predict(image_array)
    predicted_class = skin_class_labels[np.argmax(prediction)]

    return jsonify({
        'predicted_class': predicted_class,
        'confidence': float(np.max(prediction))
    })

# This block is for local development only. Railway will use Gunicorn.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000)) # Default to 5000 for local development
    app.run(host='0.0.0.0', port=port, debug=True) 
