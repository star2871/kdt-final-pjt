from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "nick_name",
            "profile_image",
        )

        labels = {
            "username": "아이디",
            "nick_name": "닉네임",
            "profile_image": "프로필이미지",
        }
