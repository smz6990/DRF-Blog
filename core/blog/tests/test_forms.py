import pytest
from datetime import datetime

from ..forms import PostForm, CategoryForm, CommentForm
from accounts.models import Profile, User
from ..models import Post


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


class TestPostForm:
    def test_post_form_valid_data(self):
        data = {
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
            "captcha": 1,
        }
        post = PostForm(data=data)
        # post is not valid because of captcha field
        assert not post.is_valid()
        assert len(post.errors) == 1
        assert post.has_error("captcha")

    def test_post_form_missing_field_data(self):
        data = {
            "title": "test title",
            "content": "test content",
            "captcha": 1,
        }
        post = PostForm(data=data)
        # post is not valid because of captcha field and
        # missing published_date field
        assert not post.is_valid()
        assert len(post.errors) == 2
        assert post.has_error("captcha")
        assert post.has_error("published_date")

    def test_post_form_no_data(self):
        post = PostForm()
        assert not post.is_valid()


@pytest.mark.django_db
class TestCommentForm:
    def test_comment_form_valid_data(self, create_post):
        data = {
            "post": create_post.id,
            "name": "test",
            "email": "test@test.com",
            "message": "test message",
        }
        comment = CommentForm(data=data)
        assert comment.is_valid()
        assert len(comment.errors) == 0

    def test_comment_form_invalid_data(self, create_post):
        data = {
            "post": create_post.id,
            "name": "test",
            "email": "invalid email format",
            "message": "test message",
        }
        comment = CommentForm(data=data)
        assert not comment.is_valid()
        assert len(comment.errors) == 1

    def test_comment_form_invalid_data_missing_post_field(self):
        data = {
            "name": "test",
            "email": "test@test.com",
            "message": "test message",
        }
        comment = CommentForm(data=data)
        assert not comment.is_valid()
        assert len(comment.errors) == 1


class TestCategoryForm:
    def test_category_form_valid_data(self):
        data = {"name": "test", "captcha": 1}
        cat = CategoryForm(data=data)
        # category is not valid because of captcha field
        assert not cat.is_valid()
        assert len(cat.errors) == 1
        assert cat.has_error("captcha")

    def test_category_form_invalid_data(self):
        cat = CategoryForm()
        assert not cat.is_valid()
