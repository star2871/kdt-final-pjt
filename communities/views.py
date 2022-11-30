
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, TipForm
from .models import Article, Country
from django.shortcuts import render
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime
# 구글 캘린더 API 서비스 객체 생성
from googleapiclient.discovery import build


creds_filename = 'credentials.json'

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Create your views here.
## 리뷰 파트
## 리뷰 인덱스
def review(request, country_code):
    articles = Article.objects.filter(category="review").order_by("-pk")
    context = {
        "articles": articles
    }
    return render(request, 'communities/index.html', context)

## 리뷰 생성
def review_create(request, country_code):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            country = Country.objects.get(country_code=country_code)
            article = article_form.save(commit=False)
            article.country = country
            article.category = "review"
            article.travel_start = request.POST["start"]
            article.travel_end = request.POST["end"]
            article.save()
            return redirect('communities:review', country_code)
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'communities/form.html', context=context)

## 리뷰 상세보기
def review_detail(request, article_pk, country_code):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'article': article,
        'country_code': country_code,
    }
    return render(request, 'communities/detail.html', context)

## 리뷰 삭제
def review_delete(request, article_pk, country_code):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == "POST":
            article.delete()
            return redirect("communities:review", country_code)
    return redirect("communities:review_detail", article_pk, country_code)

## 리뷰 수정
def review_update(request, article_pk, country_code):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid:
                article_ = form.save(commit=False)
                country = Country.objects.get(country_code=country_code)
                article_.country = country
                article_.category = "review"
                article_.travel_start = request.POST["start"]
                article_.travel_end = request.POST["end"]
                article_.save()
                return redirect("communities:review_detail", country_code, article_pk)
        else:
            form = ArticleForm(instance=article)
        context = {
            "article": article,
            "article_form": form,
        }
        return render(request, "communities/form.html", context)
    return redirect("communities:review_detail", country_code, article_pk)


## 꿀팁 파트
## 꿀팁 인덱스
def tip(request, country_code):
    articles = Article.objects.filter(category="tip").order_by("-pk")
    context = {
        "articles": articles
    }
    return render(request, 'communities/index.html', context)

## 꿀팁 생성
def tip_create(request, country_code):
    if request.method == 'POST':
        article_form = TipForm(request.POST, request.FILES)
        if article_form.is_valid():
            country = Country.objects.get(country_code=country_code)
            article = article_form.save(commit=False)
            article.country = country
            article.category = "tip"
            article.save()
            return redirect('communities:review', country_code)
    else:
        article_form = TipForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'communities/form.html', context=context)



def calendar(request):
    flow = InstalledAppFlow.from_client_secrets_file(creds_filename, SCOPES)
    creds = flow.run_local_server(port=0)

    today = datetime.date.today().isoformat()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'itsplay의 OpenAPI 수업',  # 일정 제목
        'location': '서울특별시 성북구 정릉동 정릉로 77',  # 일정 장소
        'description': 'itsplay와 OpenAPI 수업에 대한 설명입니다.',  # 일정 설명
        'start': {  # 시작 날짜
            'dateTime': today + 'T09:00:00',
            'timeZone': 'Asia/Seoul',
        },
        'end': {  # 종료 날짜
            'dateTime': today + 'T10:00:00',
            'timeZone': 'Asia/Seoul',
        },
        'recurrence': [  # 반복 지정
            'RRULE:FREQ=DAILY;COUNT=2'  # 일단위; 총 2번 반복
        ],
        'attendees': [  # 참석자
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {  # 알림 설정
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # 24 * 60분 = 하루 전 알림
                {'method': 'popup', 'minutes': 10},  # 10분 전 알림
            ],
        },
    }

    # calendarId : 캘린더 ID. primary이 기본 값입니다.
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

    return render(request, 'communities/test.html')