import datetime
from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def Weather(request):
    API_KEY = open("C:\\Users\\Thinkbook 13s G2\\Desktop\\weatherproject\\API_KEY", "r").read()
    current_weather_url = "https://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no"

    if request.method == "POST":
        city = request.POST.get('city')

        weather_data = fetch_weather_and_forecast(city, API_KEY, current_weather_url)

        if weather_data is None:
            error_message = "City not found. Please check the spelling or try another city."
            context = {'error_message': error_message}
            return render(request, "weather_app/Weather.html", context)

        context = {'weather_data': weather_data}
        return render(request, "weather_app/Weather.html", context)
    else:
        return render(request, "weather_app/Weather.html")


@login_required(login_url='login')
def compareWeather(request):
    API_KEY = open("C:\\Users\\Thinkbook 13s G2\\Desktop\\weatherproject\\API_KEY","r").read()
    current_weather_url = "https://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no"

    if request.method == "POST":
        city1 = request.POST.get('city1')
        city2 = request.POST.get('city2', None)

        # Data For 1st City
        weather_data1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url)

        if weather_data1 is None:
            error_message = "City 1 not found. Please check the spelling or try another city."
            context = {'error_message': error_message}
            return render(request, "weather_app/compareWeather.html", context)

        # Data For 2nd City
        weather_data2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url)
        if weather_data2 is None:
            error_message = "City 2 not found. Please check the spelling or try another city."
            context = {'error_message': error_message}
            return render(request, "weather_app/compareWeather.html", context)

        context = {
            'weather_data1': weather_data1,
            'weather_data2': weather_data2,
        }

        return render(request, "weather_app/compareWeather.html", context)
    else:
        return render(request, "weather_app/compareWeather.html")

def fetch_weather_and_forecast(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(api_key, city)).json()

    if "error" in response:
        return None  # City not found or other error

    weather_data = {
        "city": city.capitalize(),
        "temperature": response['current']['temp_c'],
        "description": response['current']["condition"]['text'],
        'icon': response['current']["condition"]['icon']
    }

    return weather_data
