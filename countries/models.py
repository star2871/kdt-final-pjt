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
    status = models.TextField(null=True)
    status_wrt_dt = models.DateField(null=True)
    updated_at = models.DateTimeField(auto_now=True) # 갱신 시간
    visa = models.CharField(max_length=30, null=True) # 비자 정보
    quarantine = models.CharField(max_length=50, null=True) # 방역 정보
    vaccine = models.CharField(max_length=50, null=True) # 백신접종 정보
    isolation = models.CharField(max_length=50, null=True) # 격리여부 정보
    etc = models.CharField(max_length=50, null=True) # 기타 추가 정보
    exchange_rate_code = models.CharField(max_length=255, null=True) # 환율 코드
    exchange_rate = models.CharField(max_length=255, null=True) # 환율
    events = models.JSONField(null=True)
    country_image = ProcessedImageField(
        upload_to="media/",
        blank=True,
        null=True,
        processors=[ResizeToFill(240, 250)],
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