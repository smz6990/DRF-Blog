import pytest
from django.urls import resolve, reverse

from .. import views


@pytest.mark.django_db
class TestAccountsUrls:
    def test_login_url_resolve(self):
        url = reverse("accounts:login")
        assert resolve(url).func.view_class == views.CustomLoginView

    def test_logout_url_resolve(self):
        url = reverse("accounts:logout")
        assert resolve(url).func.view_class == views.CustomLogoutView

    def test_signup_url_resolve(self):
        url = reverse("accounts:signup")
        assert resolve(url).func.view_class == views.CustomSignUpView

    def test_profile_url_resolve(self):
        url = reverse("accounts:profile", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.ProfileUpdateView

    def test_custom_change_password_url_resolve(self):
        url = reverse("accounts:change-password")
        assert resolve(url).func.view_class == views.CustomChangePasswordView

    def test_verify_email_url_resolve(self):
        url = reverse("accounts:verify-email", kwargs={"token": 1})
        assert resolve(url).func.view_class == views.VerifyEmailView

    def test_resend_verify_email_url_resolve(self):
        url = reverse("accounts:resend-verify-email")
        assert resolve(url).func.view_class == views.ResendVerifyEmailView

    def test_password_reset_resolve(self):
        url = reverse("accounts:password_reset")
        assert resolve(url).func.view_class == views.PasswordResetSend

    def test_password_reset_done_resolve(self):
        url = reverse("accounts:password-reset-done", kwargs={"token": 1})
        assert resolve(url).func.view_class == views.PasswordResetDoneView
