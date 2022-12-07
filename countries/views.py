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
    
    # api = "https://api.exchangeratesapi.io/v1/latest?access_key=4uRZaoBihyNtPoOeHE9VM0YACEGJEUUM&base=KRW&symbols=GBP,JPY,EUR,USD,AUD"
    # if country_code == "JP":
    #     rates = "JPY"
    # elif country_code == 'US':
    #     rates = "USD"
    # elif country_code == 'AU':
    #     rates = "AUD"
    # elif country_code == 'GB':
    #     rates = "GBP"
    # elif country_code == 'ES':
    #     rates = "EUR"    
    url = "https://api.apilayer.com/exchangerates_data/2022-12-07&base=KRW"
    # url ='https://api.exchangeratesapi.io/v1/latest?access_key=4uRZaoBihyNtPoOeHE9VM0YACEGJEUUM&base=KRW'
    
    
    headers = {
        "apikey":'4uRZaoBihyNtPoOeHE9VM0YACEGJEUUM'
    }
    response = requests.get(url, headers=headers).json()
    exchange_code = ''
    if country_code == "JP":
        exchange_code = '엔'
        response['rates']=response['rates']['JPY']
    elif country_code == 'US':
        exchange_code = '달러'
        response['rates']=response['rates']['USD']
    elif country_code == 'AU':
        exchange_code = '호주달러'
        response['rates']=response['rates']["AUD"]
    elif country_code == 'GB':
        exchange_code = '파운드'
        response['rates']=response['rates']["GBP"]
    elif country_code == 'ES':
        exchange_code = '유로'
        response['rates']=response['rates']["EUR"]
    # status_code = response.status_code
    # # if country_code == "JP":
    # #     symbols = "JPY"
    # # elif country_code == 'US':
    # #     symbols = "USD"
    # # elif country_code == 'AU':
    # #     symbols = "AUD"
    # # elif country_code == 'GB':
    # #     symbols = "GBP"
    # # elif country_code == 'ES':
    # #     symbols = "EUR"
    # result = response.text
        print(response['rates'])
    
    exchange = {
        'base_country': response['base'],
        'country_exchange' : response['rates'],
        'exchange_code' : exchange_code,
        # 'country_exchange_US' : response['rates']['USD'],
        # 'country_exchange_AU' : response['rates']['AUD'],
        # 'country_exchange_GB' : response['rates']['GBP'],
        # 'country_exchange_ES' : response['rates']['EUR'],
    }
    # if country_code == "JP":
    #     symbols = "JPY"
    # elif country_code == 'US':
    #     symbols = "USD"
    # elif country_code == 'AU':
    #     symbols = "AUD"
    # elif country_code == 'GB':
    #     symbols = "GBP"
    # elif country_code == 'ES':
    #     symbols = "EUR"
    # exchange = result.format(symbols)
    # if country_code == "JP":
    #     symbols = "JPY"
    # elif country_code == 'US':
    #     symbols = "USD"
    # elif country_code == 'AU':
    #     symbols = "AUD"
    # elif country_code == 'GB':
    #     symbols = "GBP"
    # elif country_code == 'ES':
    #     symbols = "EUR"
    # exchange = result.get(url.format(symbols)).json()
    # if country_code == "JP":
    #     print(result['rates']['JPY'])
    # elif country_code == 'US':
    #     rates = "USD"
    # elif country_code == 'AU':
    #     rates = "AUD"
    # elif country_code == 'GB':
    #     rates = "GBP"
    # elif country_code == 'ES':
    #     rates = "EUR"
    
        
    # c['cur_nm']
    # c['deal_bas_r']
    # c['ttb']
    # c['tts']
   
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
    # exchange = {
    #     'country_exchange': country_exchange,
        # 'cur_unit1' : c['cur_unit'],
        # 'cur_nm1': c['cur_nm'],
        # 'deal_bas_r1': c['deal_bas_r'],
        # 'ttb1': c['ttb'],
        # 'tts1': c['tts'],
        # 'cur_unit2' : d['cur_unit'],
        # 'cur_nm2': d['cur_nm'],
        # 'deal_bas_r2': d['deal_bas_r'],
        # 'ttb2': d['ttb'],
        # 'tts2': d['tts'],
    # }
    
# for a in weather:
#     print('time1')
    country = Country.objects.get(country_code=country_code)
    country_news = Country_news.objects.filter(country_code=country_code)
    return render(request , 'countries/detail.html', {'country': country,
    'country_news': country_news,'city_weather1':city_weather1, 'city_weather2':city_weather2,'weather':weather, 'headers': headers, 'exchange': exchange,'exchange_code': exchange_code,})
