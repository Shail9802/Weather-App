import datetime

from django.shortcuts import render
import requests 

# Create your views here.
def forecast(request):
    API_KEY = open("D:\BTech CSE Sem4\Python\Group Project\weatherproject\API_KEY","r").read()
    forecast_url = "https://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=3&aqi=no&alerts=no"

    if request.method == "POST":
        city=request.POST.get('city')

        daily_forecast = fetch_forecast(city, API_KEY, forecast_url)
        
        if daily_forecast==None:
            errorMessage = "City not found ! Please Check Your Spelling "
            context = {"errorMessage":errorMessage}
            return render(request,"weather_app/forecast.html",context)
        
        context = {
            "city": city.capitalize(),
            'daily_forecast':daily_forecast,
        }
        
        # return render(request,"weather_app/forecast.html",context)         
        return render(request,"weather_app/forecast.html",context)         
        
    else :
        # return render(request,"weather_app/forecast.html")
        return render(request,"weather_app/forecast.html")         
    
    
def forecastCompare(request):
    API_KEY = open("D:\BTech CSE Sem4\Python\Group Project\weatherproject\API_KEY","r").read()
    forecast_url = "https://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=3&aqi=no&alerts=no"

    if request.method == "POST":
        city1=request.POST.get('city1')
        city2=request.POST.get('city2')

        daily_forecast1 = fetch_forecast(city1, API_KEY, forecast_url)
        if daily_forecast1==None:
            errorMessage = "City 1 not found ! Please Check Your Spelling "
            context = {"errorMessage":errorMessage}
            return render(request,"weather_app/forecastCompare.html",context)         
            
        daily_forecast2 = fetch_forecast(city2, API_KEY, forecast_url)
        if daily_forecast2==None:
            errorMessage = "City 2 not found ! Please Check Your Spelling "
            context = {"errorMessage":errorMessage}
            return render(request,"weather_app/forecastCompare.html",context)         
            
        context = {
            'daily_forecast1':daily_forecast1,
            'daily_forecast2':daily_forecast2,
            'city1':city1.capitalize(),
            'city2':city2.capitalize(),
        }
        
        # return render(request,"weather_app/forecast.html",context)         
        return render(request,"weather_app/forecastCompare.html",context)         
        
    else :
        # return render(request,"weather_app/forecast.html")
        return render(request,"weather_app/forecastCompare.html") 
    
    
def fetch_forecast(city,api_key,forecast_url):
    
    response = requests.get(forecast_url.format(api_key,city)).json()
    if "error" in response:
        return None  # City not found or other error

    daily_forecast_data = []
    
    for daily_data in response['forecast']['forecastday']:
        daily_forecast_data.append({
            'city': city.capitalize(),
            'date': daily_data['date'],
            'max_temp': daily_data["day"]['maxtemp_c'],
            'min_temp' : daily_data["day"]["mintemp_c"],
            'condition_text': daily_data["day"]['condition']['text'],
            'icon':daily_data["day"]['condition']['icon']
            })
        
    return  daily_forecast_data