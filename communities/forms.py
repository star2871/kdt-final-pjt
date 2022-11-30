from django import forms
from .models import Article, Feed, ArticleComment, FeedComment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "grade",
            "country",
            "image",
        ]
        widgets = {
            'content': SummernoteWidget(),
        }
        labels = {
            # 후기 미리보기 이미지 불러오기 쉽게
            'image' :'대표 이미지를 설정해주세요.'
        }