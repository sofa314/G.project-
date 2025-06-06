from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock user data (in production, this should be replaced with a database)
USERS = {
    "admin@example.com": {"password": "password123"},
    "user@example.com": {"password": "userpass"}
}

@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = USERS.get(email)
        if user and user['password'] == password:
            # In a real application, generate a JWT token here
            return jsonify({
                "access_token": "your-jwt-token-here",
                "user": {
                    "email": email
                }
            })
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'msg': 'Username and password are required'}), 400

        if username in USERS:
            return jsonify({'msg': 'User already exists'}), 400

        USERS[username] = {'password': password}
        return jsonify({'msg': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/protected', methods=['GET', 'OPTIONS'])
@cross_origin()
def protected():
    auth = request.headers.get('Authorization')
    if not auth:
        return jsonify({'msg': 'Missing token'}), 401
    # Mock user info
    return jsonify({'msg': f'Welcome, {auth.split()[-1]}!'}), 200

@app.route('/history', methods=['GET', 'OPTIONS'])
@cross_origin()
def history():
    auth = request.headers.get('Authorization')
    if not auth:
        return jsonify({'msg': 'Missing token'}), 401
    # Mock history data
    return jsonify({'history': [
        {'type': 'Heart Checkup', 'result': 'Normal', 'date': '2024-06-01'},
        {'type': 'Skin Checkup', 'result': 'No issues', 'date': '2024-05-15'}
    ]}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5501))
    app.run(debug=True, port=port)