from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from simplemathcaptcha.fields import MathCaptchaField
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


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


class ResendVerifyEmailForm(forms.Form):
    """
    Form to get email to send verification email.
    """

    email = forms.EmailField(max_length=255)


class CustomPasswordResetForm(forms.Form):
    """
    Form for getting user email to send reset password link.
    """

    email = forms.EmailField(max_length=255)


class ReSetPasswordForm(forms.Form):
    """
    Form for set new password for user.
    """

    new_password = forms.CharField(
        max_length=255,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password1 = forms.CharField(max_length=255)

    def is_valid(self):
        password1 = self.data.get("new_password")
        password2 = self.data.get("new_password1")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("password_mismatch")
        password_validation.validate_password(password1)
        return super().is_valid()
