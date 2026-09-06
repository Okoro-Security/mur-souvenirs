from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profil, Publication, Commentaire, Like

from .serializers import (
    UserSerializer,
    ProfilSerializer,
    PublicationSerializer,
    CommentaireSerializer,
    RegisterSerializer,
)


# =========================================================
# PAGES HTML
# =========================================================

def accueil(request):
    return render(request, "index.html")


@ensure_csrf_cookie
def page_login(request):
    return render(request, "login.html")


@ensure_csrf_cookie
def page_register(request):
    return render(request, "register.html")


@ensure_csrf_cookie
def page_publication(request):
    return render(request, "publication.html")


def page_publications(request):
    return render(request, "publications.html")


@ensure_csrf_cookie
def page_profil(request):
    return render(request, "profil.html")


# =========================================================
# CONNEXION
# =========================================================

class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {
                    "detail": "Nom d'utilisateur et mot de passe requis."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {
                    "detail": "Nom d'utilisateur ou mot de passe incorrect."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        return Response(
            {
                "message": "Connexion réussie.",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# DÉCONNEXION
# =========================================================

class LogoutView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        logout(request)

        return Response(
            {
                "message": "Déconnexion réussie."
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# PUBLICATIONS
# =========================================================

class PublicationListCreateView(generics.ListCreateAPIView):

    queryset = Publication.objects.all()

    serializer_class = PublicationSerializer

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def perform_create(self, serializer):

        serializer.save(
            auteur=self.request.user
        )


# =========================================================
# DÉTAIL D'UNE PUBLICATION
# =========================================================

class PublicationDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Publication.objects.all()

    serializer_class = PublicationSerializer

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def perform_update(self, serializer):

        publication = self.get_object()

        if publication.auteur != self.request.user:
            raise PermissionDenied(
                "Tu ne peux modifier que tes propres publications."
            )

        serializer.save()

    def perform_destroy(self, instance):

        if instance.auteur != self.request.user:
            raise PermissionDenied(
                "Tu ne peux supprimer que tes propres publications."
            )

        instance.delete()


# =========================================================
# COMMENTAIRES
# =========================================================

class CommentaireCreateView(generics.CreateAPIView):

    serializer_class = CommentaireSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def perform_create(self, serializer):

        publication_id = self.kwargs.get(
            "publication_id"
        )

        publication = get_object_or_404(
            Publication,
            id=publication_id
        )

        serializer.save(
            auteur=self.request.user,
            publication=publication
        )


# =========================================================
# LIKE / UNLIKE
# =========================================================

class LikePublicationView(APIView):

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, publication_id):

        publication = get_object_or_404(
            Publication,
            id=publication_id
        )

        like = Like.objects.filter(
            utilisateur=request.user,
            publication=publication
        ).first()

        if like:

            like.delete()

            return Response(
                {
                    "message": "Like retiré.",
                    "liked": False,
                    "nombre_likes": publication.likes.count()
                },
                status=status.HTTP_200_OK
            )

        Like.objects.create(
            utilisateur=request.user,
            publication=publication
        )

        return Response(
            {
                "message": "Publication aimée.",
                "liked": True,
                "nombre_likes": publication.likes.count()
            },
            status=status.HTTP_201_CREATED
        )


# =========================================================
# PROFIL
# =========================================================

class ProfilView(APIView):

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):

        profil = get_object_or_404(
            Profil,
            user=request.user
        )

        serializer = ProfilSerializer(profil)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request):

        profil = get_object_or_404(
            Profil,
            user=request.user
        )

        serializer = ProfilSerializer(
            profil,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# INSCRIPTION
# =========================================================

class RegisterView(APIView):

    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "Compte créé avec succès.",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# LISTE DES UTILISATEURS
# =========================================================

class UserListView(generics.ListAPIView):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [
        permissions.AllowAny
    ]