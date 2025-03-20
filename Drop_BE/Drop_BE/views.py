from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
import requests
import random
import time


API_KEY = "c4d67afa-6289-4a54-9a05-880b7069469c"

FAKE_ALERTS = {
    "⚠ High soil moisture detected!": "Try Syngenta’s biologicals to improve soil health and moisture retention.",
    "🔥 Possible fire hazard nearby!": "Use Syngenta's solutions to create fire-resistant crops and reduce risk.",
    "💨 Strong winds approaching the farm!": "Consider Syngenta's windbreak products to protect your crops.",
    "🌧 Heavy rainfall expected soon!": "Protect your crops from excess water with Syngenta’s rain-tolerant biologicals.",
    "🐛 Pest infestation detected in Zone 3!": "Use Syngenta’s biological pest control solutions to safely eliminate pests."
}


def homepage(request):
    return render(request, 'index.html')


def get_status(request: HttpRequest):
    url = "https://services.cehub.syngenta-ais.com/api/Forecast/ShortRangeForecastHourly"
    headers = {
        "ApiKey": API_KEY,  # API Key nel header
        "Accept": "application/json"
    }
    parameters = {
        "latitude": 47,
        "longitude": 7,
        "startDate": "2025-03-20",
        "endDate": "2025-03-20",
        "suppler": "Meteoblue",
        "mesureLabel": "HumidityRel_Hourly (pct);"
                       "PrecipProbability_Hourly (pct);"
                       "ShowerProbability_Hourly (pct);"
                       "Soilmoisture_0to10cm_Hourly (vol%);"
                       "Soiltemperature_0to10cm_Hourly (C)",
        "format": "json"
    }
    try:
        response = requests.get(url, headers=headers,params=parameters, timeout=10)
        response.raise_for_status()  # Lancia un errore se lo status code non è 200

        return JsonResponse(response.json(), safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_notification(request: HttpRequest):
    """Returns a random fictitious notification with a solution."""
    fake_alert = random.choice(list(FAKE_ALERTS.keys()))
    solution = FAKE_ALERTS[fake_alert]
    timestamp = time.strftime("%H:%M:%S")  # Add a timestamp
    return JsonResponse({
        "problem": f"{timestamp} - {fake_alert}",
        "solution": solution
    })