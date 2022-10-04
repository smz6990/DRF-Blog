import pytest

from ..models import User, Profile


@pytest.fixture
def basic_user():
    data = {"email": "test@test.com", "password": "a/1234567"}
    return User.objects.create_user(**data)


@pytest.mark.django_db
class TestAccountsModel:
    def test_user_model_valid_data_basic_user(self):
        """
        Test User model with basic user
        """
        data = {"email": "test@test.com"}
        user_obj = User.objects.create(**data)
        assert user_obj.email == data.get("email")
        assert User.objects.filter(email=data["email"]).exists()
        assert User.objects.count() == 1
        assert not user_obj.is_staff
        assert user_obj.is_active
        assert not user_obj.is_superuser
        assert not user_obj.is_verify

    def test_user_model_valid_data_with_user_password(self):
        """
        Test User model with user and password
        """
        data = {"email": "test@test.com", "password": "a/1234567"}
        user_obj = User.objects.create_user(**data)
        assert user_obj.email == data.get("email")
        assert User.objects.filter(email=data["email"]).exists()
        assert User.objects.count() == 1
        assert not user_obj.is_staff
        assert user_obj.is_active
        assert not user_obj.is_superuser
        assert not user_obj.is_verify

    def test_profile_model_valid_data(self, basic_user):
        """
        Test Profile model with valid data
        """
        user = basic_user
        data = {
            "user": user,
            "first_name": "first_name",
            "last_name": "last_name",
            "description": "description",
        }
        profile_obj = Profile.objects.create(**data)
        assert Profile.objects.filter(user=user).exists()
        assert Profile.objects.count() == 2
        assert profile_obj.user == user
        assert profile_obj.first_name == "first_name"
        assert profile_obj.last_name == "last_name"
        assert profile_obj.description == "description"
