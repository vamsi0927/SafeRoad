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
    0.08 * speed +          # doubled weight
    1.5 * acceleration +
    2.5 * brake_force +
    3.5 * weather
)


        probability = 1 / (1 + np.exp(-(score - 15) * 0.25))


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

