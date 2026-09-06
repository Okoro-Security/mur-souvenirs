from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from souvenirs.views import (
    accueil,
    page_login,
    page_register,
    page_publication,
    page_profil,
    page_publications,
)


urlpatterns = [

    path("", accueil, name="accueil"),

    path("login/", page_login, name="page-login"),

    path("register/", page_register, name="page-register"),

    path("publication/", page_publication, name="page-publication"),

    path("publications/", page_publications, name="page-publications"),

    path("profil/", page_profil, name="page-profil"),

    path("admin/", admin.site.urls),

    path("api/", include("souvenirs.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )