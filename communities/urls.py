from django.urls import path
from . import views

app_name = "communities"

urlpatterns = [
    path("", views.review, name="review"),
    # path("feed/", views.feed, name="feed"),
    # path("advice/", views.advice, name="advice"),
]
