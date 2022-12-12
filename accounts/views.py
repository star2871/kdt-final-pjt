from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from communities.models import Article, ArticleComment
# Create your views here.
def index(request):
    return render(request, "accounts/index.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("accounts:index")
    else:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect("countries:index")
        else:
            form = CustomUserCreationForm()
        context = {"form": form}
        return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        # AuthenticationForm은 ModelForm이 아님!
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 세션에 저장
            # login 함수는 request, user 객체를 인자로 받음
            # user 객체는 어디있어요? 바로 form에서 인증된 유저 정보를 받을 수 있음
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "countries:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    articles = Article.objects.filter(user=user,category='review')
    articleComment=ArticleComment.objects.filter(user=user)
    advice = Article.objects.filter(user=user,category='advice')
    likes_article = user.likes_article.all()
    context = {
        "user": user,
        'articles': articles,
        'articleComment': articleComment,
        'advice': advice,
        'likes_article' : likes_article,
    }
    return render(request, "accounts/detail.html", context)


def list(request):
    user = get_user_model().objects.order_by("-pk")
    context = {
        "user": user,
    }
    return render(request, "accounts/list.html", context)


def logout(request):
    auth_logout(request)
    return redirect("countries:index")


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)
