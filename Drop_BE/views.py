from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
import requests


API_KEY = "c4d67afa-6289-4a54-9a05-880b7069469c"

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
