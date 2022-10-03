from django.urls import resolve, reverse

from .. import views


class TestWebsiteUrlsResolve:
    def test_index_view_url(self):
        url = reverse("website:index")
        assert resolve(url).func.view_class == views.IndexView

    def test_about_view_url(self):
        url = reverse("website:about")
        assert resolve(url).func.view_class == views.AboutView

    def test_contact_view_url(self):
        url = reverse("website:contact")
        assert resolve(url).func.view_class == views.ContactView

    def test_newsletter_view_url(self):
        url = reverse("website:newsletter")
        assert resolve(url).func.view_class == views.NewsletterView
