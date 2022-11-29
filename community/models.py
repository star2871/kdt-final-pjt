from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from datetime import datetime, timedelta
from django.utils import timezone



# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    travel_start = models.DateField()
    travel_end = models.DateField()
    # 신호등
    grade = models.IntegerField(default=1)
    content = models.TextField()
    image = ProcessedImageField(blank=True, 
                                processors=[Thumbnail(500, 700)], 
                                format='JPEG', options={'quality':90}, 
                                upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes_article')
    
    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return "방금 전"
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + "분 전"
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + "시간 전"
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + "일 전"
        else:
            return False

class Article_comment(models.Model):
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    secret = models.BooleanField(default=False)
    profile = ProcessedImageField(blank=True, 
                                processors=[Thumbnail(500, 700)], 
                                format='JPEG', options={'quality':90}, 
                                upload_to='images/')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)