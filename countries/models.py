from django.db import models

# Create your models here.
# e_r_c 에 null 값이 있음
# country_name 에 null 값 ? 
class Country(models.Model):
    country_name = models.CharField(max_length=255, null=True)
    country_code = models.CharField(max_length=255)
    exchange_rate_code = models.CharField(max_length=255, null=True)
    status = models.TextField(null=True)
    status_wrt_dt = models.DateField(null=True)
    ysd_er = models.CharField(max_length=255, null=True)
    cur_nm = models.CharField(max_length=255, null=True)
    events = models.JSONField(null=True)
    visa = models.JSONField(null=True)
    