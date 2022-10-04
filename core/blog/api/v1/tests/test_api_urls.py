import pytest
from django.urls import resolve, reverse

from .. import views


@pytest.mark.django_db
class TestBlogApiUrls:
    def test_blog_post_list_create_api_url(self):
        url = reverse("blog:api-v1:post-list")
        assert (
            resolve(url).func.view_class
            == views.BlogIndexListCreateAPIView
        )

    def test_blog_post_single_RUD_api_url(self):
        url = reverse("blog:api-v1:post-single", kwargs={"pk": 1})
        assert (
            resolve(url).func.view_class
            == views.BlogSingleRetrieveUpdateDeleteAPIView
        )

    def test_category_list_create_api_url(self):
        url = reverse("blog:api-v1:category")
        assert (
            resolve(url).func.view_class == views.CategoryListCreateAPIView
        )
