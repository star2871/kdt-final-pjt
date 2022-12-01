import json
import os

# django를 다루기 위해 경로 설정 (정확하지 않음)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PJT.settings")

# django 모델 다루기 위해 import (정확하지 않음)
import django

django.setup()

# 모델 DB를 다루기 위해 import
from countries.models import Country_news

# json 파일 저장 위치
BASE_DIR = "crawling/"

with open(os.path.join("news2.json"), "r", encoding="UTF-8") as json_file:
    json_file = json.load(json_file)
    a = json_file
    for s in a:
        
        p = Country_news(
            country_code=s.get("country_code"),
            title=s.get("title"),
            url=s.get("url"),    
        )
        p.save()  # 저장