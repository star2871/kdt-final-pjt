# import http.client, urllib.parse

# conn = http.client.HTTPConnection('api.mediastack.com')

# params = urllib.parse.urlencode({
#     'access_key': '2ce490c56eb2b37e39c6046ebdabd3d3',
#     'categories': '-sports',
#     'sort': 'published_desc',
#     'limit': 10,
#     'keywords': '-worldcup',
#     'languages': 'en',
#     'countries': 'jp'
#     })

# conn.request('GET', '/v1/news?{}'.format(params))

# res = conn.getresponse()
# data = res.read()

# print(data.decode('utf-8'))
# import requests
# import json

# # movieGlu 의 GET filmsNowShowing 받기
# url = "https://api.mediastack.com/news"
# apikey = "2ce490c56eb2b37e39c6046ebdabd3d3"
# params = {   "author": "author",
#                 "title": "Hurricane Hanna makes landfall around 5 p.m. on Saturday.",
#                 "description": "Hurricane Hanna battered southern Texas with sustained winds of 75 mph and continued to deliver heavy rain and flash flooding as it moved inland late Saturday.",
#                 "url": "https://abcnews.go.com/US/hurricane-hanna-makes-landfall-texas/story?id=71985566",
#                 "source": "ABC News",
#                 "image": "https://s.abcnews.com/images/US/hanna-swimmer-mo_hpMain_20200725-163152_2_4x3t_384.jpg",
#                 "category": "general",
#                 "language": "en",
#                 "country": "us",
#                 "published_at": "2020-07-26T01:04:23+00:00"}
# with open('news.json', 'w') as f:
#     json.dump(params, f)

# import http.client, urllib.parse
# import json
# conn = http.client.HTTPConnection('api.mediastack.com')

# params = urllib.parse.urlencode({
#     'access_key': '2ce490c56eb2b37e39c6046ebdabd3d3',
#     'categories': '-general',
#     'sort': 'published_desc',
#     'limit': 10,
#     'countries':'es',
#     })

# conn.request('GET', '/v1/news?{}'.format(params))

# res = conn.getresponse()
# data = res.read()
# # print(data.decode('utf-8'))
# print(data)
import requests
import json

requestData = requests.get('http://api.mediastack.com/v1/news?access_key=b21d51f4c2bbf1dcb7277f91fb87e507&categories=-general&countries=us,jp,es,au,gb')
jsonData = None
if requestData.status_code == 200:
    jsonData = requestData.json()
    a=jsonData.get('data')
    with open('news.json', 'w') as f:
        json.dump(a, f, indent='\t')