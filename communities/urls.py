from django.urls import path
from . import views

app_name = "communities"

urlpatterns = [
    path("<str:country_code>/review/", views.review, name="review"),
    path("<str:country_code>/review/review_create", views.review_create, name="review_create"),
    path("<str:country_code>/review/<int:article_pk>/review_detail", views.detail, name="detail"),
    path("<str:country_code>/review/<int:article_pk>/review_delete", views.delete, name="delete"),
    path("<str:country_code>/review/<int:article_pk>/review_update", views.review_update, name="review_update"),
    path("<str:country_code>/advice/", views.advice, name="advice"),
    path("<str:country_code>/advice/advice_create", views.advice_create, name="advice_create"),
    path("<str:country_code>/feed/", views.review, name="feed"),
    path("<str:country_code>/feed/feed_create", views.feed_create, name="feed_create"),
    path("<str:country_code>/review/<int:article_pk>/review_detail/comment_create/", views.article_comment_create, name="comment_create"),
    path("<str:country_code>/review/<int:article_pk>/review_detail/<int:comment_pk>/comment_update/", views.article_comment_update, name="comment_update"),
    path("<str:country_code>/review/<int:article_pk>/review_detail/<int:comment_pk>/comment_delete/", views.article_comment_delete, name="comment_delete"),
    path("<str:country_code>/review/<int:article_pk>/review_detail/<int:comment_pk>/sub_comment_create/", views.article_sub_comment_create, name="article_sub_comment_create"),
    path("test", views.test, name="test"),
    path("search/", views.search, name="search"),
]
