from datetime import datetime
import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Category, Post
from accounts.models import Profile, User


@pytest.fixture
def create_basic_user():
    data = {"email": "test@test.com", "password": "a/1234567"}
    return User.objects.create_user(**data, is_verify=True)


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


@pytest.fixture
def user_profile(create_basic_user):
    user = create_basic_user
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


@pytest.fixture
def create_post_not_owner():
    user = User.objects.create_user(
        email="test2@test@.com", password="a/1234567"
    )
    profile = Profile.objects.create(user=user)
    data = {
        "author": profile,
        "title": "user2 title",
        "content": "user2 content",
        "published_date": datetime.now(),
    }
    return Post.objects.create(**data)


@pytest.fixture
def create_category():
    return Category.objects.create(name="category")


@pytest.mark.django_db
class TestBlogViews:
    def test_blog_index_view_GET_anonymous_user(self, anonymous_user):
        """
        testing BlogIndexView by GET method with anonymous user
        """
        url = reverse("blog:index")
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_blog_single_view_GET_anonymous_user_existing_post(
        self, anonymous_user, create_post
    ):
        """
        testing BlogSingleView by GET method with anonymous user
        with existing post
        """
        post = create_post
        post.status = True
        post.save()
        url = reverse("blog:single", kwargs={"pk": post.id})
        response = anonymous_user.get(url)
        assert response.status_code == 200

    def test_blog_single_view_GET_anonymous_user_no_existing_post(
        self, anonymous_user, create_post
    ):
        """
        testing BlogSingleView by GET method with anonymous user
        with NOT existing post
        """
        post = create_post
        post.status = True
        url = reverse("blog:single", kwargs={"pk": post.id})
        post.delete()
        response = anonymous_user.get(url)
        assert response.status_code == 404

    def test_blog_create_post_view_GET_auth_user_verified(self, logged_user):
        """
        Testing BlogCreatePostView in GET method with authorized and
        verified user
        """
        url = reverse("blog:create-post")
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_blog_create_post_view_GET_auth_user_not_verified(
        self, not_verified_user
    ):
        """
        Testing BlogCreatePostView in GET method with authorized and
        NOT verified user
        """
        url = reverse("blog:create-post")
        response = not_verified_user.get(url)
        assert response.status_code == 403

    def test_blog_create_post_view_GET_anonymous_user(self, anonymous_user):
        """
        Testing BlogCreatePostView in GET method with not authorized user
        """
        url = reverse("blog:create-post")
        response = anonymous_user.get(url)
        # redirect to login page
        assert response.status_code == 302

    def test_blog_create_post_view_POST_auth_user_verified(
        self, logged_user
    ):
        """
        Testing BlogCreatePostView in GET method with authorized and
        verified user
        """
        url = reverse("blog:create-post")
        profile = Profile.objects.get(user__email="test@test.com")
        data = {
            "author": profile,
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
            "captcha": 1,
        }
        response = logged_user.post(url, data)
        # because of captcha field, POST method not completed and gets back to
        # the same page to correct the posting form (if new post was created
        # response would be 201)
        assert response.status_code == 200

    def test_blog_create_post_view_POST_auth_user_not_verified(
        self, not_verified_user
    ):
        """
        Testing BlogCreatePostView in GET method with authorized and
        NOT verified user
        """
        profile = Profile.objects.get(user__email="test@test.com")
        data = {
            "author": profile,
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
            "captcha": 1,
        }
        url = reverse("blog:create-post")
        response = not_verified_user.post(url, data)
        assert response.status_code == 403

    def test_blog_create_post_view_POST_anonymous_user(self, anonymous_user):
        """
        Testing BlogCreatePostView in GET method with not authorized user
        """
        url = reverse("blog:create-post")
        response = anonymous_user.post(url, data={})
        # redirect to login page
        assert response.status_code == 302

    def test_blog_edit_post_view_GET_auth_user_verified_and_owner(
        self, logged_user, create_post
    ):
        """
        Testing BlogEditPostView in GET method with authorized and
        verified user and user is owner of post
        """
        post = create_post
        url = reverse("blog:edit-post", kwargs={"pk": post.id})
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_blog_edit_post_view_GET_auth_user_verified_but_not_owner(
        self, logged_user, create_post_not_owner
    ):
        """
        Testing BlogEditPostView in GET method with authorized and
        verified user BUT NOT owner of post
        """
        post = create_post_not_owner
        url = reverse("blog:edit-post", kwargs={"pk": post.id})
        response = logged_user.get(url)
        # because its not the owner ,redirect to blog index
        assert response.status_code == 302

    def test_blog_edit_post_view_GET_auth_user_not_verified(
        self, not_verified_user, create_post
    ):
        """
        Testing BlogEditPostView in GET method with authorized and
        NOT verified user
        """
        post = create_post
        url = reverse("blog:edit-post", kwargs={"pk": post.id})
        response = not_verified_user.get(url)
        assert response.status_code == 403

    def test_blog_edit_post_view_GET_anonymous_user(
        self, anonymous_user, create_post
    ):
        """
        Testing BlogEditPostView in GET method with anonymous user
        """
        post = create_post
        url = reverse("blog:edit-post", kwargs={"pk": post.id})
        response = anonymous_user.get(url)
        # redirect to login page
        assert response.status_code == 302

    def test_blog_edit_post_view_POST_auth_user_verified(
        self, logged_user, create_post
    ):
        """
        Testing BlogEditPostView in GET method with authorized and
        verified user and user is the OWNER of post
        """
        post = create_post
        url = reverse("blog:edit-post", kwargs={"pk": post.id})
        data = {
            "author": post.author,
            "title": "test edit post title",
            "content": "test edit post content",
            "published_date": datetime.now(),
            "captcha": 1,
        }
        response = logged_user.post(url, data)
        # because of captcha field, POST method not completed and gets back to
        # the same page to correct the posting form (if new post was created
        # response would be 201)
        assert response.status_code == 200

    def test_blog_edit_post_view_POST_auth_user_verified_but_not_owner(
        self, logged_user, create_post_not_owner
    ):
        """
        Testing BlogEditPostView in POST method with authorized and
        verified user BUT NOT owner of post
        """
        post = create_post_not_owner
        url = reverse("blog:edit-post", kwargs={"pk": post.id})
        data = {
            "author": post.author,
            "title": "test edit post not owner",
            "content": "test edit post not owner",
            "published_date": datetime.now(),
            "captcha": 1,
        }
        response = logged_user.post(url, data)
        # because its not the owner, its redirects to blog index
        assert response.status_code == 302

    def test_blog_edit_post_view_POST_auth_user_not_verified(
        self, not_verified_user, create_post
    ):
        """
        Testing BlogEditPostView in POST method with authorized and
        NOT verified user
        """
        post = create_post
        data = {
            "author": post.author,
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
            "captcha": 1,
        }
        url = reverse("blog:edit-post", kwargs={"pk": post.id})
        response = not_verified_user.post(url, data)
        assert response.status_code == 403

    def test_blog_edit_post_view_POST_anonymous_user(
        self, anonymous_user, create_post
    ):
        """
        Testing BlogEditPostView in POST method with anonymous user
        """
        post = create_post
        url = reverse("blog:edit-post", kwargs={"pk": post.id})
        data = {
            "author": post.author,
            "title": "test title",
            "content": "test content",
            "published_date": datetime.now(),
            "captcha": 1,
        }
        response = anonymous_user.post(url, data=data)
        # redirect to login page
        assert response.status_code == 302

    def test_blog_delete_post_view_GET_auth_user_verified_owner(
        self, logged_user, create_post
    ):
        """
        Testing BlogDeletePostView in GET method with authorized and
        verified user and user is owner of post
        """
        post = create_post
        url = reverse("blog:delete-post", kwargs={"pk": post.id})
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_blog_delete_post_view_GET_auth_user_verified_but_not_owner(
        self, logged_user, create_post_not_owner
    ):
        """
        Testing BlogDeletePostView in GET method with authorized and
        verified user BUT NOT owner of post
        """
        post = create_post_not_owner
        url = reverse("blog:delete-post", kwargs={"pk": post.id})
        response = logged_user.get(url)
        # because its not the owner ,redirect to blog index
        assert response.status_code == 302

    def test_blog_delete_post_view_GET_auth_user_not_verified(
        self, not_verified_user, create_post
    ):
        """
        Testing BlogDeletePostView in GET method with authorized and
        NOT verified user
        """
        post = create_post
        url = reverse("blog:delete-post", kwargs={"pk": post.id})
        response = not_verified_user.get(url)
        assert response.status_code == 403

    def test_blog_delete_post_view_GET_anonymous_user(
        self, anonymous_user, create_post
    ):
        """
        Testing BlogEditPostView in GET method with anonymous user
        """
        post = create_post
        url = reverse("blog:delete-post", kwargs={"pk": post.id})
        response = anonymous_user.get(url)
        # redirect to login page
        assert response.status_code == 302

    def test_blog_delete_post_view_DELETE_auth_user_verified_owner(
        self, logged_user, create_post
    ):
        """
        Testing BlogDeletePostView in DELETE method with authorized and
        verified user and user is owner of post
        """
        post = create_post
        url = reverse("blog:delete-post", kwargs={"pk": post.id})
        response = logged_user.delete(url)
        assert response.status_code == 302

    def test_blog_delete_post_view_DELETE_auth_user_verified_but_not_owner(
        self, logged_user, create_post_not_owner
    ):
        """
        Testing BlogDeletePostView in DELETE method with authorized and
        verified user BUT NOT owner of post
        """
        post = create_post_not_owner
        url = reverse("blog:delete-post", kwargs={"pk": post.id})
        response = logged_user.delete(url)
        # because its not the owner ,redirect to blog index
        assert response.status_code == 302

    def test_blog_delete_post_view_DELETE_auth_user_not_verified(
        self, not_verified_user, create_post
    ):
        """
        Testing BlogDeletePostView in DELETE method with authorized and
        NOT verified user
        """
        post = create_post
        url = reverse("blog:delete-post", kwargs={"pk": post.id})
        response = not_verified_user.delete(url)
        assert response.status_code == 403

    def test_blog_delete_post_view_DELETE_anonymous_user(
        self, anonymous_user, create_post
    ):
        """
        Testing BlogEditPostView in DELETE method with anonymous user
        """
        post = create_post
        url = reverse("blog:delete-post", kwargs={"pk": post.id})
        response = anonymous_user.delete(url)
        # redirect to login page
        assert response.status_code == 302

    def test_blog_comment_create_view_POST_auth_user_verified(
        self, logged_user, create_post
    ):
        """
        Testing BlogCommentCreateView in POST method with authorized and
        verified user
        """
        post = create_post
        data = {
            "post": post,
            "name": "test comment",
            "email": "comment@test.com",
            "message": "comment message",
        }
        url = reverse("blog:comment")
        response = logged_user.post(url, data)
        assert response.status_code == 200

    def test_blog_comment_create_view_POST_auth_user_not_verified(
        self, not_verified_user, create_post
    ):
        """
        Testing BlogCommentCreateView in POST method with authorized but
        NOT verified user
        """
        post = create_post
        data = {
            "post": post,
            "name": "test comment",
            "email": "comment@test.com",
            "message": "comment message",
        }
        url = reverse("blog:comment")
        response = not_verified_user.post(url, data)
        assert response.status_code == 403

    def test_blog_comment_create_view_POST_anonymous_user(
        self, anonymous_user, create_post
    ):
        """
        Testing BlogCommentCreateView in POST method with anonymous user
        """
        post = create_post
        data = {
            "post": post,
            "name": "test comment",
            "email": "comment@test.com",
            "message": "comment message",
        }
        url = reverse("blog:comment")
        response = anonymous_user.post(url, data)
        # redirect to login page
        assert response.status_code == 302

    def test_category_list_view_GET_auth_user_verified(
        self, logged_user, create_category
    ):
        """
        Testing CategoryListView in POST method with authorized and
        verified user
        """
        cat = create_category
        url = reverse("blog:category", kwargs={"cat_name": cat.name})
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_category_list_view_GET_anonymous_user(
        self, anonymous_user, create_category
    ):
        """
        Testing CategoryListView in GET method with anonymous user
        """
        cat = create_category
        url = reverse("blog:category", kwargs={"cat_name": cat.name})
        response = anonymous_user.get(url)
        # redirect to login page
        assert response.status_code == 200

    def test_category_create_view_GET_auth_user_verified(self, logged_user):
        """
        Testing CategoryCreateView in GET method with authorized and
        verified user
        """
        url = reverse("blog:category-create")
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_category_create_view_GET_auth_user_not_verified(
        self, not_verified_user
    ):
        """
        Testing CategoryCreateView in GET method with authorized but
        NOT verified user
        """
        url = reverse("blog:category-create")
        response = not_verified_user.get(url)
        assert response.status_code == 403

    def test_category_create_view_GET_anonymous_user(self, anonymous_user):
        """
        Testing CategoryCreateView in GET method with anonymous user
        """
        url = reverse("blog:category-create")
        response = anonymous_user.get(url)
        # redirect to login page
        assert response.status_code == 302

    def test_category_create_view_POST_auth_user_verified(self, logged_user):
        """
        Testing CategoryCreateView in POST method with authorized and
        verified user
        """
        url = reverse("blog:category-create")
        response = logged_user.post(url, data={"name": "test"})
        assert response.status_code == 200

    def test_category_create_view_POST_auth_user_not_verified(
        self, not_verified_user
    ):
        """
        Testing CategoryCreateView in POST method with authorized but
        NOT verified user
        """
        url = reverse("blog:category-create")
        response = not_verified_user.post(url, data={"name": "test"})
        assert response.status_code == 403

    def test_category_create_view_POST_anonymous_user(self, anonymous_user):
        """
        Testing CategoryCreateView in POST method with anonymous user
        """
        url = reverse("blog:category-create")
        response = anonymous_user.post(url, data={"name": "test"})
        # redirect to login page
        assert response.status_code == 302

    def test_search_view_GET_auth_user_verified(self, logged_user):
        """
        Testing SearchView in GET method with authorized and
        verified user
        """
        url = reverse("blog:search") + "?Search=test"
        response = logged_user.get(url)
        assert response.status_code == 200

    def test_search_view_GET_anonymous_user(self, anonymous_user):
        """
        Testing SearchView in GET method with anonymous user
        """
        url = reverse("blog:search") + "?Search=test"
        response = anonymous_user.get(url)
        assert response.status_code == 200
