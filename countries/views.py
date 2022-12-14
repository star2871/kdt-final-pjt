from django.shortcuts import render
from .models import Country, Country_news, Festival
import requests

def index(request):
    countries = Country.objects.all()
    return render(request, 'countries/index.html', {'countries': countries})

def country_detail_view(request, country_code):
    # 날씨
    url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid=8b2ecb443e51f61ba8afcf78c940e833&units=metric&lang=kr'
    if country_code == "JP":
        city1 = 'Tokyo'
        city2 = 'Osaka'
        city3 = 'Okinawa'
    elif country_code == "GB":
        city1 = 'London'
        city2 = 'Liverpool'
        city3 = 'Manchester'
    elif country_code == "US":
        city1 = 'New jersey'
        city2 = 'New York'
        city3 = 'Boston'
    elif country_code == "ES":
        city1 = 'Madrid'
        city2 = 'Barcelona'
        city3 = 'Valencia'
    elif country_code == "AU":
        city1 = 'Canberra'
        city2 = 'Sydney'
        city3 = 'Brisbane'
    city_weather1 = requests.get(url.format(city1)).json() #request the API data and convert the JSON to Python data types
    city_weather2 = requests.get(url.format(city2)).json()
    city_weather3 = requests.get(url.format(city3)).json()


    list_day1=[]
    list_temp1=[]
    list_icon1=[]
    for a in city_weather1['list']:
        list_day1.append(a['dt_txt'])
        list_temp1.append(a['main']['temp'])
        list_icon1.append(a['weather'][0]['icon'])


    list_day2=[]
    list_temp2=[]
    list_icon2=[]
    for b in city_weather2['list']:
        list_day2.append(b['dt_txt'])
        list_temp2.append(b['main']['temp'])
        list_icon2.append(b['weather'][0]['icon'])


    list_day3=[]
    list_temp3=[]
    list_icon3=[]
    for c in city_weather3['list']:
        list_day3.append(c['dt_txt'])
        list_temp3.append(c['main']['temp'])
        list_icon3.append(c['weather'][0]['icon'])


    weather = {
        
        'city1' : city_weather1['city']['name'],
        'time1' : list_day1,
        'temperature1' : list_temp1,
        'icon1' : list_icon1,
        
        'city2' : city_weather2['city']['name'],
        'time2' : list_day2,
        'temperature2' : list_temp2,
        'icon2' : list_icon2,

        'city3' : city_weather3['city']['name'],
        'time3' : list_day3,
        'temperature3' : list_temp3,
        'icon3' : list_icon3,       
    }
    # 환율 
    # url에서 나중에 발표할때 날짜 바꿔야 한다, 또한 250번만 가져올 수있으므로 api_key를 다시 받아야한다.
    url = "https://api.apilayer.com/exchangerates_data/2022-12-13&base=KRW"
   
    headers = {
        "apikey":'4uRZaoBihyNtPoOeHE9VM0YACEGJEUUM'
    }
    response = requests.get(url, headers=headers).json()
    exchange_code = ''
    if country_code == "JP":
        exchange_code = '엔'
        response['rates']=100/response['rates']['JPY']
        100/response['rates']
    elif country_code == 'US':
        exchange_code = '달러'
        response['rates']=1/response['rates']['USD']
        1/response['rates']
    elif country_code == 'AU':
        exchange_code = '호주달러'
        response['rates']=1/response['rates']["AUD"]
        1/response['rates']
    elif country_code == 'GB':
        exchange_code = '파운드'
        response['rates']=1/response['rates']["GBP"]
        1/response['rates']
    elif country_code == 'ES':
        exchange_code = '유로'
        response['rates']=1/response['rates']["EUR"]
        1/response['rates']

    
    exchange = {
        'base_country': response['base'],
        'country_exchange' : response['rates'],
        'exchange_code' : exchange_code,
    }
    
    festivals = Festival.objects.filter(country__country_code=country_code,).order_by("-pk")
    country = Country.objects.get(country_code=country_code)
    country_news = Country_news.objects.filter(country_code=country_code)
    return render(request , 'countries/detail.html', {'country': country,
    'country_news': country_news,'city_weather1':city_weather1, 'city_weather2':city_weather2, 'city_weather3':city_weather3, 'weather':weather, 'festivals': festivals, 'exchange': exchange, 'exchange_code': exchange_code,})
    # 환율 넣을때 넣어야 할 부분
    # 'exchange': exchange, 'exchange_code': exchange_code,