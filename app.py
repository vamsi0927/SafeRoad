from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "SafeRoad Backend Running Successfully"
    })

@app.route("/send_sensor_data", methods=["POST"])
def receive_sensor_data():
    try:
        data = request.json

        speed = float(data["speed"])
        acceleration = float(data["acceleration"])
        brake_force = float(data["brake_force"])
        weather = float(data["weather"])

        # Logistic-style trained formula
        score = (
    0.12 * speed +        # strong speed impact
    2.0 * acceleration +
    3.0 * brake_force +
    4.0 * weather
)

probability = 1 / (1 + np.exp(-(score - 10) * 0.5))



        if probability > 0.7:
            risk_level = "HIGH"
            alert_message = "⚠️ High Accident Risk! Slow Down!"
        elif probability > 0.4:
            risk_level = "MEDIUM"
            alert_message = "⚠️ Moderate Risk! Drive Carefully!"
        else:
            risk_level = "LOW"
            alert_message = "Safe Driving Conditions"

        return jsonify({
            "risk_level": risk_level,
            "probability": float(probability),
            "alert": alert_message
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


