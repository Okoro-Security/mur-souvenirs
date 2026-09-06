from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profil, Publication, Commentaire, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]
        read_only_fields = ["id"]


class ProfilSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profil
        fields = [
            "id",
            "user",
            "niveau",
            "promotion",
            "photo",
            "bio",
            "date_creation",
        ]
        read_only_fields = [
            "id",
            "date_creation",
        ]


class CommentaireSerializer(serializers.ModelSerializer):
    auteur = UserSerializer(read_only=True)

    class Meta:
        model = Commentaire
        fields = [
            "id",
            "publication",
            "auteur",
            "texte",
            "date_creation",
        ]
        read_only_fields = [
            "id",
            "publication",
            "auteur",
            "date_creation",
        ]


class LikeSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = [
            "id",
            "publication",
            "utilisateur",
            "date_creation",
        ]
        read_only_fields = [
            "id",
            "utilisateur",
            "date_creation",
        ]


class PublicationSerializer(serializers.ModelSerializer):
    auteur = UserSerializer(read_only=True)

    commentaires = CommentaireSerializer(
        many=True,
        read_only=True
    )

    nombre_likes = serializers.SerializerMethodField()

    nombre_commentaires = serializers.SerializerMethodField()

    a_deja_like = serializers.SerializerMethodField()

    est_auteur = serializers.SerializerMethodField()

    class Meta:
        model = Publication

        fields = [
            "id",
            "auteur",
            "type",
            "texte",
            "image",
            "annee",
            "date_creation",
            "commentaires",
            "nombre_likes",
            "nombre_commentaires",
            "a_deja_like",
            "est_auteur",
        ]

        read_only_fields = [
            "id",
            "auteur",
            "date_creation",
            "commentaires",
            "nombre_likes",
            "nombre_commentaires",
            "a_deja_like",
            "est_auteur",
        ]

    def get_nombre_likes(self, obj):
        return obj.likes.count()

    def get_nombre_commentaires(self, obj):
        return obj.commentaires.count()

    def get_a_deja_like(self, obj):
        request = self.context.get("request")

        if not request:
            return False

        if not request.user.is_authenticated:
            return False

        return obj.likes.filter(
            utilisateur=request.user
        ).exists()

    def get_est_auteur(self, obj):
        request = self.context.get("request")

        if not request:
            return False

        if not request.user.is_authenticated:
            return False

        return obj.auteur == request.user


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    niveau = serializers.ChoiceField(
        choices=[
            ("L1", "Licence 1"),
            ("L2", "Licence 2"),
            ("L3", "Licence 3"),
        ],
        write_only=True
    )

    promotion = serializers.CharField(
        write_only=True,
        max_length=50
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "niveau",
            "promotion",
        ]

    def create(self, validated_data):
        niveau = validated_data.pop("niveau")
        promotion = validated_data.pop("promotion")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data.get("email", ""),
            password=password,
        )

        Profil.objects.create(
            user=user,
            niveau=niveau,
            promotion=promotion,
        )

        return user