from django.urls import path
from . import views

urlpatterns = [
    path('',views.Weather,name="Home"),
    path('compare/',views.compareWeather,name="compareWeather"),
]
