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