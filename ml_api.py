from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
import joblib
import numpy as np

# تحميل الموديلات
heart_model = joblib.load("ml_models/gradin_boost_model.pkl")  # قلب
breast_model = joblib.load("ml_models/decision_tree_model.pkl")  # سرطان
scaler = joblib.load("ml_models/scaler (1).pkl")  # لو محتاجه

# Route لتوقع مرض القلب
@app.route('/predict-heart', methods=['POST'])
def predict_heart():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)  # shape (1, 13)
    # Indices of the 11 features your model expects
    selected_indices = [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12]
    selected_features = features[:, selected_indices]
    # Scale the selected features if needed
    selected_features_scaled = scaler.transform(selected_features)
    prediction = heart_model.predict(selected_features_scaled)
    return jsonify({'prediction': int(prediction[0])})


# Route لتوقع سرطان الثدي
@app.route('/predict-breast', methods=['POST', 'OPTIONS'])
def predict_breast():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    prediction = breast_model.predict(features)[0]
    result = "Malignant" if prediction == 4 else "Benign"
    return jsonify({"prediction": result})

# تشغيل السيرفر
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)


# features = scaler.transform(features)  # scaling لو الموديل محتاجه
