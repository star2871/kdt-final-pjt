from django.contrib import admin
from .models import Country, Festival
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
class CountryAdmin(SummernoteModelAdmin):
    summernote_fields = ('',)

admin.site.register(Country, CountryAdmin)
admin.site.register(Festival,)
