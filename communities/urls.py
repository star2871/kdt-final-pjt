from django.urls import path
from . import views

app_name = "communities"

urlpatterns = [
    path("<str:country_code>/review/", views.review, name="review"),
    path("<str:country_code>/feed/", views.review, name="feed"),
    path("<str:country_code>/advice/", views.review, name="advice"),
]