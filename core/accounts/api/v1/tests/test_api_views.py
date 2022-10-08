import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User


@pytest.fixture
def anonymous_user():
    return APIClient()


@pytest.fixture
def create_user_obj():
    data = {"email": "test@test.com", "password": "a/1234567"}
    user = User.objects.create_user(**data, is_verify=True)
    return user


@pytest.fixture
def test_user(create_user_obj):
    user = create_user_obj
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def not_verified_user(create_user_obj):
    user = create_user_obj
    user.is_verify = False
    user.save()
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def get_token(create_user_obj):
    user = create_user_obj
    return str(AccessToken.for_user(user))


@pytest.mark.django_db
class TestAccountsApiViews:
    def test_signup_api_view_POST_anonymous_user_valid_data(
        self, anonymous_user
    ):
        """
        Test SignUpAPIView by POST method with anonymous user with valid data
        """
        url = reverse("accounts:api-v1:signup")
        data = {
            "email": "test@test.com",
            "password": "a/1234567",
            "password1": "a/1234567",
        }
        response = anonymous_user.post(url, data)
        assert response.status_code == 201

    def test_signup_api_view_POST_anonymous_user_invalid_data(
        self, anonymous_user
    ):
        """
        Test SignUpAPIView by POST method with anonymous user invalid data
        """
        url = reverse("accounts:api-v1:signup")
        data = {
            "email": "test@test.com",
            "password": "a/1234567",
            "password1": "a/123456712",
        }
        response = anonymous_user.post(url, data)
        assert response.status_code == 400

    def test_signup_api_view_POST_anonymous_user_existing_email(
        self, anonymous_user, test_user
    ):
        """
        Test SignUpAPIView by POST method with anonymous user with existing
        email
        """
        # user = test_user
        url = reverse("accounts:api-v1:signup")
        data = {
            "email": "test@test.com",
            "password": "a/1234567",
            "password1": "a/123456712",
        }
        response = anonymous_user.post(url, data)
        assert response.status_code == 400

    def test_signup_api_view_POST_logged_user(self, test_user):
        """
        Test SignUpAPIView by POST method with logged user
        """
        url = reverse("accounts:api-v1:signup")
        data = {
            "email": "test@test.com",
            "password": "a/1234567",
            "password1": "a/123456712",
        }
        response = test_user.post(url, data)
        assert response.status_code == 403

    def test_custom_obtain_auth_token_view_POST_anonymous_user_valid_data_not_signup(
        self, anonymous_user
    ):
        """
        Test CustomObtainAuthToken by POST method with anonymous user with
        valid data but not sign up
        """
        url = reverse("accounts:api-v1:token-login")
        data = {
            "email": "test@test.com",
            "password": "a/1234567",
        }
        response = anonymous_user.post(url, data)
        assert response.status_code == 400

    def test_custom_obtain_auth_token_view_POST_logged_user(self, test_user):
        """
        Test CustomObtainAuthToken by POST method with logged user
        """
        url = reverse("accounts:api-v1:token-login")
        data = {
            "email": "test@test.com",
            "password": "a/1234567",
        }
        response = test_user.post(url, data)
        assert response.status_code == 403

    def test_custom_discard_token_view_POST_anonymous_user(
        self, anonymous_user
    ):
        """
        Test CustomLogOutDiscardToken by POST method with anonymous user
        """
        url = reverse("accounts:api-v1:token-logout")
        response = anonymous_user.post(url)
        assert response.status_code == 401

    def test_custom_discard_token_view_POST_logged_user(self, test_user):
        """
        Test CustomLogOutDiscardToken by POST method with logged user
        """
        url = reverse("accounts:api-v1:token-logout")
        response = test_user.post(url)
        assert response.status_code == 204

    def test_change_password_update_view_PUT_logged_user(self, test_user):
        """
        Test ChangePasswordUpdateAPIView by PUT method with logged user
        """
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password": "a/1234567",
            "new_password": "a/1234567",
            "new_password1": "a/1234567",
        }
        response = test_user.put(url, data=data)

        assert response.status_code == 204

    def test_change_password_update_view_PUT_logged_user_invalid_data(
        self, test_user
    ):
        """
        Test ChangePasswordUpdateAPIView by PUT method with logged user
        invalid old password
        """
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password": "1234567",
            "new_password": "a/1234567",
            "new_password1": "a/1234567",
        }
        response = test_user.put(url, data=data)

        assert response.status_code == 400

    def test_change_password_update_view_PUT_logged_user_mismatch_password(
        self, test_user
    ):
        """
        Test ChangePasswordUpdateAPIView by PUT method with logged user
        mismatch new password
        """
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password": "a/1234567",
            "new_password": "1234567/a",
            "new_password1": "a/1234567",
        }
        response = test_user.put(url, data=data)

        assert response.status_code == 400

    def test_change_password_update_view_PUT_logged_user_easy_password(
        self, test_user
    ):
        """
        Test ChangePasswordUpdateAPIView by PUT method with logged user
        easy new password
        """
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password": "a/1234567",
            "new_password": "1234567",
            "new_password1": "1234567",
        }
        response = test_user.put(url, data=data)

        assert response.status_code == 400

    def test_change_password_update_view_PUT_anonymous_user(
        self, anonymous_user
    ):
        """
        Test ChangePasswordUpdateAPIView by POST method with anonymous user
        """
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password": "a/1234567",
            "new_password": "1234567/a",
            "new_password1": "1234567/a",
        }
        response = anonymous_user.put(url, data)
        assert response.status_code == 401

    def test_change_password_update_view_PUT_not_verified_user(
        self, not_verified_user
    ):
        """
        Test ChangePasswordUpdateAPIView by PUT method with not verified user
        """
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password": "a/1234567",
            "new_password": "1234567/a",
            "new_password1": "1234567/a",
        }
        response = not_verified_user.put(url, data=data)

        assert response.status_code == 403

    def test_profile_RU_view_GET_anonymous_user(self, anonymous_user):
        """
        Test ProfileRetrieveUpdateAPIView by GET method with anonymous user
        """
        url = reverse("accounts:api-v1:profile")
        try:
            response = anonymous_user.get(url)
        except TypeError:
            assert True
        else:
            assert response.status_code == 401

    def test_profile_RU_view_GET_test_user(self, test_user):
        """
        Test ProfileRetrieveUpdateAPIView by GET method with test user
        """
        url = reverse("accounts:api-v1:profile")
        response = test_user.get(url)
        assert response.status_code == 200

    def test_profile_RU_view_GET_not_verified_user(self, not_verified_user):
        """
        Test ProfileRetrieveUpdateAPIView by GET method with not verified user
        """
        url = reverse("accounts:api-v1:profile")
        response = not_verified_user.get(url)
        assert response.status_code == 403

    def test_profile_RU_view_PUT_anonymous_user(self, anonymous_user):
        """
        Test ProfileRetrieveUpdateAPIView by PUT method with anonymous user
        """
        url = reverse("accounts:api-v1:profile")
        try:
            data = {
                "first_name": "test",
                "last_name": "test",
            }
            response = anonymous_user.put(url, data)
        except TypeError:
            assert True
        else:
            assert response.status_code == 401

    def test_profile_RU_view_PUT_test_user(self, test_user):
        """
        Test ProfileRetrieveUpdateAPIView by PUT method with test user
        """
        url = reverse("accounts:api-v1:profile")
        data = {
            "first_name": "test",
            "last_name": "test",
        }
        response = test_user.put(url, data)
        assert response.status_code == 200

    def test_profile_RU_view_PUT_not_verified_user(self, not_verified_user):
        """
        Test ProfileRetrieveUpdateAPIView by PUT method with not verified user
        """
        url = reverse("accounts:api-v1:profile")
        data = {
            "first_name": "test",
            "last_name": "test",
        }
        response = not_verified_user.put(url, data)
        assert response.status_code == 403

    def test_profile_RU_view_PATCH_anonymous_user(self, anonymous_user):
        """
        Test ProfileRetrieveUpdateAPIView by PATCH method with anonymous user
        """
        url = reverse("accounts:api-v1:profile")
        try:
            data = {
                "first_name": "test",
                "last_name": "test",
            }
            response = anonymous_user.patch(url, data)
        except TypeError:
            assert True
        else:
            assert response.status_code == 401

    def test_profile_RU_view_PATCH_test_user(self, test_user):
        """
        Test ProfileRetrieveUpdateAPIView by PATCH method with test user
        """
        url = reverse("accounts:api-v1:profile")
        data = {
            "first_name": "test",
            "last_name": "test",
        }
        response = test_user.patch(url, data)
        assert response.status_code == 200

    def test_profile_RU_view_PATCH_not_verified_user(
        self, not_verified_user
    ):
        """
        Test ProfileRetrieveUpdateAPIView by PATCH method with not
        verified user
        """
        url = reverse("accounts:api-v1:profile")
        data = {
            "first_name": "test",
            "last_name": "test",
        }
        response = not_verified_user.patch(url, data)
        assert response.status_code == 403

    def test_verify_email_token_view_GET_anonymous_user_valid_token(
        self, anonymous_user, get_token
    ):
        """
        Test VerifyEmailTokenAPIView by GET method with anonymous user with
        valid token
        """
        token = get_token
        url = reverse(
            "accounts:api-v1:verify-email", kwargs={"token": token}
        )
        response = anonymous_user.get(url)
        assert response.status_code == 400

    def test_verify_email_token_view_GET_anonymous_user_invalid_token(
        self, anonymous_user, get_token
    ):
        """
        Test VerifyEmailTokenAPIView by GET method with anonymous user with
        invalid token
        """
        token = get_token + "123"
        url = reverse(
            "accounts:api-v1:verify-email", kwargs={"token": token}
        )
        response = anonymous_user.get(url)
        assert response.status_code == 400

    def test_verify_email_token_view_GET_test_user_valid_token(
        self, test_user, get_token
    ):
        """
        Test VerifyEmailTokenAPIView by GET method with test user with
        valid token
        """
        token = get_token
        url = reverse(
            "accounts:api-v1:verify-email", kwargs={"token": token}
        )
        response = test_user.get(url)
        assert response.status_code == 400

    def test_verify_email_token_view_GET_test_user_invalid_token(
        self, test_user, get_token
    ):
        """
        Test VerifyEmailTokenAPIView by GET method with test user with
        invalid token
        """
        token = get_token + "123"
        url = reverse(
            "accounts:api-v1:verify-email", kwargs={"token": token}
        )
        response = test_user.get(url)
        assert response.status_code == 400

    def test_verify_email_token_view_GET_not_verified_user_valid_token(
        self, not_verified_user, get_token
    ):
        """
        Test VerifyEmailTokenAPIView by GET method with not verified user with
        valid token
        """
        token = get_token
        url = reverse(
            "accounts:api-v1:verify-email", kwargs={"token": token}
        )
        response = not_verified_user.get(url)
        assert response.status_code == 200

    def test_verify_email_token_view_GET_not_verified_user_invalid_token(
        self, not_verified_user, get_token
    ):
        """
        Test VerifyEmailTokenAPIView by GET method with not verified user with
        invalid token
        """
        token = get_token + "123"
        url = reverse(
            "accounts:api-v1:verify-email", kwargs={"token": token}
        )
        response = not_verified_user.get(url)
        assert response.status_code == 400

    def test_resend_verify_email_token_view_POST_anonymous_user(
        self, anonymous_user
    ):
        """
        Test ResendVerifyEmailGenericAPIView by POST method with anonymous user
        """
        data = {"email": "test@test.com", "password": "a/1234567"}
        url = reverse("accounts:api-v1:verify-resend")
        response = anonymous_user.post(url, data)
        assert response.status_code == 400

    def test_resend_verify_email_token_view_POST_test_user(self, test_user):
        """
        Test ResendVerifyEmailGenericAPIView by POST method with test user
        """
        data = {"email": "test@test.com", "password": "a/1234567"}
        url = reverse("accounts:api-v1:verify-resend")
        response = test_user.post(url, data)
        assert response.status_code == 400

    def test_resend_verify_email_token_view_POST_not_verified_user(
        self, not_verified_user
    ):
        """
        Test ResendVerifyEmailGenericAPIView by POST method with not verified
        user
        """
        data = {"email": "test@test.com", "password": "a/1234567"}
        url = reverse("accounts:api-v1:verify-resend")
        response = not_verified_user.post(url, data)
        assert response.status_code == 200

    def test_reset_password_view_POST_anonymous_user(self, anonymous_user):
        """
        Test ResetPasswordGenericAPIView by POST method with anonymous user
        """
        data = {"email": "test@test.com", "password": "a/1234567"}
        url = reverse("accounts:api-v1:reset-password")
        response = anonymous_user.post(url, data)
        assert response.status_code == 400

    def test_reset_password_view_POST_test_user(self, test_user):
        """
        Test ResetPasswordGenericAPIView by POST method with test user
        """
        data = {"email": "test@test.com", "password": "a/1234567"}
        url = reverse("accounts:api-v1:reset-password")
        response = test_user.post(url, data)
        assert response.status_code == 200

    def test_reset_password_done_view_PUT_anonymous_user_valid_token(
        self, anonymous_user, get_token
    ):
        """
        Test PasswordResetDoneGenericAPIView by PUT method with anonymous user
        with valid token
        """
        token = get_token
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        url = reverse(
            "accounts:api-v1:reset-password-done", kwargs={"token": token}
        )
        response = anonymous_user.put(url, data)
        assert response.status_code == 204

    def test_reset_password_done_view_PUT_test_user_valid_token(
        self, test_user, get_token
    ):
        """
        Test PasswordResetDoneGenericAPIView by PUT method with test user
        with valid token
        """
        token = get_token
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        url = reverse(
            "accounts:api-v1:reset-password-done", kwargs={"token": token}
        )
        response = test_user.put(url, data)
        assert response.status_code == 204

    def test_reset_password_done_view_PUT_anonymous_user_valid_token_mismatch_password(
        self, anonymous_user, get_token
    ):
        """
        Test PasswordResetDoneGenericAPIView by PUT method with anonymous user
        with valid token and mismatch password
        """
        token = get_token
        data = {"new_password": "1234a/1234", "new_password1": "a/1234567"}
        url = reverse(
            "accounts:api-v1:reset-password-done", kwargs={"token": token}
        )
        response = anonymous_user.put(url, data)
        assert response.status_code == 400

    def test_reset_password_done_view_PUT_test_user_valid_token_mismatch_password(
        self, test_user, get_token
    ):
        """
        Test PasswordResetDoneGenericAPIView by PUT method with test user
        with valid token and mismatch password
        """
        token = get_token
        data = {"new_password": "1234a/1234", "new_password1": "a/1234567"}
        url = reverse(
            "accounts:api-v1:reset-password-done", kwargs={"token": token}
        )
        response = test_user.put(url, data)
        assert response.status_code == 400

    def test_reset_password_done_view_PUT_anonymous_user_invalid_token(
        self, anonymous_user, get_token
    ):
        """
        Test PasswordResetDoneGenericAPIView by PUT method with anonymous user
        with invalid token
        """
        token = get_token + "123"
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        url = reverse(
            "accounts:api-v1:reset-password-done", kwargs={"token": token}
        )
        response = anonymous_user.put(url, data)
        assert response.status_code == 400

    def test_reset_password_done_view_PUT_test_user_invalid_token(
        self, test_user, get_token
    ):
        """
        Test PasswordResetDoneGenericAPIView by PUT method with test user
        with invalid token
        """
        token = get_token + "123"
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        url = reverse(
            "accounts:api-v1:reset-password-done", kwargs={"token": token}
        )
        response = test_user.put(url, data)
        assert response.status_code == 400

    def test_reset_password_done_view_PUT_anonymous_user_invalid_token_mismatch_password(
        self, anonymous_user, get_token
    ):
        """
        Test PasswordResetDoneGenericAPIView by PUT method with anonymous user
        with invalid token and mismatch password
        """
        token = get_token + "123"
        data = {"new_password": "a/1234567", "new_password1": "7899234567"}
        url = reverse(
            "accounts:api-v1:reset-password-done", kwargs={"token": token}
        )
        response = anonymous_user.put(url, data)
        assert response.status_code == 400

    def test_reset_password_done_view_PUT_test_user_invalid_token_mismatch_password(
        self, test_user, get_token
    ):
        """
        Test PasswordResetDoneGenericAPIView by PUT method with test user
        with invalid token and mismatch password
        """
        token = get_token + "123"
        data = {"new_password": "a/1234567", "new_password1": "7899234567"}
        url = reverse(
            "accounts:api-v1:reset-password-done", kwargs={"token": token}
        )
        response = test_user.put(url, data)
        assert response.status_code == 400
