from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .sitemaps import StaticViewSitemap
from blog.sitemaps import BlogSitemap

sitemaps = {"static": StaticViewSitemap, "blog": BlogSitemap}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", include("robots.urls")),
]

if settings.DEBUG:

    schema_view = get_schema_view(
        openapi.Info(
            title="Documentation API",
            default_version="v1",
            description="API description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="saleh.mohammadzadeh@gmail.com"),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns.append(path("api-auth/", include("rest_framework.urls")))
    urlpatterns.append(
        path("api-docs/", include_docs_urls(title="Api Documentations"))
    )
    urlpatterns.append(
        path(
            "swagger.json",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        )
    )
    urlpatterns.append(
        path(
            "swagger.yaml",
            schema_view.without_ui(cache_timeout=0),
            name="schema-yaml",
        )
    )
    urlpatterns.append(
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        )
    )
    urlpatterns.append(
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        )
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
