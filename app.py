import datetime
import json

from flask import Flask, render_template, jsonify, request
import random
import requests
import time

app = Flask(__name__, static_folder="static")

API_KEY = ""

# Sample alert messages with corresponding solutions
FAKE_ALERTS = {
    "High soil moisture detected!": ("⚠️","Use Syngenta’s Stress Booster"),
    "Heavy rainfall expected soon!": ("🌧️","Use Syngenta’s Stress Booster"),
    "High temperature detected!": ("♨️","Use Syngenta’s Stress Booster"),
    "Pest infestation detected!": ("🐛","Use Syngenta’s Stress Booster"),
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_notification")
def get_notification():
    """Returns a random fictitious notification with a solution."""
    fake_alert = random.choice(list(FAKE_ALERTS.keys()))
    icon, solution = FAKE_ALERTS[fake_alert]
    timestamp = time.strftime("%H:%M:%S")  # Add a timestamp
    like_count = random.randint(0, 200)
    dislike_count = random.randint(0, 200)
    return jsonify({
        "timestamp": timestamp,
        "problem": f"{fake_alert}",
        "icon": icon,
        "solution": solution,
        "like_count": like_count,
        "dislike_count": dislike_count
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
