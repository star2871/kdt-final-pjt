from django.shortcuts import render
from .models import Country

def index(request):
    countries = Country.objects.all()
    return render(request, 'country/index.html', {'countries': countries})

def country_detail_view(request, country_code):
    country = Country.objects.get(country_code=country_code)
    return render(request , 'country/detail.html', {'country': country})