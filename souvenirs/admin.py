from django.contrib import admin

from .models import Profil, Publication, Commentaire, Like


# =========================================================
# PROFIL
# =========================================================

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "niveau",
        "promotion",
        "date_creation",
    )

    list_filter = (
        "niveau",
        "promotion",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )


# =========================================================
# PUBLICATION
# =========================================================

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):

    list_display = (
        "auteur",
        "type",
        "annee",
        "date_creation",
    )

    list_filter = (
        "type",
        "annee",
        "date_creation",
    )

    search_fields = (
        "auteur__username",
        "auteur__first_name",
        "auteur__last_name",
        "texte",
    )

    readonly_fields = (
        "date_creation",
    )


# =========================================================
# COMMENTAIRE
# =========================================================

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):

    list_display = (
        "auteur",
        "publication",
        "date_creation",
    )

    list_filter = (
        "date_creation",
    )

    search_fields = (
        "auteur__username",
        "auteur__first_name",
        "auteur__last_name",
        "texte",
    )

    readonly_fields = (
        "date_creation",
    )


# =========================================================
# LIKE
# =========================================================

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = (
        "utilisateur",
        "publication",
        "date_creation",
    )

    list_filter = (
        "date_creation",
    )

    search_fields = (
        "utilisateur__username",
        "utilisateur__first_name",
        "utilisateur__last_name",
    )

    readonly_fields = (
        "date_creation",
    )