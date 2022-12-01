from django.shortcuts import render
from .models import Country, Country_news
import requests
def index(request):
    countries = Country.objects.all()
    return render(request, 'countries/index.html', {'countries': countries})

def country_detail_view(request, country_code):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=8b2ecb443e51f61ba8afcf78c940e833&units=metric&lang=kr'
    if country_code == "JP":
        city1 = 'Tokyo'
        city2 = 'Osaka'
    elif country_code == "GB":
        city1 = 'London'
        city2 = 'Liverpool'
    elif country_code == "US":
        city1 = 'Los angeles'
        city2 = 'New York'
    elif country_code == "ES":
        city1 = 'Madrid'
        city2 = 'Barcelona'
    elif country_code == "AU":
        city1 = 'Canberra'
        city2 = 'Sydney'

    city_weather1 = requests.get(url.format(city1)).json() #request the API data and convert the JSON to Python data types
    city_weather2 = requests.get(url.format(city2)).json()
    weather = {
        'city1' : city1,
        'temperature1' : city_weather1['main']['temp'],
        'description1' : city_weather1['weather'][0]['description'],
        'icon1' : city_weather1['weather'][0]['icon'],
        'city2' : city2,
        'temperature2' : city_weather2['main']['temp'],
        'description2' : city_weather2['weather'][0]['description'],
        'icon2' : city_weather2['weather'][0]['icon'],
    }
    country = Country.objects.get(country_code=country_code)
    country_news = Country_news.objects.filter(country_code=country_code)
    return render(request , 'countries/detail.html', {'country': country,
    'country_news': country_news,'city_weather1':city_weather1, 'city_weather2':city_weather2,'weather':weather,})
