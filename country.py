# import json


# with open("countries_test.json", "r", encoding="utf8") as f:
#     contents = f.read() # string 타입
#     json_data = json.loads(contents)

#     a=json_data[71]['fields']

#     for key, val in a.items():
#         print(key, val)

# print(json_data[165]['fields']['country_name'])

# print(json_data[230]['fields']['country_name'])

# print(json_data[143]['fields']['country_name'])

# print(json_data[116]['fields']['country_name'])
# 전체 JSON을 dict type으로 가져옴
# print(json_data[0]["fields"]['country_name']) # Employee 정보를 조회
# print(json_data["employees"][0]["firstName"]) # 첫 Employee의 이름을 출력 -> John

import json
import os
import sys
import urllib.request
import urllib.parse

# django를 다루기 위해 경로 설정 (정확하지 않음)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PJT.settings")

# django 모델 다루기 위해 import (정확하지 않음)
import django

django.setup()

# 모델 DB를 다루기 위해 import
from countries.models import Country

# json 파일 저장 위치
BASE_DIR = "crawling/"

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
# countries_test.json에서 생성한 데이터 가져오기
with open(os.path.join("countries_test.json"), "r", encoding="UTF-8") as json_file:
    json_file = json.load(json_file)
    a = json_file[165]["fields"]  # 일본
    b = json_file[71]["fields"]  # 미국
    c = json_file[229]["fields"]  # 호주
    d = json_file[116]["fields"]  # 스페인
    e = json_file[143]["fields"]  # 영국
    # for g, data in a.items():
    # Country 테이블 생성
    # for j in data:
    #     print(j)
    # if __name__ == "__main__":

    # Country 모델 형식에 맞춰서 입력
    title = []
    description = []
    result = []

    # 설명 해석에 필요한 언어감지
    for i in range(len(a["events"])):
        encQuery = urllib.parse.quote(a["events"][i]["description"]) # 언어감지, 변역을 위한 설명문 삽입
        if encQuery != "":
            data = "query=" + encQuery
            url = "https://openapi.naver.com/v1/papago/detectLangs"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                response_body = response_body.decode("utf-8")   # bytes 타입으로 날아온 response_body를 utf-8로 디코딩
                response_body = json.loads(response_body)   # Json타입으로 변환하여 데이터 추출이 가능하게 변경
            else:
                print("Error Code:" + rescode)

            # 설명 번역 시작
            # langCode가 빈칸이면 설명이 없다는 뜻이므로 빈칸이 아닐때만 번역 실행
            if response_body["langCode"] != "":
                #  source - 원본 언어
                #  target - 번역 언어
                #  text - 번역할 설명
                data = "source=" + response_body["langCode"] + "&target=ko&text=" + encQuery
                url = "https://openapi.naver.com/v1/papago/n2mt"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if (rescode == 200):
                    response_body = response.read()
                    response_body = response_body.decode("utf-8")
                    response_body = json.loads(response_body)
                    translate = response_body["message"]["result"]["translatedText"]
                    description.append(translate)
                else:
                    print("Error Code:" + rescode)
        # 설명이 빈칸일 경우 해석을 할 필요가 없음(API 실행시 오류 발생)
        # description 배열에 빈값 삽입
        else:
            description.append("")
            continue

    # 파파고 API 활용 축제 이름 해석 시작
    for i in range(len(a["events"])):
        encText = urllib.parse.quote(a["events"][i]["title"]) #축제 이름
        data = "source=en&target=ko&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            response_body = response_body.decode("utf-8")
            response_body = json.loads(response_body)
            fix = str(response_body["message"]["result"]["translatedText"])
            title.append(fix)
        else:
            print("Error Code:" + rescode)

        # 완성된 title과 description을 딕셔너리로 변환하여 리스트에 삽입
        temp={"title": title[i], 'description': description[i]}
        result.append(temp)

    p = Country(
        country_name=a.get("country_name"),
        country_code=a.get("country_code"),
        exchange_rate_code=a.get("exchange_rate_code"),
        status=a.get("status"),
        ysd_er=a.get("ysd_er"),
        cur_nm=a.get("cur_nm"),
        status_wrt_dt=a.get("status_wrt_dt"),
        events=result,
        visa=a.get("visa"),
    )

    p.save()  # 저장
    print('일본 완료')


    language = []
    title = []
    description = []
    result=[]
    for i in range(len(b["events"])):
        encQuery = urllib.parse.quote(b["events"][i]["description"])  # 언어감지를 위한 설명문 삽입
        if encQuery != "":
            data = "query=" + encQuery
            url = "https://openapi.naver.com/v1/papago/detectLangs"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                response_body = response_body.decode("utf-8")
                response_body = json.loads(response_body)
            else:
                print("Error Code:" + rescode)
            if response_body["langCode"] != "":
                data = "source=" + response_body["langCode"] + "&target=ko&text=" + encQuery
                url = "https://openapi.naver.com/v1/papago/n2mt"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if (rescode == 200):
                    response_body = response.read()
                    response_body = response_body.decode("utf-8")
                    response_body = json.loads(response_body)
                    translate = response_body["message"]["result"]["translatedText"]
                    description.append(translate)
                else:
                    print("Error Code:" + rescode)
        else:
            description.append("")
            continue
    for i in range(len(b["events"])):
        encText = urllib.parse.quote(b["events"][i]["title"])
        data = "source=en&target=ko&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            response_body = response_body.decode("utf-8")
            response_body = json.loads(response_body)
            fix = str(response_body["message"]["result"]["translatedText"])
            title.append(fix)
        else:
            print("Error Code:" + rescode)
        temp = {"title": title[i], 'description': description[i]}
        result.append(temp)

    o = Country(
        country_name=b.get("country_name"),
        country_code=b.get("country_code"),
        exchange_rate_code=b.get("exchange_rate_code"),
        status=b.get("status"),
        ysd_er=b.get("ysd_er"),
        cur_nm=b.get("cur_nm"),
        status_wrt_dt=b.get("status_wrt_dt"),
        events=result,
        visa=b.get("visa"),
    )

    o.save()  # 저장
    print('미국 완료')

    title = []
    description = []
    result = []
    for i in range(len(c["events"])):
        encQuery = urllib.parse.quote(c["events"][i]["description"])  # 언어감지를 위한 설명문 삽입
        if encQuery != "":
            data = "query=" + encQuery
            url = "https://openapi.naver.com/v1/papago/detectLangs"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                response_body = response_body.decode("utf-8")
                response_body = json.loads(response_body)
            else:
                print("Error Code:" + rescode)
            if response_body["langCode"] != "":
                data = "source=" + response_body["langCode"] + "&target=ko&text=" + encQuery
                url = "https://openapi.naver.com/v1/papago/n2mt"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if (rescode == 200):
                    response_body = response.read()
                    response_body = response_body.decode("utf-8")
                    response_body = json.loads(response_body)
                    translate = response_body["message"]["result"]["translatedText"]
                    description.append(translate)
                else:
                    print("Error Code:" + rescode)
        else:
            description.append("")
            continue
    for i in range(len(c["events"])):
        encText = urllib.parse.quote(c["events"][i]["title"])
        data = "source=en&target=ko&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            response_body = response_body.decode("utf-8")
            response_body = json.loads(response_body)
            fix = str(response_body["message"]["result"]["translatedText"])
            title.append(fix)
        else:
            print("Error Code:" + rescode)
        temp = {"title": title[i], 'description': description[i]}
        result.append(temp)

    q = Country(
        country_name=c.get("country_name"),
        country_code=c.get("country_code"),
        exchange_rate_code=c.get("exchange_rate_code"),
        status=c.get("status"),
        ysd_er=c.get("ysd_er"),
        cur_nm=c.get("cur_nm"),
        status_wrt_dt=c.get("status_wrt_dt"),
        events=result,
        visa=c.get("visa"),
    )
    q.save()  # 저장
    print('호주 완료')


    title = []
    description = []
    result = []
    for i in range(len(d["events"])):
        encQuery = urllib.parse.quote(d["events"][i]["description"])  # 언어감지를 위한 설명문 삽입
        if encQuery != "":
            data = "query=" + encQuery
            url = "https://openapi.naver.com/v1/papago/detectLangs"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                response_body = response_body.decode("utf-8")
                response_body = json.loads(response_body)
            else:
                print("Error Code:" + rescode)
            if response_body["langCode"] != "":
                data = "source=" + response_body["langCode"] + "&target=ko&text=" + encQuery
                url = "https://openapi.naver.com/v1/papago/n2mt"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if (rescode == 200):
                    response_body = response.read()
                    response_body = response_body.decode("utf-8")
                    response_body = json.loads(response_body)
                    translate = response_body["message"]["result"]["translatedText"]
                    description.append(translate)
                else:
                    print("Error Code:" + rescode)
        else:
            description.append("")
            continue

    for i in range(len(d["events"])):
        encText = urllib.parse.quote(d["events"][i]["title"])
        data = "source=en&target=ko&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            response_body = response_body.decode("utf-8")
            response_body = json.loads(response_body)
            fix = str(response_body["message"]["result"]["translatedText"])
            title.append(fix)
        else:
            print("Error Code:" + rescode)
        temp = {"title": title[i], 'description': description[i]}
        result.append(temp)
    r = Country(
        country_name=d.get("country_name"),
        country_code=d.get("country_code"),
        exchange_rate_code=d.get("exchange_rate_code"),
        status=d.get("status"),
        ysd_er=d.get("ysd_er"),
        cur_nm=d.get("cur_nm"),
        status_wrt_dt=d.get("status_wrt_dt"),
        events=result,
        visa=d.get("visa"),
    )
    r.save()  # 저장
    print("스페인 완료")


    title = []
    description = []
    result = []
    for i in range(len(e["events"])):
        encQuery = urllib.parse.quote(e["events"][i]["description"])  # 언어감지를 위한 설명문 삽입
        if encQuery != "":
            data = "query=" + encQuery
            url = "https://openapi.naver.com/v1/papago/detectLangs"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                response_body = response_body.decode("utf-8")
                response_body = json.loads(response_body)
            else:
                print("Error Code:" + rescode)
            if response_body["langCode"] != "":
                data = "source=" + response_body["langCode"] + "&target=ko&text=" + encQuery
                url = "https://openapi.naver.com/v1/papago/n2mt"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if (rescode == 200):
                    response_body = response.read()
                    response_body = response_body.decode("utf-8")
                    response_body = json.loads(response_body)
                    translate = response_body["message"]["result"]["translatedText"]
                    description.append(translate)
                else:
                    print("Error Code:" + rescode)
        else:
            description.append("")
            continue
    for i in range(len(e["events"])):
        encText = urllib.parse.quote(e["events"][i]["title"])
        data = "source=en&target=ko&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            response_body = response_body.decode("utf-8")
            response_body = json.loads(response_body)
            fix = str(response_body["message"]["result"]["translatedText"])
            title.append(fix)
        else:
            print("Error Code:" + rescode)
        temp = {"title": title[i], 'description': description[i]}
        result.append(temp)
    s = Country(
        country_name=e.get("country_name"),
        country_code=e.get("country_code"),
        exchange_rate_code=e.get("exchange_rate_code"),
        status=e.get("status"),
        ysd_er=e.get("ysd_er"),
        cur_nm=e.get("cur_nm"),
        status_wrt_dt=e.get("status_wrt_dt"),
        events=e.get("events"),
        visa=e.get("visa"),
    )
    s.save()  # 저장
    print("영국 완료")
    print("최종 완료")
