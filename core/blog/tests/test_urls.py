from django.urls import resolve, reverse

from .. import views


class TestBlogUrlsResolve:
    def test_url_blog_index_view(self):
        url = reverse("blog:index")
        assert resolve(url).func.view_class == views.BlogIndexView

    def test_url_blog_single_view(self):
        url = reverse("blog:single", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.BlogSingleView

    def test_url_blog_create_post_view(self):
        url = reverse("blog:create-post")
        assert resolve(url).func.view_class == views.BlogCreatePostView

    def test_url_blog_edit_post_view(self):
        url = reverse("blog:edit-post", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.BlogEditPostView

    def test_url_blog_delete_post_view(self):
        url = reverse("blog:delete-post", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.BlogDeletePostView

    def test_url_blog_comment_view(self):
        url = reverse("blog:comment")
        assert resolve(url).func.view_class == views.BlogCommentCreateView

    def test_url_blog_category_create_view(self):
        url = reverse("blog:category-create")
        assert resolve(url).func.view_class == views.CategoryCreateView

    def test_url_blog_category_view(self):
        url = reverse("blog:category", kwargs={"cat_name": "test"})
        assert resolve(url).func.view_class == views.CategoryListView

    def test_url_blog_search_view(self):
        url = reverse("blog:search")
        assert resolve(url).func.view_class == views.SearchView
