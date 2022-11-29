from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.
class Feeds(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to="images/",
        processors=[Thumbnail(500, 700)],
        format="JPEG",
        options={"quality": 100},
    )
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_feeds"
    )

    # object 를 Post 의 title 문자열로 반환
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


class FeedComments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret = models.BooleanField(default=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_feed_comments"
    )

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
