import pytest
from django.test import Client
from django.urls import reverse


@pytest.fixture
def basic_user_client():
    return Client()


@pytest.mark.django_db
class TestWebsiteViews:
    def test_index_view_get_response_200(self, basic_user_client):
        url = reverse("website:index")
        response = basic_user_client.get(url)
        assert response.status_code == 200

    def test_about_view_get_response_200(self, basic_user_client):
        url = reverse("website:about")
        response = basic_user_client.get(url)
        assert response.status_code == 200

    def test_contact_view_get_response_200(self, basic_user_client):
        url = reverse("website:contact")
        response = basic_user_client.get(url)
        assert response.status_code == 200

    def test_contact_view_post_response_200(self, basic_user_client):
        url = reverse("website:contact")
        data = {
            "name": "test",
            "email": "test@test.com",
            "subject": "test subject",
            "message": "test message",
            "captcha": 1,
        }
        response = basic_user_client.post(url, data)
        assert response.status_code == 200

    def test_newsletter_view_post_response_302(self, basic_user_client):
        """after successful post , redirects to the index page"""
        url = reverse("website:newsletter")
        data = {
            "email": "test@test.com",
        }
        response = basic_user_client.post(url, data)
        assert response.status_code == 302
