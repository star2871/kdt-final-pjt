from django.urls import path
from . import views

app_name = "communities"

urlpatterns = [
    path("<str:country_code>/review/", views.review, name="review"),
    path("<str:country_code>/review/review_create", views.review_create, name="review_create"),
    path("<str:country_code>/review/<int:article_pk>/review_detail", views.review_detail, name="review_detail"),
    path("<str:country_code>/review/<int:article_pk>/review_delete", views.review_delete, name="review_delete"),
    path("<str:country_code>/review/<int:article_pk>/review_update", views.review_update, name="review_update"),
    path("<str:country_code>/feed/", views.review, name="feed"),
    path("<str:country_code>/advice/", views.review, name="advice"),   
]
