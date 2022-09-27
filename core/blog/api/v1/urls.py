from django.urls import path

from . import views


app_name = "api-v1"

urlpatterns = [
    path("", views.BlogIndexListCreateAPIView.as_view(), name="index"),
    path(
        "<int:pk>/",
        views.BlogSingleRetrieveUpdateDeleteAPIView.as_view(),
        name="single",
    ),
    path(
        "category/",
        views.CategoryListCreateAPIView.as_view(),
        name="category",
    ),
]
