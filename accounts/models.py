from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec rôles Étudiant/Professeur
    """
    EST_PROFESSEUR = 'professeur'
    EST_ETUDIANT = 'etudiant'

    CHOIX_ROLE = [
        (EST_PROFESSEUR, 'Professeur'),
        (EST_ETUDIANT, 'Étudiant'),
    ]

    role = models.CharField(
        max_length=20,
        choices=CHOIX_ROLE,
        default=EST_ETUDIANT,
        verbose_name="Rôle"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name="Photo de profil"
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Biographie"
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"