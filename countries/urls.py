from django.urls import path, re_path
from . import views

app_name = 'countries'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<country_code>[A-Z]{2})/$', views.country_detail_view, name='detail'),
]