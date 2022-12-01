from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from datetime import datetime, timedelta
from django.utils import timezone
from countries.models import Country
from django.template.defaultfilters import slugify


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    category = models.CharField(max_length=80, blank=True)
    travel_start = models.DateField(blank=True, null=True)
    travel_end = models.DateField(blank=True, null=True)
    # 신호등
    grade = models.IntegerField(default=1, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)
    image = ProcessedImageField(blank=True, 
                                processors=[Thumbnail(500, 700)], 
                                format='JPEG', options={'quality':90}, 
                                upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes_article')
    
    def __str__(self):
        return self.title

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


# Create your models here.
class Feed(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_feeds"
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

def get_image_filename(instance, filename):
    # 해당 Post 모델의 id 을 가져옴
    id = instance.feed.id
    # slug - 의미있는 url 사용을 위한 필드.
    # slugfy 를 사용해서 id slug 시켜줌.
    slug = slugify(id)
    # 제목 - 슬러그된 파일이름 형태
    return "post_images/%s-%s" % (slug, filename)

# default, upload_to 먼지 보기
class FeedImages(models.Model):
    # default = None 으로 이미지를 등록하지 않을 때는 db에 저장되지 않음.
    feed = models.ForeignKey(
        Feed, default=None, on_delete=models.CASCADE, related_name="feeds_image"
    )
    # get_image_filename method 경로 사용
    # 문자열로 경로를 지정할 경우, media/문자열 지정 경로로 저장되며, 중간 디렉토리 경로를 지정할 수 있고,
    # 메소드(함수)로 지정할 경우, 중간 디렉토리 경로명뿐만 아니라 파일명까지 지정 가능
    image = models.ImageField(upload_to=get_image_filename)
    # admin 에서 모델이름
    class Meta:
        # 단수
        verbose_name = "Image"
        # 복수
        verbose_name_plural = "Images"

    # 이것도 역시 post title 로 반환
    def __str__(self):
        return str(self.feed)


class ArticleComment(models.Model):
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

class FeedComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret = models.BooleanField(default=False)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
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
