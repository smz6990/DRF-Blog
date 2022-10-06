from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


app_name = "api-v1"

urlpatterns = [
    path(
        "token/login/",
        views.CustomObtainAuthToken.as_view(),
        name="token-login",
    ),
    path(
        "token/logout/",
        views.CustomLogOutDiscardToken.as_view(),
        name="token-logout",
    ),
    path("signup/", views.SignUpAPIView.as_view(), name="signup"),
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    path(
        "change-password/",
        views.ChangePasswordUpdateAPIView.as_view(),
        name="change-password",
    ),
    path(
        "profile/",
        views.ProfileRetrieveUpdateAPIView.as_view(),
        name="profile",
    ),
    path(
        "verify-email/<str:token>/",
        views.VerifyEmailTokenAPIView.as_view(),
        name="verify-email",
    ),
    path(
        "verify-email-resend/",
        views.ResendVerifyEmailGenericAPIView.as_view(),
        name="verify-resend",
    ),
    path(
        "reset-password/",
        views.ResetPasswordGenericAPIView.as_view(),
        name="reset-password",
    ),
    path(
        "reset/<str:token>/",
        views.PasswordResetDoneGenericAPIView.as_view(),
        name="reset-password-done",
    ),
]
