from django import forms
from .models import Article, Feed, FeedImages, ArticleComment, FeedComment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from django.utils.translation import gettext_lazy as _

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "grade",
            "image",
        ]
        widgets = {
            'content': SummernoteWidget(),
        }
        labels = {
            # 후기 미리보기 이미지 불러오기 쉽게
            'image' :'대표 이미지를 설정해주세요.'
        }

class AdviceForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "image",
        ]
        widgets = {
            'content': SummernoteWidget(),
        }

        labels = {
            # 후기 미리보기 이미지 불러오기 쉽게
            'image' :'대표 이미지를 설정해주세요.'
        }

class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = [
            "content",
        ]

class FeedImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="사진",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )
    class Meta:
        model = FeedImages
        fields = ["image",]
        labels = {
            "image": _("Image"),
        }

class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ["content",]

class FeedCommentForm(forms.ModelForm):
    class Meta:
        model = FeedComment
        fields = ["content",]