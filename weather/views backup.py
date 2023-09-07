import datetime

from django.shortcuts import render
import requests 

# Create your views here.
def Weather(request):
    API_KEY = open("D:\BTech CSE Sem4\Python\Group Project\weatherproject\API_KEY","r").read()

    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"

    if request.method == "POST":
        city=request.POST.get('city')

        weather_data = fetch_weather_and_forecast(city, API_KEY, current_weather_url)
            
        context = {
            'weather_data':weather_data,
        }
        
        return render(request,"weather_app/Weather.html",context)         
        
    else :
        return render(request,"weather_app/Weather.html")
    

    
def compareWeather(request):
    API_KEY = open("D:\BTech CSE Sem4\Python\Group Project\weatherproject\API_KEY","r").read()
    # current_weather_url = f"https://api.openweathermap.org/data/3.0/weather?q={}&appid={API_KEY}"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"

    if request.method == "POST":
        city1=request.POST.get('city1')
        city2=request.POST.get('city2',None)

        # weather_data1 , daily_forecast1= fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)
        weather_data1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url)
        
        if city2 :
            # weather_data2 , daily_forecast2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
            weather_data2  = fetch_weather_and_forecast(city2, API_KEY, current_weather_url)
        else:
            weather_data2 , daily_forecast2 = None , None
            
        context = {
            'weather_data1':weather_data1,
            'weather_data2' : weather_data2,
        }
        
        return render(request,"weather_app/compareWeather.html",context)         
        
    else :
        return render(request,"weather_app/compareWeather.html")
    


def fetch_weather_and_forecast(city,api_key,current_weather_url):
    # lat,lon = response[0]["lat"],response['coord']['lon']
    latlon = requests.get("http://api.openweathermap.org/geo/1.0/direct?q={}&appid={}".format(city,api_key)).json()
    lat,lon = latlon[0]["lat"], latlon[0]['lon']
    response = requests.get(current_weather_url.format(lat,lon,api_key)).json()
    
    # forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    
    weather_data = {
        "city" : city.capitalize(),
        "temperature" : round(response['main']['temp']-273.15,2),
        "description" : response['weather'][0]['description'],
        'icon':response['weather'][0]['icon']
    }
    
    # daily_forecast = []
    # for daily_data in forecast_response['daily'][:5]:
    #     daily_forecast.append({
    #         'day':datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
    #         'min_temp' : round(daily_data['temp']['min'] - 273.15 , 2),
    #         'max_temp' : round(daily_data['temp']['max'] - 273.15 , 2),
    #         'description' : daily_data['weather'][0]['description'],
    #         'icon':daily_data['weather'][0]['icon']
    #     })
        
    return weather_data #, daily_forecast