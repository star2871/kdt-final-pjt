from django.urls import path
from . import views

app_name = "communities"

urlpatterns = [
    path("<str:country_code>/review/", views.review, name="review"),
    path("<str:country_code>/review/review_create", views.review_create, name="review_create"),
    path("<str:country_code>/review/<int:article_pk>/review_detail", views.review_detail, name="review_detail"),
    path("<str:country_code>/feed/", views.review, name="feed"),
    path("<str:country_code>/advice/", views.review, name="advice"),
    path("<str:country_code>/review/review_create", views.review_create, name="review_create"),
    path("review/<int:article_pk>/review_detail", views.review_detail, name="review_detail"),
    path("test", views.test, name="test"),
]
