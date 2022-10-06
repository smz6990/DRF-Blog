import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from django.core.exceptions import ValidationError


User = get_user_model()


@pytest.fixture
def create_basic_user():
    data = {"email": "test@test.com", "password": "a/1234567"}
    return User.objects.create(**data, is_verify=True)


@pytest.fixture
def logged_user(create_basic_user):
    user = create_basic_user
    client = Client()
    client.force_login(user=user)
    return client


@pytest.fixture
def not_verified_user(create_basic_user):
    user = create_basic_user
    user.is_verify = False
    user.save()
    client = Client()
    client.force_login(user=user)
    return client


@pytest.fixture
def anonymous_user():
    return Client()


@pytest.mark.django_db
class TestAccountsViews:
    def test_login_view_GET_anonymous_user(self, anonymous_user):
        """
        Test for CustomLoginView by GET method with anonymous user
        """
        url = reverse("accounts:login")
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_login_view_POST_anonymous_user(self, anonymous_user):
        """
        Test for CustomLoginView by POST method with anonymous user
        """
        url = reverse("accounts:login")
        data = {
            "username": "test@test.com",
            "password": "a/12345670",
            "captcha": 1,
        }
        response = anonymous_user.post(url, data)
        assert response.status_code == 200

    def test_login_view_GET_logged_user(self, logged_user):
        """
        Test for CustomLoginView by GET method with authorized user
        """
        url = reverse("accounts:login")
        response = logged_user.get(url)
        assert response.status_code == 403

    def test_login_view_POST_logged_user(self, logged_user):
        """
        Test for CustomLoginView by POST method with authorized user
        """
        url = reverse("accounts:login")
        data = {
            "username": "test@test.com",
            "password": "a/12345670",
            "captcha": 1,
        }
        response = logged_user.post(url, data)
        assert response.status_code == 403

    def test_logout_view_GET_anonymous_user(self, anonymous_user):
        """
        Test for CustomLogoutView by GET method with anonymous user
        """
        url = reverse("accounts:logout")
        response = anonymous_user.get(url)
        # redirect not authenticated user to login page
        assert response.status_code == 302

    def test_logout_view_POST_anonymous_user(self, anonymous_user):
        """
        Test for CustomLogoutView by POST method with anonymous user
        """
        url = reverse("accounts:logout")
        response = anonymous_user.post(url)
        # redirect not authenticated user to login page
        assert response.status_code == 302

    def test_logout_view_GET_logged_user(self, logged_user):
        """
        Test for CustomLogoutView by GET method with authorized user
        """
        url = reverse("accounts:logout")
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_logout_view_POST_logged_user(self, logged_user):
        """
        Test for CustomLogoutView by POST method with authorized user
        """
        url = reverse("accounts:logout")
        response = logged_user.post(url)
        assert response.status_code == 200

    def test_sign_up_view_GET_anonymous_user(self, anonymous_user):
        """
        Test for CustomSignUpView by GET method with anonymous user
        """
        url = reverse("accounts:signup")
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_sign_up_view_POST_anonymous_user(self, anonymous_user):
        """
        Test for CustomSignUpView by POST method with anonymous user
        """
        url = reverse("accounts:signup")
        data = {
            "email": "test@test.com",
            "password1": "a/1234567",
            "password2": "a/1234567",
            "captcha": 1,
        }
        response = anonymous_user.post(url, data)
        # because of captcha field it gets 200 instead of 201
        assert response.status_code == 200

    def test_sign_up_view_GET_logged_user(self, logged_user):
        """
        Test for CustomSignUpView by GET method with authenticated user
        """
        url = reverse("accounts:signup")
        response = logged_user.get(url)
        assert response.status_code == 403

    def test_sign_up_view_POST_logged_user(self, logged_user):
        """
        Test for CustomSignUpView by POST method with authenticated user
        """
        url = reverse("accounts:signup")
        response = logged_user.post(url)
        assert response.status_code == 403

    def test_profile_update_view_GET_anonymous_user(self, anonymous_user):
        """
        Test for ProfileUpdateView by GET method with anonymous user
        """
        url = reverse("accounts:profile", kwargs={"pk": 1})
        response = anonymous_user.get(url)
        # redirect user to login page
        assert response.status_code == 302

    def test_profile_update_view_POST_anonymous_user(self, anonymous_user):
        """
        Test for ProfileUpdateView by POST method with anonymous user
        """
        url = reverse("accounts:profile", kwargs={"pk": 1})
        response = anonymous_user.post(url)
        # redirect user to login page
        assert response.status_code == 302

    def test_profile_update_view_GET_logged_user(self, logged_user):
        """
        Test for ProfileUpdateView by GET method with authenticated user
        """
        user = User.objects.get(email="test@test.com")
        url = reverse("accounts:profile", kwargs={"pk": user.id})
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_profile_update_view_POST_logged_user(self, logged_user):
        """
        Test for ProfileUpdateView by POST method with authenticated user
        """
        user = User.objects.get(email="test@test.com")
        url = reverse("accounts:profile", kwargs={"pk": user.id})
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "description": "test description",
            "captcha": 1,
        }
        response = logged_user.post(url, data)
        assert response.status_code == 200

    def test_profile_update_view_GET_logged_user_not_owner(
        self, logged_user
    ):
        """
        Test for ProfileUpdateView by GET method with
        authenticated user but someone else profile
        """
        user = User.objects.create_user(
            email="test2@test2.com", password="a/1234567"
        )
        url = reverse("accounts:profile", kwargs={"pk": user.id})
        response = logged_user.get(url)
        # redirect to website index
        assert response.status_code == 302

    def test_profile_update_view_POST_logged_user_not_owner(
        self, logged_user
    ):
        """
        Test for ProfileUpdateView by POST method with
        authenticated user but someone else profile
        """
        user = User.objects.create_user(
            email="test2@test2.com", password="a/1234567"
        )
        url = reverse("accounts:profile", kwargs={"pk": user.id})
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "description": "test description",
            "captcha": 1,
        }
        response = logged_user.post(url, data)
        # redirect to website index
        assert response.status_code == 302

    def test_change_password_view_GET_anonymous_user(self, anonymous_user):
        """
        Test for CustomChangePasswordView by GET method with anonymous user
        """
        url = reverse("accounts:change-password")
        response = anonymous_user.get(url)
        assert response.status_code == 302

    def test_change_password_view_POST_anonymous_user(
        self, anonymous_user
    ):
        """
        Test for CustomChangePasswordView by POST method with anonymous user
        """
        url = reverse("accounts:change-password")
        data = {
            "old_password": "a/1234567",
            "new_password1": "a/1234567",
            "new_password2": "a/1234567",
            "captcha": 1,
        }
        response = anonymous_user.post(url, data)
        assert response.status_code == 302

    def test_change_password_view_GET_not_verified_user(
        self, not_verified_user
    ):
        """
        Test for CustomChangePasswordView by GET method with not verified user
        """
        url = reverse("accounts:change-password")
        response = not_verified_user.get(url)
        assert response.status_code == 403

    def test_change_password_view_POST_not_verified_user(
        self, not_verified_user
    ):
        """
        Test for CustomChangePasswordView by POST method with not verified user
        """
        url = reverse("accounts:change-password")
        data = {
            "old_password": "a/1234567",
            "new_password1": "a/1234567",
            "new_password2": "a/1234567",
            "captcha": 1,
        }
        response = not_verified_user.post(url, data)
        assert response.status_code == 403

    def test_change_password_view_GET_logged_user(self, logged_user):
        """
        Test for CustomChangePasswordView by GET method with authorized user
        """
        url = reverse("accounts:change-password")
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_change_password_view_POST_logged_user(self, logged_user):
        """
        Test for CustomChangePasswordView by POST method with authorized user
        """
        url = reverse("accounts:change-password")
        data = {
            "old_password": "a/1234567",
            "new_password1": "a/1234567",
            "new_password2": "a/1234567",
            "captcha": 1,
        }
        response = logged_user.post(url, data)
        assert response.status_code == 200

    def test_verify_email_view_GET_anonymous_user_valid_toke(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for VerifyEmailView by GET method with anonymous user
        with valid token
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse("accounts:verify-email", kwargs={"token": token})
        response = anonymous_user.get(url)
        assert response.status_code == 302

    def test_verify_email_view_GET_anonymous_user_invalid_token(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for VerifyEmailView by GET method with anonymous user
        with invalid token
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse("accounts:verify-email", kwargs={"token": token})
        response = anonymous_user.get(url)
        assert response.status_code == 302

    def test_verify_email_view_GET_logged_user_valid_token(
        self, logged_user, create_basic_user
    ):
        """
        Test for VerifyEmailView by GET method with authorized user
        with valid token
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse("accounts:verify-email", kwargs={"token": token})
        response = logged_user.get(url)
        assert response.status_code == 302

    def test_verify_email_view_GET_logged_user_invalid_token(
        self, logged_user, create_basic_user
    ):
        """
        Test for VerifyEmailView by GET method with authorized user
        with invalid token
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse("accounts:verify-email", kwargs={"token": token})
        response = logged_user.get(url)
        assert response.status_code == 302

    def test_verify_email_view_GET_not_verified_user_valid_token(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for VerifyEmailView by GET method with not verified user with
        valid token
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse("accounts:verify-email", kwargs={"token": token})
        response = not_verified_user.get(url)
        assert response.status_code == 302

    def test_verify_email_view_GET_not_verified_user_invalid_token(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for VerifyEmailView by GET method with not verified user with
        invalid token
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse("accounts:verify-email", kwargs={"token": token})
        response = not_verified_user.get(url)
        assert response.status_code == 302

    def test_resend_verify_email_view_GET_anonymous_user(
        self, anonymous_user
    ):
        """
        Test for ResendVerifyEmailView by GET method with anonymous user
        """
        url = reverse("accounts:resend-verify-email")
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_resend_verify_email_view_POST_anonymous_user(
        self, anonymous_user
    ):
        """
        Test for ResendVerifyEmailView by POST method with anonymous user
        """
        url = reverse("accounts:resend-verify-email")
        response = anonymous_user.post(url, {"email": "test@test.com"})
        assert response.status_code == 302

    def test_resend_verify_email_view_GET_not_verified_user(
        self, not_verified_user
    ):
        """
        Test for ResendVerifyEmailView by GET method with not verified user
        """
        url = reverse("accounts:resend-verify-email")
        response = not_verified_user.get(url)
        assert response.status_code == 200

    def test_resend_verify_email_view_POST_not_verified_user(
        self, not_verified_user
    ):
        """
        Test for ResendVerifyEmailView by POST method with not verified user
        """
        url = reverse("accounts:resend-verify-email")
        response = not_verified_user.post(url, {"email": "test@test.com"})
        assert response.status_code == 302

    def test_resend_verify_email_view_GET_logged_user(self, logged_user):
        """
        Test for ResendVerifyEmailView by GET method with authenticated user
        """
        url = reverse("accounts:resend-verify-email")
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_resend_verify_email_view_POST_logged_user(self, logged_user):
        """
        Test for ResendVerifyEmailView by POST method with authenticated user
        """
        url = reverse("accounts:resend-verify-email")
        response = logged_user.post(url, {"email": "test@test.com"})
        assert response.status_code == 302

    def test_password_reset_send_view_GET_anonymous_user(
        self, anonymous_user
    ):
        """
        Test for PasswordResetSend by GET method with anonymous user
        """
        url = reverse("accounts:password_reset")
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_password_reset_send_view_POST_anonymous_user(
        self, anonymous_user
    ):
        """
        Test for PasswordResetSend by POST method with anonymous user
        """
        url = reverse("accounts:password_reset")
        response = anonymous_user.post(url, {"email": "test@test.com"})
        assert response.status_code == 302

    def test_password_reset_send_view_GET_not_verified_user(
        self, not_verified_user
    ):
        """
        Test for PasswordResetSend by GET method with not verified user
        """
        url = reverse("accounts:password_reset")
        response = not_verified_user.get(url)
        assert response.status_code == 200

    def test_password_reset_send_view_POST_not_verified_user(
        self, not_verified_user
    ):
        """
        Test for PasswordResetSend by POST method with not verified user
        """
        url = reverse("accounts:password_reset")
        response = not_verified_user.post(url, {"email": "test@test.com"})
        assert response.status_code == 302

    def test_password_reset_send_view_GET_logged_user(self, logged_user):
        """
        Test for PasswordResetSend by GET method with authenticated user
        """
        url = reverse("accounts:password_reset")
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_password_reset_send_view_POST_logged_user(self, logged_user):
        """
        Test for PasswordResetSend by POST method with authenticated user
        """
        url = reverse("accounts:password_reset")
        response = logged_user.post(url, {"email": "test@test.com"})
        assert response.status_code == 302

    def test_password_reset_done_view_GET_anonymous_user_valid_token(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by GET method with anonymous user
        with valid token
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_password_reset_done_view_GET_anonymous_user_invalid_token(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by GET method with anonymous user
        with invalid token
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_password_reset_done_view_POST_anonymous_user_valid_token_valid_password(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with anonymous user
        with valid token with correct password
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        response = anonymous_user.post(url, data)
        assert response.status_code == 302

    def test_password_reset_done_view_POST_anonymous_user_invalid_token_valid_password(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with anonymous user
        with invalid token with correct password
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        response = anonymous_user.post(url, data)
        assert response.status_code == 302

    def test_password_reset_done_view_POST_anonymous_user_valid_token_mismatch_password(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with anonymous user
        with valid token with mismatch password
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "a/1234567", "new_password1": "1234567@/"}
        try:
            response = anonymous_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_POST_anonymous_user_invalid_token_mismatch_password(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with anonymous user
        with invalid token with mismatch password
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "a/1234567", "new_password1": "1234567@/"}
        try:
            response = anonymous_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_POST_anonymous_user_valid_token_easy_password(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with anonymous user
        with valid token with easy password
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "1234567", "new_password1": "1234567"}
        try:
            response = anonymous_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_POST_anonymous_user_invalid_token_easy_password(
        self, anonymous_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with anonymous user
        with invalid token with easy password
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "1234567", "new_password1": "1234567"}
        try:
            response = anonymous_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_GET_logged_user_valid_token(
        self, logged_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by GET method with authorized user
        with valid token
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_password_reset_done_view_POST_logged_user_valid_token_correct_password(
        self, logged_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with authorized user
        with valid token with correct password
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        response = logged_user.post(url, data)
        assert response.status_code == 302

    def test_password_reset_done_view_POST_logged_user_valid_token_mismatch_password(
        self, logged_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with authorized user
        with valid token with mismatch password
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "1234567/a", "new_password1": "a/1234567"}
        try:
            response = logged_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_POST_logged_user_valid_token_easy_password(
        self, logged_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with authorized user
        with valid token with easy password
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "1234567", "new_password1": "1234567"}
        try:
            response = logged_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_GET_logged_user_invalid_token(
        self, logged_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by GET method with authorized user
        with invalid token
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_password_reset_done_view_POST_logged_user_invalid_token_correct_password(
        self, logged_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with authorized user
        with invalid token with correct password
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        response = logged_user.post(url, data)
        assert response.status_code == 302

    def test_password_reset_done_view_POST_logged_user_invalid_token_mismatch_password(
        self, logged_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with authorized user
        with invalid token with mismatch password
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "1234567/a", "new_password1": "a/1234567"}
        try:
            response = logged_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_POST_logged_user_invalid_token_easy_password(
        self, logged_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with authorized user
        with invalid token with easy password
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "1234567", "new_password1": "1234567"}
        try:
            response = logged_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_GET_not_verified_user_valid_token(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by GET method with not verified user
        with valid token
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        response = not_verified_user.get(url)
        assert response.status_code == 200

    def test_password_reset_done_view_GET_not_verified_user_invalid_token(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by GET method with not verified user
        with invalid token
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        response = not_verified_user.get(url)
        assert response.status_code == 200

    def test_password_reset_done_view_POST_not_verified_user_valid_token_valid_password(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with not verified user
        with valid token and valid password
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        response = not_verified_user.post(url, data)
        assert response.status_code == 302

    def test_password_reset_done_view_POST_not_verified_user_invalid_token_valid_password(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with not verified user
        with invalid token and valid password
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        response = not_verified_user.post(url, data)
        assert response.status_code == 302

    def test_password_reset_done_view_POST_not_verified_user_valid_token_mismatch_password(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with not verified user
        with valid token and mismatch password
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {
            "new_password": "a/1234567",
            "new_password1": "a/123456789",
        }
        try:
            response = not_verified_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_POST_not_verified_user_invalid_token_mismatch_password(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with not verified user
        with invalid token and mismatch password
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {
            "new_password": "a/1234567",
            "new_password1": "a/123456780",
        }
        try:
            response = not_verified_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_POST_not_verified_user_valid_token_easy_password(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with not verified user
        with valid token and easy password
        """
        token = str(AccessToken.for_user(create_basic_user))
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "1234567", "new_password1": "1234567"}
        try:
            response = not_verified_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302

    def test_password_reset_done_view_POST_not_verified_user_invalid_token_easy_password(
        self, not_verified_user, create_basic_user
    ):
        """
        Test for PasswordResetDoneView by POST method with not verified user
        with invalid token and easy password
        """
        token = str(AccessToken.for_user(create_basic_user)) + "123"
        url = reverse(
            "accounts:password-reset-done", kwargs={"token": token}
        )
        data = {"new_password": "1234567", "new_password1": "1234567"}
        try:
            response = not_verified_user.post(url, data)
        except ValidationError:
            assert True
        else:
            assert response.status_code == 302
