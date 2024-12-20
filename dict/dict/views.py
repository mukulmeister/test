from logging import exception

from django.shortcuts import render
import requests
from .forms import InputForm
from datetime import datetime

from decouple import config

key = config('key')



# Define your API key




# Define the complete URL with parameters









Direction = {"N": "North","S": "South","W": "West","E": "East"}


def weather(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            city_details = form.cleaned_data['City']
            weather_url = f"https://api.tomorrow.io/v4/weather/forecast?location={city_details}&apikey={key}"
            headers = {"Accept": "application/json"}

            try:
                response = requests.get(weather_url, headers=headers)

                if response.status_code == 200:
                    weather_details = response.json()
                    timelines = weather_details.get("timelines", {})
                    daily_data = timelines.get("daily", [])

                    processed_data = []
                    for entry in daily_data:
                        time = datetime.fromisoformat(entry["time"].replace("Z", "+00:00"))
                        values = entry.get("values", {})
                        sunrise_time = datetime.fromisoformat(values.get("sunriseTime", "").replace("Z", "+00:00"))
                        sunset_time = datetime.fromisoformat(values.get("sunsetTime", "").replace("Z", "+00:00"))

                        processed_data.append({
                            "date": time.strftime('%Y-%m-%d'),
                            "temperature_avg": values.get("temperatureAvg"),
                            "temperature_max": values.get("temperatureMax"),
                            "temperature_min": values.get("temperatureMin"),
                            "humidity_avg": values.get("humidityAvg"),
                            "wind_speed_avg": values.get("windSpeedAvg"),
                            "sunrise": sunrise_time.strftime('%H:%M') if sunrise_time else "N/A",
                            "sunset": sunset_time.strftime('%H:%M') if sunset_time else "N/A",
                        })

                    return render(request, 'weather_details.html', {"weather_data": processed_data, "city": city_details})

                else:
                    error_message = f"Error: Received status code {response.status_code}. {response.json().get('message', 'Unknown error occurred.')}"
                    return render(request, 'error.html', {"error_message": error_message})

            except requests.RequestException as e:
                error_message = f"Network error: {str(e)}"
                return render(request, 'error.html', {"error_message": error_message})

    else:
        form = InputForm()

    return render(request, 'index.html', {"form": form})

























