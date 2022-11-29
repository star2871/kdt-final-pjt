from django.urls import path
from . import views

app_name = 'countries'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:country_code>/', views.country_detail_view, name='detail')
]