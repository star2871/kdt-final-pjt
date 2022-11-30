from django.contrib import admin
from .models import Country
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
class CountryAdmin(SummernoteModelAdmin):
    summernote_fields = ('status',)

admin.site.register(Country, CountryAdmin)
