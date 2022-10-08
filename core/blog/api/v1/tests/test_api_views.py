from datetime import datetime
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

from ....models import Post
from accounts.models import Profile


User = get_user_model()


@pytest.fixture
def anonymous_user():
    return APIClient()


@pytest.fixture
def test_user():
    data = {"email": "test@test.com", "password": "a/1234567"}
    user = User.objects.create(**data, is_verify=True)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def owner_user():
    data = {"email": "owner@owner.com", "password": "a/1234567"}
    user = User.objects.create(**data, is_verify=True)
    client = APIClient()
    client.force_authenticate(user=user)
    return user, client


@pytest.fixture
def post_by_owner(owner_user):
    user_obj, client_obj = owner_user
    author = Profile.objects.get(user=user_obj)
    data = {
        "author": author,
        "title": "test title",
        "content": "test content",
        "status": True,
        "published_date": datetime.now(),
    }
    post_obj = Post.objects.create(**data)
    return post_obj, client_obj


@pytest.mark.django_db
class TestBlogApiViews:
    def test_blog_index_list_create_api_GET_anonymous_user(
        self, anonymous_user
    ):
        """
        Test BlogIndexListCreateAPIView by GET method with anonymous user
        """
        url = reverse("blog:api-v1:post-list")
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_blog_index_list_create_api_POST_anonymous_user(
        self, anonymous_user
    ):
        """
        Test BlogIndexListCreateAPIView by POST method with anonymous user
        """
        url = reverse("blog:api-v1:post-list")
        response = anonymous_user.post(url)
        assert response.status_code == 401

    def test_blog_index_list_create_api_GET_logged_user(self, test_user):
        """
        Test BlogIndexListCreateAPIView by GET method with authenticated user
        """
        url = reverse("blog:api-v1:post-list")
        response = test_user.get(url)
        assert response.status_code == 200

    def test_blog_index_list_create_api_POST_logged_user_valid_data(
        self, test_user
    ):
        """
        Test BlogIndexListCreateAPIView by POST method with authenticated
        user with valid data
        """
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
        }
        response = test_user.post(url, data)
        assert response.status_code == 201

    def test_blog_index_list_create_api_POST_logged_user_invalid_data(
        self, test_user
    ):
        """
        Test BlogIndexListCreateAPIView by POST method with authenticated
        user with invalid data
        """
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
        }
        response = test_user.post(url, data)
        assert response.status_code == 400

    def test_blog_single_RUT_api_GET_anonymous_user(
        self, anonymous_user, post_by_owner
    ):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by GET method with
        anonymous user
        """
        post, _ = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_blog_single_RUT_api_PUT_anonymous_user(
        self, anonymous_user, post_by_owner
    ):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by PUT method with
        anonymous user
        """
        post, _ = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        data = {
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
        }
        response = anonymous_user.put(url, data)
        assert response.status_code == 401

    def test_blog_single_RUT_api_PATCH_anonymous_user(
        self, anonymous_user, post_by_owner
    ):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by PATCH method with
        anonymous user
        """
        post, _ = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        data = {
            "content": "test patch content",
        }
        response = anonymous_user.patch(url, data)
        assert response.status_code == 401

    def test_blog_single_RUT_api_DELETE_anonymous_user(
        self, anonymous_user, post_by_owner
    ):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by DELETE method with
        anonymous user
        """
        post, _ = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        response = anonymous_user.delete(url)
        assert response.status_code == 401

    def test_blog_single_RUT_api_GET_test_user(
        self, test_user, post_by_owner
    ):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by GET method with
        logged user
        """
        post, _ = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        response = test_user.get(url)
        assert response.status_code == 200

    def test_blog_single_RUT_api_PUT_test_user(
        self, test_user, post_by_owner
    ):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by PUT method with
        logged user
        """
        post, _ = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        data = {
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
        }
        response = test_user.put(url, data)
        assert response.status_code == 403

    def test_blog_single_RUT_api_PATCH_test_user(
        self, test_user, post_by_owner
    ):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by PATCH method with
        logged user
        """
        post, _ = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        data = {
            "content": "test patch content",
        }
        response = test_user.patch(url, data)
        assert response.status_code == 403

    def test_blog_single_RUT_api_DELETE_test_user(
        self, test_user, post_by_owner
    ):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by DELETE method with
        logged user
        """
        post, _ = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        response = test_user.delete(url)
        assert response.status_code == 403

    def test_blog_single_RUT_api_GET_owner_user(self, post_by_owner):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by GET method with
        post owner
        """
        post, client = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        response = client.get(url)
        assert response.status_code == 200

    def test_blog_single_RUT_api_PUT_owner_user(self, post_by_owner):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by PUT method with
        post owner
        """
        post, client = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        data = {
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
        }
        response = client.put(url, data)
        assert response.status_code == 200

    def test_blog_single_RUT_api_PATCH_owner_user(self, post_by_owner):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by PATCH method with
        post owner
        """
        post, client = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        data = {
            "content": "test patch content",
        }
        response = client.patch(url, data)
        assert response.status_code == 200

    def test_blog_single_RUT_api_DELETE_owner_user(self, post_by_owner):
        """
        Test BlogSingleRetrieveUpdateDeleteAPIView by DELETE method with
        post owner
        """
        post, client = post_by_owner
        url = reverse("blog:api-v1:post-single", kwargs={"pk": post.id})
        response = client.delete(url)
        assert response.status_code == 204

    def test_blog_category_list_create_api_GET_anonymous_user(
        self, anonymous_user
    ):
        """
        Test CategoryListCreateAPIView by GET method with anonymous user
        """
        url = reverse("blog:api-v1:category")
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_blog_category_list_create_api_POST_anonymous_user(
        self, anonymous_user
    ):
        """
        Test CategoryListCreateAPIView by POST method with anonymous user
        """
        url = reverse("blog:api-v1:category")
        data = {"name": "test"}
        response = anonymous_user.post(url, data)
        assert response.status_code == 401

    def test_blog_category_list_create_api_GET_logged_user(self, test_user):
        """
        Test CategoryListCreateAPIView by GET method with authenticated user
        """
        url = reverse("blog:api-v1:category")
        response = test_user.get(url)
        assert response.status_code == 200

    def test_blog_category_list_create_api_POST_logged_user_valid_data(
        self, test_user
    ):
        """
        Test CategoryListCreateAPIView by POST method with authenticated
        user with valid data
        """
        url = reverse("blog:api-v1:category")
        data = {"name": "test"}
        response = test_user.post(url, data)
        assert response.status_code == 201

    def test_blog_category_list_create_api_POST_logged_user_invalid_data(
        self, test_user
    ):
        """
        Test CategoryListCreateAPIView by POST method with authenticated
        user with invalid data
        """
        url = reverse("blog:api-v1:category")
        data = {}
        response = test_user.post(url, data)
        assert response.status_code == 400
