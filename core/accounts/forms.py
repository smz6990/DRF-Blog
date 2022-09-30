from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from simplemathcaptcha.fields import MathCaptchaField


from .models import Profile


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form for signup
    """

    captcha = MathCaptchaField()

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "captcha"]


class ProfileFrom(forms.ModelForm):
    """
    Custom form for Profile model
    """

    captcha = MathCaptchaField()

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "image",
            "description",
            "captcha",
        ]


class CustomAuthenticationForm(AuthenticationForm):
    """
    Customize the authentication form
    """

    captcha = MathCaptchaField()

    class Meta:
        model = User
        fields = ["user", "password", "captcha"]


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Customize PasswordChangeForm
    """

    captcha = MathCaptchaField()

    class Meta:
        Model = User
        fields = [
            "old_password",
            "new_password1",
            "new_password2",
            "captcha",
        ]
