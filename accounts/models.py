from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    nick_name = models.CharField(max_length=30, default=False)
    profile_image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        null=True,
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 80},
    )
