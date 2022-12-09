from django.shortcuts import render
from .models import Country, Country_news, Festival
import requests
from datetime import datetime
from pytz import timezone
def index(request):
    countries = Country.objects.all()
    return render(request, 'countries/index.html', {'countries': countries,})

def country_detail_view(request, country_code):
    # 날씨
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
    

    list_day1=[]
    list_temp1=[]
    list_des1=[]
    list_icon1=[]
    for a in city_weather1['list']:
        list_day1.append(a['dt_txt'])
        list_temp1.append(a['main']['temp'])
        list_des1.append(a['weather'][0]['description'])
        list_icon1.append(a['weather'][0]['icon'])
     
    list_day2=[]
    list_temp2=[]
    list_des2=[]
    list_icon2=[]
    for b in city_weather2['list']:
        list_day2.append(b['dt_txt'])
        list_temp2.append(b['main']['temp'])
        list_des2.append(b['weather'][0]['description'])
        list_icon2.append(b['weather'][0]['icon'])
    weather = {
        
        'city1' : city_weather1['city']['name'],
        'time1' : list_day1,
        'temperature1' : list_temp1,
        'description1' : list_des1,
        'icon1' : list_icon1,
        
        'city2' : city_weather2['city']['name'],
        'time2' : list_day2,
        'temperature2' : list_temp2,
        'description2' : list_des2,
        'icon2' : list_icon2,
    }
    # 환율 
    # 나중에 발표할때 날짜 바꿔야 한다, 또한 250번만 가져올 수있으므로 api_key를 다시 받아야한다.
    # url = "https://api.apilayer.com/exchangerates_data/2022-12-07&base=KRW"
   
    # headers = {
    #     "apikey":'4uRZaoBihyNtPoOeHE9VM0YACEGJEUUM'
    # }
    # response = requests.get(url, headers=headers).json()
    # exchange_code = ''
    # if country_code == "JP":
    #     exchange_code = '엔'
    #     response['rates']=response['rates']['JPY']
    # elif country_code == 'US':
    #     exchange_code = '달러'
    #     response['rates']=response['rates']['USD']
    # elif country_code == 'AU':
    #     exchange_code = '호주달러'
    #     response['rates']=response['rates']["AUD"]
    # elif country_code == 'GB':
    #     exchange_code = '파운드'
    #     response['rates']=response['rates']["GBP"]
    # elif country_code == 'ES':
    #     exchange_code = '유로'
    #     response['rates']=response['rates']["EUR"]


    
    # exchange = {
    #     'base_country': response['base'],
    #     'country_exchange' : response['rates'],
    #     'exchange_code' : exchange_code,
    # }
    # 실시간 나라별 현지 시간
    한국 = datetime.now(timezone('Asia/Seoul')).strftime('%Y/%m/%d %p %I:%M:%S')
    country_time1 = []
    country_time2 = []
    if country_code == 'US':
        country_time1 = ['LA시간', datetime.now(timezone('America/Los_Angeles')).strftime('%Y/%m/%d %p %I:%M:%S')]
        country_time2 = ['뉴욕시간', datetime.now(timezone('America/Atikokan')).strftime('%Y/%m/%d %p %I:%M:%S')]
    elif country_code == 'GB':   
        country_time1 = ['영국시간', datetime.now(timezone('Atlantic/Reykjavik')).strftime('%Y/%m/%d %p %I:%M:%S')]
    elif country_code == 'JP':
        country_time1 = ['일본시간', datetime.now(timezone('Asia/Tokyo')).strftime('%Y/%m/%d %p %I:%M:%S')]
    elif country_code == 'AU':
        country_time1 = ['호주시간', datetime.now(timezone('Australia/ACT')).strftime('%Y/%m/%d %p %I:%M:%S')]

    
    
    festivals = Festival.objects.all()
    country = Country.objects.get(country_code=country_code)
    country_news = Country_news.objects.filter(country_code=country_code)
    return render(request , 'countries/detail.html', {'country': country,
    'country_news': country_news,'city_weather1':city_weather1, 'city_weather2':city_weather2,'weather':weather,'country_time1':country_time1,'한국':한국, 'country_time2' : country_time2, 'festivals': festivals})
    # 'headers': headers, 'exchange': exchange, 'exchange_code': exchange_code,