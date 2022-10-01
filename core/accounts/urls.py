from django.urls import path, include

from . import views


app_name = "accounts"

urlpatterns = [
    path("api/v1/", include("accounts.api.v1.urls")),
    path("api/v2/", include("djoser.urls")),
    path("api/v2/", include("djoser.urls.jwt")),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("signup/", views.CustomSignUpView.as_view(), name="signup"),
    path(
        "profile/<int:pk>/",
        views.ProfileUpdateView.as_view(),
        name="profile",
    ),
    path(
        "change-password/",
        views.CustomChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "verify-email/<str:token>/",
        views.VerifyEmailView.as_view(),
        name="verify-email",
    ),
    path(
        "resend-verify-email/",
        views.ResendVerifyEmailView.as_view(),
        name="resend-verify-email",
    ),
    path(
        "password_reset/",
        views.PasswordResetSend.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset-done/<str:token>/",
        views.PasswordResetDoneView.as_view(),
        name="password-reset-done",
    ),
]
