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

# django를 다루기 위해 경로 설정 (정확하지 않음)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PJT.settings")

# django 모델 다루기 위해 import (정확하지 않음)
import django

django.setup()

# 모델 DB를 다루기 위해 import
from countries.models import Country

# json 파일 저장 위치
BASE_DIR = "crawling/"

# countries_test.json에서 생성한 데이터 가져오기
with open(os.path.join("countries_test.json"), "r", encoding="UTF-8") as json_file:
    json_file = json.load(json_file)
    a = json_file[165]["fields"]  # 일본
    b = json_file[71]["fields"]  # 미국
    c = json_file[230]["fields"]  # 홍콩
    d = json_file[116]["fields"]  # 스페인
    e = json_file[143]["fields"]  # 영국
    # for g, data in a.items():
    # Country 테이블 생성
    # for j in data:
    #     print(j)
    # if __name__ == "__main__":

    # Country 모델 형식에 맞춰서 입력
    p = Country(
        country_name=a.get("country_name"),
        country_code=a.get("country_code"),
        exchange_rate_code=a.get("exchange_rate_code"),
        status=a.get("status"),
        ysd_er=a.get("ysd_er"),
        cur_nm=a.get("cur_nm"),
        status_wrt_dt=a.get("status_wrt_dt"),
        events=a.get("events"),
        visa=a.get("visa"),
    )
    p.save()  # 저장

    o = Country(
        country_name=b.get("country_name"),
        country_code=b.get("country_code"),
        exchange_rate_code=b.get("exchange_rate_code"),
        status=b.get("status"),
        ysd_er=b.get("ysd_er"),
        cur_nm=b.get("cur_nm"),
        status_wrt_dt=b.get("status_wrt_dt"),
        events=b.get("events"),
        visa=b.get("visa"),
    )
    o.save()  # 저장

    q = Country(
        country_name=c.get("country_name"),
        country_code=c.get("country_code"),
        exchange_rate_code=c.get("exchange_rate_code"),
        status=c.get("status"),
        ysd_er=c.get("ysd_er"),
        cur_nm=c.get("cur_nm"),
        status_wrt_dt=c.get("status_wrt_dt"),
        events=c.get("events"),
        visa=c.get("visa"),
    )
    q.save()  # 저장

    r = Country(
        country_name=d.get("country_name"),
        country_code=d.get("country_code"),
        exchange_rate_code=d.get("exchange_rate_code"),
        status=d.get("status"),
        ysd_er=d.get("ysd_er"),
        cur_nm=d.get("cur_nm"),
        status_wrt_dt=d.get("status_wrt_dt"),
        events=d.get("events"),
        visa=d.get("visa"),
    )
    r.save()  # 저장

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
