import pytest
from django.contrib.auth import get_user_model

from ..serializers import (
    SignUpModelSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ResendVerifyEmailSerializer,
    ResetPasswordSerializer,
    PasswordResetDoneSerializer,
)


User = get_user_model()


@pytest.fixture
def simple_user():
    data = {
        "email": "test@test.com",
        "password": "a/1234567",
    }
    user = User.objects.create(**data, is_verify=True)
    return user


@pytest.mark.django_db
class TestAccountsApiSerializers:
    def test_signup_model_serializer_valid_data(self):
        data = {
            "email": "test@test.com",
            "password": "a/1234567",
            "password1": "a/1234567",
        }
        serializer = SignUpModelSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data
        assert serializer.errors == {}

    def test_signup_model_serializer_invalid_email(self):
        data = {
            "email": "test",
            "password": "a/1234567",
            "password1": "a/1234567",
        }
        serializer = SignUpModelSerializer(data=data)
        assert not serializer.is_valid()

    def test_signup_model_serializer_mismatch_password(self):
        data = {
            "email": "test@test.com",
            "password": "123456789a/",
            "password1": "a/1234567",
        }
        serializer = SignUpModelSerializer(data=data)
        assert not serializer.is_valid()

    def test_signup_model_serializer_easy_password(self):
        data = {
            "email": "test@test.com",
            "password": "1234567",
            "password1": "1234567",
        }
        serializer = SignUpModelSerializer(data=data)
        assert not serializer.is_valid()

    def test_change_password_serializer_valid_data(self):
        data = {
            "old_password": "a/1234567",
            "new_password": "a/1234567",
            "new_password1": "a/1234567",
        }
        serializer = ChangePasswordSerializer(data=data)
        assert serializer.is_valid()

    def test_change_password_serializer_mismatch_password(self):
        data = {
            "old_password": "a/1234567",
            "new_password": "a/1234567",
            "new_password1": "a/1234",
        }
        serializer = ChangePasswordSerializer(data=data)
        assert not serializer.is_valid()

    def test_change_password_serializer_miss_field(self):
        data = {
            "old_password": "a/1234567",
            "new_password": "a/1234567",
        }
        serializer = ChangePasswordSerializer(data=data)
        assert not serializer.is_valid()

    def test_profile_serializer_valid_data(self):
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "description": "test description",
        }
        serializer = ProfileSerializer(data=data)
        assert serializer.is_valid()

    def test_resend_verify_email_serializer_user_not_exists(self):
        data = {"email": "test@test.com"}
        serializer = ResendVerifyEmailSerializer(data=data)
        assert not serializer.is_valid()

    def test_resend_verify_email_serializer_user_exists_verified(
        self, simple_user
    ):
        user = simple_user
        data = {"email": user.email}
        serializer = ResendVerifyEmailSerializer(data=data)
        assert not serializer.is_valid()

    def test_resend_verify_email_serializer_user_exists_not_verified(
        self, simple_user
    ):
        user = simple_user
        user.is_verify = False
        user.save()
        data = {"email": user.email}
        serializer = ResendVerifyEmailSerializer(data=data)
        assert serializer.is_valid()

    def test_reset_password_serializer_user_not_exists(self):
        data = {"email": "test@test.com"}
        serializer = ResetPasswordSerializer(data=data)
        assert not serializer.is_valid()

    def test_reset_password_serializer_user_exists(self, simple_user):
        user = simple_user
        data = {"email": user.email}
        serializer = ResetPasswordSerializer(data=data)
        assert serializer.is_valid()

    def test_password_reset_done_serializer_valid_data(self):
        data = {
            "new_password": "a/1234567",
            "new_password1": "a/1234567",
        }
        serializer = PasswordResetDoneSerializer(data=data)
        assert serializer.is_valid()

    def test_password_reset_done_serializer_mismatch_password(self):
        data = {
            "new_password": "a/1234567",
            "new_password1": "a/1234",
        }
        serializer = PasswordResetDoneSerializer(data=data)
        assert not serializer.is_valid()

    def test_password_reset_done_serializer_miss_field(self):
        data = {
            "new_password": "a/1234567",
        }
        serializer = PasswordResetDoneSerializer(data=data)
        assert not serializer.is_valid()
