from django.urls import path

from . import views


app_name = "api-v1"

urlpatterns = [
    # path("login/", views.CustomLoginView.as_view(), name="login"),
    # path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpAPIView.as_view(), name="signup"),
    # path(
    #     "profile/<int:pk>/",
    #     views.ProfileUpdateView.as_view(),
    #     name="profile",
    # ),
    # path(
    #     "password_reset/",
    #     views.password_reset_request_view,
    #     name="password_reset",
    # ),
    # accounts/password_change/ [name='password_change']
    # accounts/password_change/done/ [name='password_change_done']
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