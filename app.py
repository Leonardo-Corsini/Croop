import datetime
import json

from flask import Flask, render_template, jsonify, request
import random
import requests
import time

app = Flask(__name__, static_folder="static")

API_KEY = "c4d67afa-6289-4a54-9a05-880b7069469c"

# Sample alert messages with corresponding solutions
FAKE_ALERTS = {
    "⚠ High soil moisture detected!": "Try Syngenta’s biologicals to improve soil health and moisture retention.",
    "🔥 Possible fire hazard nearby!": "Use Syngenta's solutions to create fire-resistant crops and reduce risk.",
    "💨 Strong winds approaching the farm!": "Consider Syngenta's windbreak products to protect your crops.",
    "🌧 Heavy rainfall expected soon!": "Protect your crops from excess water with Syngenta’s rain-tolerant biologicals.",
    "🐛 Pest infestation detected in Zone 3!": "Use Syngenta’s biological pest control solutions to safely eliminate pests."
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_notification")
def get_notification():
    """Returns a random fictitious notification with a solution."""
    fake_alert = random.choice(list(FAKE_ALERTS.keys()))
    solution = FAKE_ALERTS[fake_alert]
    timestamp = time.strftime("%H:%M:%S")  # Add a timestamp
    return jsonify({
        "problem": f"{timestamp} - {fake_alert}",
        "solution": solution
    })


@app.route("/get_corn_risk", methods=["GET"])
def get_corn_risk():
    url = "https://services.cehub.syngenta-ais.com/api/DiseaseRisk/CornRisk_V2"
    time = datetime.datetime.now()
    delta_15_minutes = datetime.timedelta(hours=0, minutes=15)
    headers = {
        "ApiKey": API_KEY,  # API Key nel header
        "Accept": "application/json"
    }
    # Extract parameters from the request
    latitude = request.args.get("latitude", 47, type=float)  # Default to 47 if not provided
    longitude = request.args.get("longitude", 7, type=float)  # Default to 7 if not provided

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "startDate": time - delta_15_minutes,
        "endDate": time,
        "modelId": "TarSpot",
        "format": "json"
    }
    try:
        response = requests.get(url, headers=headers, params=parameters, timeout=10)
        response.raise_for_status()  # Lancia un errore se lo status code non è 200
        result = {"value": entry["value"] for entry in response.json()}

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}, status=500)


@app.route("/send_alert", methods=["POST"])
def send_alert():
    """Receives the alert from the frontend and returns a confirmation."""
    alert_data = request.json  # Get the alert data sent from the frontend
    print(f"Received alert: {alert_data['message']} at {alert_data['coordinates']}")
    # Here you can update your backend data or log the alert
    return jsonify({"status": "success", "message": "Alert received and logged."})


@app.route("/get_soil_params", methods=["GET"])
def get_soil_params():
    url = "https://services.cehub.syngenta-ais.com/api/Forecast/ShortRangeForecastHourly"
    time = datetime.datetime.now()
    delta_60_minutes = datetime.timedelta(hours=0, minutes=60)
    headers = {
        "ApiKey": API_KEY,  # API Key nel header
        "Accept": "application/json"
    }
    # Extract parameters from the request
    latitude = request.args.get("latitude", 47, type=float)  # Default to 47 if not provided
    longitude = request.args.get("longitude", 7, type=float)  # Default to 7 if not provided

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "startDate": time - delta_60_minutes,
        "endDate": time,
        "measureLabel": "Soilmoisture_0to10cm_Hourly (vol%);"
                        "Soiltemperature_0to10cm_Hourly (C);",
        "suppler": "Meteoblue",
        "format": "json"
    }
    try:
        response = requests.get(url, headers=headers, params=parameters, timeout=10)
        print(response.json())
        response.raise_for_status()  # Lancia un errore se lo status code non è 200
        result = {entry["measureLabel"].split(" ")[0]: entry["value"] for entry in response.json()}

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}, status=500)


@app.route("/get_status", methods=["GET"])
def get_status():
    url = "https://services.cehub.syngenta-ais.com/api/Forecast/Nowcast"
    time = datetime.datetime.now()
    delta_15_minutes = datetime.timedelta(hours=0, minutes=15)
    headers = {
        "ApiKey": API_KEY,  # API Key nel header
        "Accept": "application/json"
    }

    # Extract parameters from the request
    latitude = request.args.get("latitude", 47, type=float)  # Default to 47 if not provided
    longitude = request.args.get("longitude", 7, type=float)  # Default to 7 if not provided

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "startDate": time - delta_15_minutes,
        "endDate": time,
        "measureLabel": "Temperature_15Min (C);"
                        "WindSpeed_15Min (m/s);"
                        "WindDirection_15Min;"
                        "HumidityRel_15Min (pct);"
                        "Airpressure_15Min (hPa)",
        "suppler": "Meteoblue",
        "format": "json"
    }
    try:
        response = requests.get(url, headers=headers,params=parameters, timeout=10)
        response.raise_for_status()  # Lancia un errore se lo status code non è 200
        result = {entry["measureLabel"].split(" ")[0]: entry["value"] for entry in response.json()}

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}, status=500)


if __name__ == "__main__":
    app.run(debug=True)
