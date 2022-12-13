from django.contrib import admin
from .models import Country, Festival, Country_news
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
class CountryAdmin(SummernoteModelAdmin):
    summernote_fields = ('',)

admin.site.register(Country, CountryAdmin)
admin.site.register(Festival,)
admin.site.register(Country_news,)
