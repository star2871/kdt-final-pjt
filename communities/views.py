from django.shortcuts import render

# Create your views here.
## 리뷰, 꿀팁, 피드 홈
def review(request, country_code):
    return render(request, 'communities/index.html')
