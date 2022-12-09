from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
# e_r_c 에 null 값이 있음
# country_name 에 null 값 ? 
class Country(models.Model):
    country_name = models.CharField(max_length=255, null=True)
    country_eng_name = models.CharField(max_length=255, null=True)
    country_code = models.CharField(max_length=255)
    exchange_rate_code = models.CharField(max_length=255, null=True)
    status = models.TextField(null=True)
    status_wrt_dt = models.DateField(null=True)
    ysd_er = models.CharField(max_length=255, null=True)
    cur_nm = models.CharField(max_length=255, null=True)
    events = models.JSONField(null=True)
    visa = models.JSONField(null=True)
    country_image = ProcessedImageField(
        upload_to="media/",
        blank=True,
        null=True,
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 100},
    )
    flag_image = ProcessedImageField(
        upload_to="media/",
        blank=True,
        null=True,
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 80},
    )

class Country_news(models.Model):
    country_code = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True)
    url = models.URLField(max_length=200)

class Festival(models.Model):
    festival_name = models.CharField(max_length=255, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)
    period = models.TextField(max_length=255, null=True)
    festival_image = ProcessedImageField(
        upload_to="media/",
        blank=True,
        null=True,
        processors=[ResizeToFill(240, 300)],
        format="JPEG",
        options={"quality": 100},
    )