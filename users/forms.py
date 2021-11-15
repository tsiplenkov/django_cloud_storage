from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile


class UserProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserProfile
        fields = ("email",)


class UserProfileChangeForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ("email",)
