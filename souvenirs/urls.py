from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # PUBLICATIONS
    # =====================================================

    path(
        "publications/",
        views.PublicationListCreateView.as_view(),
        name="publications"
    ),

    path(
        "publications/<int:pk>/",
        views.PublicationDetailView.as_view(),
        name="publication-detail"
    ),

    # =====================================================
    # COMMENTAIRES
    # =====================================================

    path(
        "publications/<int:publication_id>/commentaires/",
        views.CommentaireCreateView.as_view(),
        name="commentaire-create"
    ),

    # =====================================================
    # LIKES
    # =====================================================

    path(
        "publications/<int:publication_id>/like/",
        views.LikePublicationView.as_view(),
        name="publication-like"
    ),

    # =====================================================
    # PROFIL
    # =====================================================

    path(
        "profil/",
        views.ProfilView.as_view(),
        name="profil"
    ),

    # =====================================================
    # INSCRIPTION
    # =====================================================

    path(
        "register/",
        views.RegisterView.as_view(),
        name="register"
    ),

    # =====================================================
    # CONNEXION
    # =====================================================

    path(
        "login/",
        views.LoginView.as_view(),
        name="login"
    ),

    # =====================================================
    # DÉCONNEXION
    # =====================================================

    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout"
    ),

    # =====================================================
    # UTILISATEURS
    # =====================================================

    path(
        "utilisateurs/",
        views.UserListView.as_view(),
        name="utilisateurs"
    ),
]