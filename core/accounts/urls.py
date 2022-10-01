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
    # email verification url and view
    # email resend verification url and view
    path(
        "password_reset",
        views.password_reset_request_view,
        name="password_reset",
    )
    # path('password_reset/done/',
    #     auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
    #     name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html",
    #     post_reset_login=False,success_url='/registration/reset/done/'),
    # name='password_reset_confirm'),
    # path('reset/done/',
    #     auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    #     name='password_reset_complete'),
]
