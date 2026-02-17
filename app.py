from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle

app = Flask(__name__)
CORS(app)


# Load model and scaler
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route("/")
def home():
    return jsonify({
        "message": "SafeRoad Backend Running Successfully"
    })

@app.route("/send_sensor_data", methods=["POST"])
def receive_sensor_data():
    try:
        data = request.json

        speed = data["speed"]
        acceleration = data["acceleration"]
        brake_force = data["brake_force"]
        weather = data["weather"]

        features = np.array([[speed, acceleration, brake_force, weather]])
        scaled_features = scaler.transform(features)

        prediction = model.predict(scaled_features)[0]
        probability = model.predict_proba(scaled_features)[0][1]

        if prediction == 1:
            risk_level = "HIGH"
            alert_message = "⚠️ High Accident Risk! Slow Down!"
        else:
            risk_level = "LOW"
            alert_message = "Safe Driving Conditions"

        return jsonify({
            "risk_level": risk_level,
            "probability": float(probability),
            "alert": alert_message
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


