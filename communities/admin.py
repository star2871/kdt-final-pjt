from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Article, ArticleComment, Notice

# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Article, PostAdmin,)
admin.site.register(ArticleComment)
admin.site.register(Notice)