
from django.shortcuts import render, redirect, get_object_or_404
from countries.models import Country
from .forms import ArticleForm, AdviceForm, FeedForm, FeedImageForm, ArticleCommentForm, FeedCommentForm
from .models import Article, Country, Feed, FeedImages, ArticleComment, FeedComment
from accounts.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime
# 구글 캘린더 API 서비스 객체 생성
from googleapiclient.discovery import build
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
import json
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required

creds_filename = 'credentials.json'

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Create your views here.
## 리뷰 파트
## 리뷰 인덱스
def main(request):
    articles = Article.objects.all()
    countries = Country.objects.all()

    context = {
        'articles': articles,
        'countries': countries
    }

    return render(request, 'communities/main.html', context)

def review(request, country_code):
    # 현재 페이지의 국가코드와 동일한 게시물(리뷰) 뽑기
    reviews = Article.objects.filter(country__country_code=country_code, category="review").order_by("-pk")
    # 베스트 게시글
    best_reviews = reviews.annotate(like_count=Count('like_users')).order_by("-like_count")[0:10]
    print(best_reviews)
    context = {
        "articles": reviews,
        "best_articles" : best_reviews,
        "country_code" : country_code,
    }
    return render(request, 'communities/index.html', context)

## 리뷰 생성
def review_create(request, country_code):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            country = Country.objects.get(country_code=country_code)
            article = article_form.save(commit=False)
            article.user = request.user
            article.country = country
            article.category = "review"
            article.travel_start = request.POST["start"]
            article.travel_end = request.POST["end"]
            article.save()
            return redirect('communities:review', country_code)
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form,
        "country_code" : country_code,
    }
    return render(request, 'communities/form.html', context=context)

## 리뷰 상세보기
def detail(request, article_pk, country_code):
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.articlecomment_set.order_by("-pk")
    comment_count = 0

    for comment in comments:
        if comment.parent_id == None:
            comment_count += 1
            
    comment_form = ArticleCommentForm()
    context = {
        'article': article,
        'country_code': country_code,
        'comments' : comments,
        'comment_form': comment_form,
        'comment_count': comment_count,
    }
    return render(request, 'communities/detail.html', context)

## 리뷰 삭제
def delete(request, article_pk, country_code):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == "POST":
            article.delete()
            return redirect("communities:review", country_code)
    return redirect("communities:detail", article_pk, country_code)

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
                return redirect("communities:detail", country_code, article_pk)
        else:
            # 기존 날짜 데이터 가져오기
            article_start = article.travel_start.strftime("%Y-%m-%d")
            article_end = article.travel_end.strftime("%Y-%m-%d")
            form = ArticleForm(instance=article)
            print(article_end)
        context = {
            "article": article,
            "article_form": form,
            "article_start" : article_start,
            "article_end" : article_end,
            'country_code': country_code,
        }
        return render(request, "communities/form.html", context)
    return redirect("communities:review_detail", country_code, article_pk)

## 게시글 댓글 (리뷰, 꿀팁 동일)
## 댓글 생성
def article_comment_create(request, article_pk, country_code):
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = ArticleCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()
        
    comments = ArticleComment.objects.filter(article_id=article_pk).order_by('-pk')
    
    comments_data = []
    for co in comments:
        # 부모 댓글이 없는 댓글만
        if co.parent_id == None:
            img = f'/media/{co.user.profile_image}'
            # 대댓글
            sub_comments = co.articlecomment_set.all()
            
            sub_comments_data = []
            if len(sub_comments):
                for sub in sub_comments:
                    sub_img = f'/media/{sub.user.profile_image}'
                    sub_comments_data.append({
                                'created_string':sub.created_string,
                                'request_user_pk': request.user.pk,
                                'comment_pk': sub.pk,
                                'user_pk': sub.user.pk,
                                'img_url': sub_img,
                                'nick_name':sub.user.nick_name,
                                'content': sub.content,
                                'created_at': sub.created_at,
                                'updated_at': sub.updated_at,
                                'article_id': sub.article_id,
                                'parent': sub.parent.pk                    
                    })
                    
                comments_data.append(
                    {
                        'created_string': co.created_string,
                        'request_user_pk': request.user.pk,
                        'comment_pk': co.pk,
                        'user_pk': co.user.pk,
                        'img_url': img,
                        'nick_name':co.user.nick_name,
                        'content': co.content,
                        'created_at': co.created_at,
                        'updated_at': co.updated_at,
                        'article_id': co.article_id,
                        'secret': co.secret,
                        'like': co.like.count(),
                        'sub_comments_data' : sub_comments_data
                    })
            else:
                    comments_data.append(
                        {
                            'created_string': co.created_string,
                            'request_user_pk': request.user.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url': img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'updated_at': co.updated_at,
                            'article_id': co.article_id,
                            'secret': co.secret,
                            'like': co.like.count(),
                        })
    if comments[0].parent:
        recent_comment = comments[0].parent.pk
        print(recent_comment)
        context = {
            "comments_data" : comments_data,
            "recent_comment" : recent_comment     
        }
    
    else:
        context = {
            'comments_data': comments_data,
        }
    return JsonResponse(context)

@login_required
def article_likes(request, country_code, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if not request.user == article.user:
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
            likes = False
        else:
            article.like_users.add(request.user)
            likes = True
    else:
        likes = "confirm"
    return JsonResponse({"likes": likes,
                         "like_count" : article.like_users.count(),
                         })

## 댓글 수정
def article_comment_update(request, article_pk, comment_pk, country_code):
    if request.user.is_authenticated:
        jsonObject = json.loads(request.body)
        comment = ArticleComment.objects.get(pk=comment_pk)
        comment.content = jsonObject.get('content')
        comment.save()

        comments = ArticleComment.objects.filter(article_id=article_pk).order_by('-pk')
        comments_data = []
        
    for co in comments:
        # 부모 댓글이 없는 댓글만
        if co.parent_id == None:
            img = f'/media/{co.user.profile_image}'
            # 대댓글
            sub_comments = co.articlecomment_set.all()
            
            sub_comments_data = []
            if len(sub_comments):
                for sub in sub_comments:
                    sub_img = f'/media/{sub.user.profile_image}'
                    sub_comments_data.append({
                                'created_string':sub.created_string,
                                'request_user_pk': request.user.pk,
                                'comment_pk': sub.pk,
                                'user_pk': sub.user.pk,
                                'img_url': sub_img,
                                'nick_name':sub.user.nick_name,
                                'content': sub.content,
                                'created_at': sub.created_at,
                                'updated_at': sub.updated_at,
                                'article_id': sub.article_id,
                                'parent': sub.parent.pk
                    })
                    
                comments_data.append(
                    {
                        'created_string': co.created_string,
                        'request_user_pk': request.user.pk,
                        'comment_pk': co.pk,
                        'user_pk': co.user.pk,
                        'img_url': img,
                        'nick_name':co.user.nick_name,
                        'content': co.content,
                        'created_at': co.created_at,
                        'updated_at': co.updated_at,
                        'article_id': co.article_id,
                        'secret': co.secret,
                        'like': co.like.count(),
                        'sub_comments_data' : sub_comments_data
                    })
            else:
                    comments_data.append(
                        {
                            'created_string': co.created_string,
                            'request_user_pk': request.user.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url': img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'updated_at': co.updated_at,
                            'article_id': co.article_id,
                            'secret': co.secret,
                            'like': co.like.count(),
                        })
    if comments[0].parent:
        recent_comment = comments[0].parent.pk
        print(recent_comment)
        context = {
            "comments_data" : comments_data,
            "recent_comment" : recent_comment     
        }
    
    else:
        context = {
            'comments_data': comments_data,
        }
    return JsonResponse(context)


## 댓글 삭제
def article_comment_delete(request, article_pk, comment_pk, country_code):
    if request.user.is_authenticated:
        comment = ArticleComment.objects.get(pk=comment_pk)
        comment.delete()

        comments = ArticleComment.objects.filter(article_id=article_pk).order_by('-pk')
        comments_data = []
    for co in comments:
        # 부모 댓글이 없는 댓글만
        if co.parent_id == None:
            img = f'/media/{co.user.profile_image}'
            # 대댓글
            sub_comments = co.articlecomment_set.all()
            
            sub_comments_data = []
            if len(sub_comments):
                for sub in sub_comments:
                    sub_img = f'/media/{sub.user.profile_image}'
                    sub_comments_data.append({
                                'created_string':sub.created_string,
                                'request_user_pk': request.user.pk,
                                'comment_pk': sub.pk,
                                'user_pk': sub.user.pk,
                                'img_url': sub_img,
                                'nick_name':sub.user.nick_name,
                                'content': sub.content,
                                'created_at': sub.created_at,
                                'updated_at': sub.updated_at,
                                'article_id': sub.article_id,
                                'parent': sub.parent.pk                    
                    })
                    
                comments_data.append(
                    {
                        'created_string': co.created_string,
                        'request_user_pk': request.user.pk,
                        'comment_pk': co.pk,
                        'user_pk': co.user.pk,
                        'img_url': img,
                        'nick_name':co.user.nick_name,
                        'content': co.content,
                        'created_at': co.created_at,
                        'updated_at': co.updated_at,
                        'article_id': co.article_id,
                        'secret': co.secret,
                        'like': co.like.count(),
                        'sub_comments_data' : sub_comments_data
                    })
            else:
                    comments_data.append(
                        {
                            'created_string': co.created_string,
                            'request_user_pk': request.user.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url': img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'updated_at': co.updated_at,
                            'article_id': co.article_id,
                            'secret': co.secret,
                            'like': co.like.count(),
                        })
                    
    context = {
        'comments_data': comments_data,
    }
    return JsonResponse(context)

## 대댓글 생성
def article_sub_comment_create(request, article_pk, country_code, comment_pk):
    user = User.objects.get(pk=request.user.pk)
    article = get_object_or_404(Article, pk=article_pk)
    parent = get_object_or_404(ArticleComment, pk=comment_pk)
    comment_form = ArticleCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = user
        comment.parent = parent
        comment.save()

    comments = ArticleComment.objects.filter(article_id=article_pk).order_by('-pk')
    parents = comments.values_list('parent_id', flat=True)
    # print(parents)
    parents_set = set(list(parents))
    # print(parents_set)
    
    comments_data = []
    for co in comments:
        # 부모 댓글이 없는 댓글만
        if co.parent_id == None:
            img = f'/media/{co.user.profile_image}'
            # 대댓글
            sub_comments = co.articlecomment_set.all()
            
            sub_comments_data = []
            if len(sub_comments):
                for sub in sub_comments:
                    sub_img = f'/media/{sub.user.profile_image}'
                    sub_comments_data.append({
                                'created_string':sub.created_string,
                                'request_user_pk': request.user.pk,
                                'comment_pk': sub.pk,
                                'user_pk': sub.user.pk,
                                'img_url': sub_img,
                                'nick_name':sub.user.nick_name,
                                'content': sub.content,
                                'created_at': sub.created_at,
                                'updated_at': sub.updated_at,
                                'article_id': sub.article_id,
                                'parent': sub.parent.pk                    
                    })
                    
                comments_data.append(
                    {
                        'created_string': co.created_string,
                        'request_user_pk': request.user.pk,
                        'comment_pk': co.pk,
                        'user_pk': co.user.pk,
                        'img_url': img,
                        'nick_name':co.user.nick_name,
                        'content': co.content,
                        'created_at': co.created_at,
                        'updated_at': co.updated_at,
                        'article_id': co.article_id,
                        'secret': co.secret,
                        'like': co.like.count(),
                        'sub_comments_data' : sub_comments_data
                    })
            else:
                    comments_data.append(
                        {
                            'created_string': co.created_string,
                            'request_user_pk': request.user.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url': img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'updated_at': co.updated_at,
                            'article_id': co.article_id,
                            'secret': co.secret,
                            'like': co.like.count(),
                        })
    context = {
        'comments_data': comments_data,
        # 'parents_set' : list(parents_set),
    }
    return JsonResponse(context)

@login_required
# def article_sub_comment_update(request, article_pk, comment_pk, country_code):
    
#     if not request.user == comment.user:
#         return HttpResponseForbidden()
    
#     comment = get_object_or_404(ArticleComment, pk=comment_pk)
#     jsonObject = json.loads(request.body)
    
#     if request.user == comment.user:
#         comment.content = jsonObject('content')
#         comment.save()
            
#         comments = ArticleComment.objects.filter(article_id=article_pk).order_by('-pk')
#         comments_data = []
            
#         for comment in comments:
#             if comment.parent_id == None:
#                 img = f'/media/{comment.user.profile_image}'
#                 sub_comments = co.articlecomment_set.all()
               
#                 sub_comments_data = []
#                 if len(sub_comments):
#                     for sub in sub_comments:
#                         sub_img = f'/media/{sub.user.profile_image}'
#                         sub_comments_data.append({
#                                 'created_string':sub.created_string,
#                                 'request_user_pk': request.user.pk,
#                                 'comment_pk': sub.pk,
#                                 'user_pk': sub.user.pk,
#                                 'img_url': sub_img,
#                                 'nick_name':sub.user.nick_name,
#                                 'content': sub.content,
#                                 'created_at': sub.created_at,
#                                 'updated_at': sub.updated_at,
#                                 'article_id': sub.article_id,
#                                 'parent': sub.parent.pk                    
#                     })
                        
#                     comments_data.append(
#                         {
#                             'created_string': co.created_string,
#                             'request_user_pk': request.user.pk,
#                             'comment_pk': co.pk,
#                             'user_pk': co.user.pk,
#                             'img_url': img,
#                             'nick_name':co.user.nick_name,
#                             'content': co.content,
#                             'created_at': co.created_at,
#                             'updated_at': co.updated_at,
#                             'article_id': co.article_id,
#                             'secret': co.secret,
#                             'like': co.like.count(),
#                             'sub_comments_data' : sub_comments_data
#                         })
                            
#                 else:
#                     comments_data.append
#                     (
#                         {'created_string': co.created_string,
#                         'request_user_pk': request.user.pk,
#                         'comment_pk': co.pk,
#                         'user_pk': co.user.pk,
#                         'img_url': img,
#                         'nick_name':co.user.nick_name,
#                         'content': co.content,
#                         'created_at': co.created_at,
#                         'updated_at': co.updated_at,
#                         'article_id': co.article_id,
#                         'secret': co.secret,
#                         'like': co.like.count(),
#                         }
#                         )
#         context = {
#             'comments_data' : comments_data,
#         }
#         return JsonResponse(context)

## 대댓글 삭제
def sub_comment_delete(request, article_pk, comment_pk, country_code):
    comment = get_object_or_404(ArticleComment, pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()
        return redirect("communities:detail", article_pk, country_code)
    return redirect("communities:detail", article_pk, country_code)

## 꿀팁 파트
## 꿀팁 인덱스
def advice(request, country_code):
    advices = Article.objects.filter(country__country_code=country_code, category="advice").order_by("-pk")
    best_advices = advices.annotate(like_count=Count('like_users')).order_by("-like_count")[0:10]
    context = {
        "articles": advices,
        "best_articles" : best_advices,
        "country_code" : country_code,
    }
    return render(request, 'communities/index.html', context)

## 꿀팁 생성
def advice_create(request, country_code):
    if request.method == 'POST':
        article_form = AdviceForm(request.POST, request.FILES)
        if article_form.is_valid():
            country = Country.objects.get(country_code=country_code)
            article = article_form.save(commit=False)
            article.user = request.user
            article.country = country
            article.category = "advice"
            article.save()
            return redirect('communities:advice', country_code)
    else:
        article_form = AdviceForm()
    context = {
        'article_form': article_form,
        "country_code" : country_code,
    }
    return render(request, 'communities/advice_form.html', context=context)

## 리뷰 수정
def advice_update(request, article_pk, country_code):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid:
                article_ = form.save(commit=False)
                country = Country.objects.get(country_code=country_code)
                article_.country = country
                article_.category = "advice"
                article_.save()
                return redirect("communities:detail", country_code, article_pk)
        else:
            form = ArticleForm(instance=article)
        context = {
            "article": article,
            "article_form": form,
            'country_code': country_code,
        }
        return render(request, "communities/advice_form.html", context)
    return redirect("communities:review_detail", country_code, article_pk)

## 피드 파트
## 피드 인덱스
def feed(request, country_code):
    feeds = Feed.objects.filter(country__country_code=country_code, category="feed").order_by("-pk")
    feeds_images = FeedImages.objects.all()
    feed_form = FeedForm()
    feed_comment_form = FeedCommentForm()
    feed_image_form = FeedImageForm()
    context = {
        "feeds": feeds,
        "feeds_images": feeds_images,
        "country_code": country_code,
        "feed_form": feed_form,
        "feed_comment_form": feed_comment_form,
        "feed_image_form": feed_image_form,
    }

    return render(request, 'communities/feed_index.html', context)

## 피드 생성
def feed_create(request, country_code):
    user = User.objects.get(pk=request.user.pk)
    form = FeedForm(request.POST)
    files = request.FILES.getlist("image")
    country = Country.objects.get(country_code=country_code)
    if form.is_valid():
        f = form.save(commit=False)
        f.user = user
        f.country = country
        f.category = "feed"
        f.save()
        for i in files:
            FeedImages.objects.create(feed=f, image=i)
       
        feeds = Feed.objects.all().order_by('-pk')
        
        feeds_data = []
        for feed in feeds:
            img = f'/media/{feed.user.profile_image}'
            comments = feed.feedcomment_set.all()
            comments_data = []
            if len(comments):
                for co in comments:
                    co_img = f'/media/{co.user.profile_image}'
                    comments_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url':co_img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'like': co.like.count(),
                        })
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                            'comments_data' : comments_data
                        })
            else:
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                        })
        context = {
            'feeds_data': feeds_data
        }
        return JsonResponse(context)
    else:
        print(form.errors)

## 피드 삭제
def feed_delete(request, feed_pk, country_code):
    feed = Feed.objects.get(pk=feed_pk)
    user = User.objects.get(pk=request.user.pk)
    if request.user.is_authenticated and user == feed.user:
        feed.delete()

        feeds = Feed.objects.all().order_by('-pk')
        
        feeds_data = []
        for feed in feeds:
            img = f'/media/{feed.user.profile_image}'
            comments = feed.feedcomment_set.all()
            comments_data = []
            if len(comments):
                for co in comments:
                    co_img = f'/media/{co.user.profile_image}'
                    comments_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url':co_img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'like': co.like.count(),
                        })
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                            'comments_data' : comments_data
                        })
            else:
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                        })
        context = {
            'feeds_data': feeds_data
        }
        return JsonResponse(context)


## 피드 수정
def feed_update(request, feed_pk, country_code):
    feed = Feed.objects.get(pk=feed_pk)
    user = User.objects.get(pk=request.user.pk)
    if request.user.is_authenticated and user == feed.user:
        jsonObject = json.loads(request.body)
        feed = Feed.objects.get(pk=feed_pk)
        feed.content = jsonObject.get('content')
        feed.save()

        feeds = Feed.objects.all().order_by('-pk')
        
        feeds_data = []
        for feed in feeds:
            img = f'/media/{feed.user.profile_image}'
            comments = feed.feedcomment_set.all()
            comments_data = []
            if len(comments):
                for co in comments:
                    co_img = f'/media/{co.user.profile_image}'
                    comments_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url':co_img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'like': co.like.count(),
                        })
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                            'comments_data' : comments_data
                        })
            else:
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                        })
        context = {
            'feeds_data': feeds_data
        }
        return JsonResponse(context)

    ## 댓글 생성
def feed_comment_create(request, feed_pk, country_code):
    feed = get_object_or_404(Feed, pk=feed_pk)
    comment_form = FeedCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.feed = feed
        comment.save()
    
        feeds = Feed.objects.all().order_by('-pk')

        feeds_data = []
        for feed in feeds:
            img = f'/media/{feed.user.profile_image}'
            comments = feed.feedcomment_set.all()
            comments_data = []
            if len(comments):
                for co in comments:
                    co_img = f'/media/{co.user.profile_image}'
                    comments_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url':co_img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'like': co.like.count(),
                        })
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                            'comments_data' : comments_data
                        })
            else:
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                        })
        context = {
            'feeds_data': feeds_data
        }
        return JsonResponse(context)

## 댓글 수정
def feed_comment_update(request, feed_pk, comment_pk, country_code):
    if request.user.is_authenticated:
        jsonObject = json.loads(request.body)
        comment = FeedComment.objects.get(pk=comment_pk)
        comment.content = jsonObject.get('content')
        comment.save()

        feeds = Feed.objects.all().order_by('-pk')

        feeds_data = []
        for feed in feeds:
            img = f'/media/{feed.user.profile_image}'
            comments = feed.feedcomment_set.all()
            comments_data = []
            if len(comments):
                for co in comments:
                    co_img = f'/media/{co.user.profile_image}'
                    comments_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url':co_img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'like': co.like.count(),
                        })
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                            'comments_data' : comments_data
                        })
            else:
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                        })
        context = {
            'feeds_data': feeds_data
        }
        return JsonResponse(context)


## 댓글 삭제
def feed_comment_delete(request, feed_pk, comment_pk, country_code):
    if request.user.is_authenticated:
        comment = FeedComment.objects.get(pk=comment_pk)
        comment.delete()

        feeds = Feed.objects.all().order_by('-pk')

        feeds_data = []
        for feed in feeds:
            img = f'/media/{feed.user.profile_image}'
            comments = feed.feedcomment_set.all()
            comments_data = []
            if len(comments):
                for co in comments:
                    co_img = f'/media/{co.user.profile_image}'
                    comments_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'comment_pk': co.pk,
                            'user_pk': co.user.pk,
                            'img_url':co_img,
                            'nick_name':co.user.nick_name,
                            'content': co.content,
                            'created_at': co.created_at,
                            'like': co.like.count(),
                        })
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                            'comments_data' : comments_data
                        })
            else:
                feeds_data.append(
                        {
                            'created_string': feed.created_string,
                            'request_user_pk': request.user.pk,
                            'feed_pk': feed.pk,
                            'user_pk': feed.user.pk,
                            'img_url':img,
                            'nick_name':feed.user.nick_name,
                            'content': feed.content,
                            'created_at': feed.created_at,
                            'like': feed.like.count(),
                        })
        context = {
            'feeds_data': feeds_data
        }
        return JsonResponse(context)

## 동기식
# def feed_create(request, country_code):
#     if request.method == "POST":
#         form = FeedForm(request.POST)
#         files = request.FILES.getlist("image")
#         if form.is_valid():
#             country = Country.objects.get(country_code=country_code)
#             f = form.save(commit=False)
#             f.user = request.user
#             f.country = country
#             f.category = "feed"
#             f.user = request.user
#             f.save()
#             for i in files:
#                 FeedImages.objects.create(feed=f, image=i)
#             return redirect('communities:feed', country_code)
#         else:
#             print(form.errors)
#     else:
#         form = FeedForm()
#         imageform = FeedImageForm()
#     return render(request, 'communities/feed_form.html', {"form": form, "imageform": imageform})


def test(request):
    country = Country.objects.values('events')
    print(country)
    context = {
        "country": country,
    }
    return render(request, 'communities/test.html',context=context)


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

def search(request):
    keyword = request.GET.get("keyword", "")  # 검색어
    countries = Country.objects.all()

    if keyword:
        articles = Article.objects.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword)
        ).distinct()
        context = {
            "articles": articles,
            "keyword": keyword,
            "countries": countries,
        }
        return render(request, "communities/search.html", context)