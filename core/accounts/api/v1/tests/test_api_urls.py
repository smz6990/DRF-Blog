import pytest
from django.urls import resolve, reverse

from .. import views
from ..urls import TokenRefreshView, TokenVerifyView


@pytest.mark.django_db
class TestAccountsApiUrls:
    def test_token_login_api_url(self):
        url = reverse("accounts:api-v1:token-login")
        assert resolve(url).func.view_class == views.CustomObtainAuthToken

    def test_token_logout_api_url(self):
        url = reverse("accounts:api-v1:token-logout")
        assert resolve(url).func.view_class == views.CustomLogOutDiscardToken

    def test_signup_api_url(self):
        url = reverse("accounts:api-v1:signup")
        assert resolve(url).func.view_class == views.SignUpAPIView

    def test_jwt_create_api_url(self):
        url = reverse("accounts:api-v1:jwt-create")
        assert (
            resolve(url).func.view_class == views.CustomTokenObtainPairView
        )

    def test_jwt_refresh_api_url(self):
        url = reverse("accounts:api-v1:jwt-refresh")
        assert resolve(url).func.view_class == TokenRefreshView

    def test_jwt_verify_api_url(self):
        url = reverse("accounts:api-v1:jwt-verify")
        assert resolve(url).func.view_class == TokenVerifyView

    def test_change_password_update_api_url(self):
        url = reverse("accounts:api-v1:change-password")
        assert (
            resolve(url).func.view_class == views.ChangePasswordUpdateAPIView
        )

    def test_profile_api_url(self):
        url = reverse("accounts:api-v1:profile")
        assert (
            resolve(url).func.view_class
            == views.ProfileRetrieveUpdateAPIView
        )

    def test_verify_email_api_url(self):
        url = reverse(
            "accounts:api-v1:verify-email", kwargs={"token": "123"}
        )
        assert resolve(url).func.view_class == views.VerifyEmailTokenAPIView

    def test_verify_email_resend_api_url(self):
        url = reverse("accounts:api-v1:verify-resend")
        assert (
            resolve(url).func.view_class
            == views.ResendVerifyEmailGenericAPIView
        )

    def test_reset_password_api_url(self):
        url = reverse("accounts:api-v1:reset-password")
        assert (
            resolve(url).func.view_class == views.ResetPasswordGenericAPIView
        )

    def test_reset_password_done_api_url(self):
        url = reverse(
            "accounts:api-v1:reset-password-done", kwargs={"token": "123"}
        )
        assert (
            resolve(url).func.view_class
            == views.PasswordResetDoneGenericAPIView
        )
