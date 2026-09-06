from django.db import models
from django.contrib.auth.models import User


# =========================================================
# PROFIL DE L'ÉTUDIANT
# =========================================================

class Profil(models.Model):

    NIVEAUX = [
        ("L1", "Licence 1"),
        ("L2", "Licence 2"),
        ("L3", "Licence 3"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profil"
    )

    niveau = models.CharField(
        max_length=2,
        choices=NIVEAUX
    )

    promotion = models.CharField(
        max_length=50
    )

    photo = models.ImageField(
        upload_to="profils/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# =========================================================
# PUBLICATION
# =========================================================

class Publication(models.Model):

    TYPES = [
        ("photo", "Photo"),
        ("discussion", "Discussion"),
        ("souvenir", "Souvenir"),
    ]

    auteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="publications"
    )

    type = models.CharField(
        max_length=20,
        choices=TYPES,
        default="souvenir"
    )

    texte = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="publications/",
        blank=True,
        null=True
    )

    annee = models.CharField(
        max_length=50,
        blank=True
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.auteur.username} - {self.type}"

    class Meta:
        ordering = ["-date_creation"]


# =========================================================
# COMMENTAIRE
# =========================================================

class Commentaire(models.Model):

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="commentaires"
    )

    auteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="commentaires"
    )

    texte = models.TextField()

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.auteur.username} : {self.texte[:30]}"


# =========================================================
# LIKE
# =========================================================

class Like(models.Model):

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["publication", "utilisateur"],
                name="unique_publication_like"
            )
        ]

    def __str__(self):
        return (
            f"{self.utilisateur.username} "
            f"aime la publication {self.publication.id}"
        )