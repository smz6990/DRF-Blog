import pytest
from datetime import datetime

from ..models import Post, Category, Comment
from accounts.models import Profile, User


@pytest.fixture
def create_test_user():
    data = {"email": "test@test.com", "password": "a/1234567"}
    return User.objects.create_user(**data, is_verify=True)


@pytest.fixture
def user_profile(create_test_user):
    user = create_test_user
    return Profile.objects.get(user=user)


@pytest.fixture
def create_post(user_profile):
    data = {
        "author": user_profile,
        "title": "test title",
        "content": "test content",
        "published_date": datetime.now(),
    }
    return Post.objects.create(**data)


@pytest.mark.django_db
class TestPostModel:
    def test_post_model_valid_data(self, user_profile):
        data = {
            "author": user_profile,
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
        }
        post = Post.objects.create(**data)
        assert Post.objects.count() == 1
        assert Post.objects.filter(title="test title").exists()
        assert post.title == "test title"
        assert post.author == user_profile
        assert post.content == "test content"


@pytest.mark.django_db
class TestCategoryModel:
    def test_category_model_valid_data(self):
        cat = Category.objects.create(name="test")
        assert Category.objects.count() == 1
        assert Category.objects.filter(name="test").exists()
        assert cat.name == "test"


@pytest.mark.django_db
class TestCommentModel:
    def test_comment_model_valid_data(self, create_post):
        data = {
            "post": create_post,
            "name": "test",
            "email": "test@test.com",
            "message": "test message",
        }
        comment_obj = Comment.objects.create(**data)
        assert Comment.objects.count() == 1
        assert Comment.objects.filter(post=create_post).exists()
        assert comment_obj.post == create_post
        assert comment_obj.name == "test"
        assert comment_obj.email == "test@test.com"
        assert comment_obj.message == "test message"
