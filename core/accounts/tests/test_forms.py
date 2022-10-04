import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from ..forms import (
    CustomUserCreationForm,
    ProfileFrom,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    ResendVerifyEmailForm,
    CustomPasswordResetForm,
    ReSetPasswordForm,
)


User = get_user_model()


@pytest.fixture
def create_user():
    data = {
        "email": "test@test.com",
        "password": "a/1234567",
    }
    user = User.objects.create(**data, is_verify=True)
    return user


@pytest.mark.django_db
class TestAccountsForm:
    def test_user_creation_form_valid_data(self):
        """
        Test for CustomUserCreationForm with valid data
        """
        data = {
            "email": "test@test.com",
            "password1": "a/1234567",
            "password2": "a/1234567",
            "captcha": 1,
        }
        form = CustomUserCreationForm(data=data)
        # it has error because of captcha field
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert form.has_error("captcha")

    def test_user_creation_form_mismatch_password(self):
        """
        Test for CustomUserCreationForm with mismatch password
        """
        data = {
            "email": "test@test.com",
            "password1": "a/1234567",
            "password2": "a/123456787",
            "captcha": 1,
        }
        form = CustomUserCreationForm(data=data)
        # it has error because of captcha and password2 fields.
        assert not form.is_valid()
        assert len(form.errors) == 2
        assert form.has_error("password2")
        assert form.has_error("captcha")

    def test_user_creation_form_invalid_data(self):
        """
        Test for CustomUserCreationForm with invalid email field
        """
        data = {
            "email": "invalid email",
            "password1": "a/1234567",
            "password2": "a/1234567",
            "captcha": 1,
        }
        form = CustomUserCreationForm(data=data)
        # it has error because of captcha and email fields.
        assert not form.is_valid()
        assert len(form.errors) == 2
        assert form.has_error("email")
        assert form.has_error("captcha")

    def test_user_creation_form_no_data(self):
        """
        Test for CustomUserCreationForm with no data
        """
        form = CustomUserCreationForm({})
        assert not form.is_valid()

    def test_profile_form_valid_data(self):
        """
        Test for ProfileFrom with valid data
        """
        data = {
            "first_name": "test first name",
            "last_name": "test last name",
            "description": "test description",
            "captcha": 1,
        }
        form = ProfileFrom(data=data)
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert form.has_error("captcha")

    def test_profile_form_no_data(self):
        """
        Test for ProfileFrom with no data
        """
        form = ProfileFrom({})
        assert not form.is_valid()

    def test_authentication_form_valid_data(self, create_user):
        """
        Test for CustomAuthenticationForm with valid data
        """
        user = create_user
        data = {
            "username": user.email,
            "password": "a/1234567",
            "captcha": 1,
        }
        form = CustomAuthenticationForm(data=data)
        # form valid is false because of captcha field
        assert not form.is_valid()
        assert len(form.errors) == 2
        assert form.has_error("captcha")

    def test_authentication_form_invalid_data(self):
        """
        Test for CustomAuthenticationForm with invalid data
        """
        data = {
            "username": "test",
            "password": "a/1234567",
            "captcha": 1,
        }
        form = CustomAuthenticationForm(data=data)
        # form valid is false because of captcha field and
        # username(email) fields
        assert not form.is_valid()
        assert len(form.errors) == 2
        assert form.has_error("captcha")

    def test_password_change_form_valid_data(self, create_user):
        """
        Test for CustomPasswordChangeForm with valid data
        """
        user = create_user
        data = {
            "old_password": user.password,
            "new_password1": "a/123456789",
            "new_password2": "a/123456789",
            "captcha": 1,
        }
        form = CustomPasswordChangeForm(user, data)
        # form valid is false because of captcha field and
        # username(email) fields
        assert not form.is_valid()
        assert form.has_error("captcha")

    def test_password_change_form_mismatch_password(self, create_user):
        """
        Test for CustomPasswordChangeForm with mismatch password
        """
        user = create_user
        data = {
            "old_password": user.password,
            "new_password1": "987654321/a",
            "new_password2": "a/123456789",
            "captcha": 1,
        }
        form = CustomPasswordChangeForm(user, data)
        assert not form.is_valid()
        assert form.has_error("captcha")
        assert form.has_error("new_password2")

    def test_password_change_form_wrong_old_password(self, create_user):
        """
        Test for CustomPasswordChangeForm with wrong old password
        """
        user = create_user
        data = {
            "old_password": "password",
            "new_password1": "a/123456789",
            "new_password2": "a/123456789",
            "captcha": 1,
        }
        form = CustomPasswordChangeForm(user, data)
        assert not form.is_valid()
        assert form.has_error("captcha")
        assert form.has_error("old_password")

    def test_password_change_form_simple_new_password(self, create_user):
        """
        Test for CustomPasswordChangeForm with not complex new password
        """
        user = create_user
        data = {
            "old_password": user.password,
            "new_password1": "123456",
            "new_password2": "123456",
            "captcha": 1,
        }
        form = CustomPasswordChangeForm(user, data)
        assert not form.is_valid()
        assert form.has_error("captcha")
        assert form.has_error("new_password2")

    def test_resend_verify_email_form_valid_data(self):
        """
        Test for ResendVerifyEmailForm with valid data
        """
        data = {"email": "test@test.com"}
        form = ResendVerifyEmailForm(data=data)
        assert form.is_valid()
        assert len(form.errors) == 0

    def test_resend_verify_email_form_invalid_data(self):
        """
        Test for ResendVerifyEmailForm with invalid data
        """
        data = {"email": "test"}
        form = ResendVerifyEmailForm(data=data)
        assert not form.is_valid()
        assert len(form.errors) == 1

    def test_resend_verify_email_form_no_data(self):
        """
        Test for ResendVerifyEmailForm with no data
        """
        data = {}
        form = ResendVerifyEmailForm(data=data)
        assert not form.is_valid()
        assert len(form.errors) == 1

    def test_password_reset_form_valid_data(self):
        """
        Test for CustomPasswordResetForm with valid data
        """
        data = {"email": "test@test.com"}
        form = CustomPasswordResetForm(data=data)
        assert form.is_valid()
        assert len(form.errors) == 0

    def test_password_reset_form_invalid_data(self):
        """
        Test for CustomPasswordResetForm with invalid data
        """
        data = {"email": "test"}
        form = CustomPasswordResetForm(data=data)
        assert not form.is_valid()
        assert len(form.errors) == 1

    def test_password_reset_form_no_data(self):
        """
        Test for CustomPasswordResetForm with no data
        """
        data = {}
        form = CustomPasswordResetForm(data=data)
        assert not form.is_valid()
        assert len(form.errors) == 1

    def test_reset_password_valid_data(self):
        """
        Test for ReSetPasswordForm with valid data
        """
        data = {"new_password": "a/1234567", "new_password1": "a/1234567"}
        form = ReSetPasswordForm(data=data)
        assert form.is_valid()
        assert len(form.errors) == 0

    def test_reset_password_mismatch_password(self):
        """
        Test for ReSetPasswordForm with mismatch password
        """
        data = {
            "new_password": "a/1234567",
            "new_password1": "123a/1234567",
        }
        try:
            form = ReSetPasswordForm(data=data)
        except ValidationError:
            assert not form.is_valid()
            assert len(form.errors) == 1

    def test_reset_password_simple_password(self):
        """
        Test for ReSetPasswordForm with not complex data
        """
        data = {"new_password": "234567", "new_password1": "234567"}
        try:
            form = ReSetPasswordForm(data=data)
        except ValidationError:
            assert not form.is_valid()
            assert len(form.errors) == 1
