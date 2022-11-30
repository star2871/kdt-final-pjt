from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article

# Create your views here.
## 리뷰, 꿀팁, 피드 홈
def review(request, country_code):
    articles = Article.objects.order_by("-pk")
    context = {
        "articles": articles
    }
    return render(request, 'communities/index.html', context)

def review_create(request, country_code):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.travel_start = request.POST["start"]
            article.travel_end = request.POST["end"]
            article.save()
            return redirect('communities:review', country_code)
    else: 
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'communities/form.html', context=context)

def review_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'article': article,
    }
    return render(request, 'communities/detail.html', context)