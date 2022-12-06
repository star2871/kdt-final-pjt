from django.shortcuts import render
from .models import Country, Country_news
import requests
def index(request):
    countries = Country.objects.all()
    return render(request, 'countries/index.html', {'countries': countries})

def country_detail_view(request, country_code):
    # url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=8b2ecb443e51f61ba8afcf78c940e833&units=metric&lang=kr'
    # if country_code == "JP":
    #     city1 = 'Tokyo'
    #     city2 = 'Osaka'
    # elif country_code == "GB":
    #     city1 = 'London'
    #     city2 = 'Liverpool'
    # elif country_code == "US":
    #     city1 = 'Los angeles'
    #     city2 = 'New York'
    # elif country_code == "ES":
    #     city1 = 'Madrid'
    #     city2 = 'Barcelona'
    # elif country_code == "AU":
    #     city1 = 'Canberra'
    #     city2 = 'Sydney'
    url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid=8b2ecb443e51f61ba8afcf78c940e833&units=metric&lang=kr'
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
    
    # print(city_weather1['city']['name'])
    # a = city_weather1['list']
    list_day1=[]
    list_temp1=[]
    list_des1=[]
    list_icon1=[]
    for a in city_weather1['list']:
        list_day1.append(a['dt_txt'])
        list_temp1.append(a['main']['temp'])
        list_des1.append(a['weather'][0]['description'])
        list_icon1.append(a['weather'][0]['icon'])
        # print(a['dt_txt'])
        # print(a['main']['temp'])
        # print(a['weather'][0]['description'])
        # print(a['weather'][0]['icon'])   
    list_day2=[]
    list_temp2=[]
    list_des2=[]
    list_icon2=[]
    city_weather2['city']['name']
    
    for b in city_weather2['list']:
        list_day2.append(b['dt_txt'])
        list_temp2.append(b['main']['temp'])
        list_des2.append(b['weather'][0]['description'])
        list_icon2.append(b['weather'][0]['icon'])
    weather = {
        # 'list1' : list1,
        'city1' : city_weather1['city']['name'],
        'time1' : list_day1,
        'temperature1' : list_temp1,
        'description1' : list_des1,
        'icon1' : list_icon1,
        # 'list2' : list2,
        'city2' : city_weather2['city']['name'],
        'time2' : list_day2,
        'temperature2' : list_temp2,
        'description2' : list_des2,
        'icon2' : list_icon2,
    }
    api = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=SthDQi9wM06s2PTo8YSafUGNB0b6Mlkj&data=AP01"
    if country_code == "JP":
        cur_unit = "JPY"
    # elif country_code == 'US':
    #     cur_unit = "USD"
    country_exchange = requests.get(api.format(cur_unit)).json()
    for a in country_exchange:
    # 호주
    # for a in country_exchange:
        # # 호주 
        # a = country_exchange[1]
        # # 유로화
        # b = country_exchange[8]
        # # 영국 파운드
        # c = country_exchange[9]
        # # 일본
        # d = country_exchange[12]
        # # 미국
        # e = country_exchange[22]
        # print(a, b, c, d, e)
        exchange = {
            'country_exchange': country_exchange,
            # 'money' : a['kftc_deal_bas_r'],
            # 'cur_nm': a['cur_nm'],
            # 'cur_unit': a['cur_unit'],
            # 'money_jp': d['kftc_deal_bas_r'],
            # 'cur_nm_jp': d['cur_nm'],
        }
        # print(exchange)
# for a in weather:
#     print('time1')
    country = Country.objects.get(country_code=country_code)
    country_news = Country_news.objects.filter(country_code=country_code)
    return render(request , 'countries/detail.html', {'country': country,
    'country_news': country_news,'city_weather1':city_weather1, 'city_weather2':city_weather2,'weather':weather, 'country_exchange':country_exchange,})
