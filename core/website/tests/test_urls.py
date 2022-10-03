from django.urls import resolve, reverse

from .. import views


class TestWebsiteUrlsResolve:
    def test_url_index_view(self):
        url = reverse("website:index")
        assert resolve(url).func.view_class == views.IndexView

    def test_url_about_view(self):
        url = reverse("website:about")
        assert resolve(url).func.view_class == views.AboutView

    def test_url_contact_view(self):
        url = reverse("website:contact")
        assert resolve(url).func.view_class == views.ContactView

    def test_url_newsletter_view(self):
        url = reverse("website:newsletter")
        assert resolve(url).func.view_class == views.NewsletterView
