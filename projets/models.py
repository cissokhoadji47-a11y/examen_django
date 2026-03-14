# projets/models.py
from django.db import models
from django.conf import settings


class Projet(models.Model):
    """
    Modèle représentant un projet
    """
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    createur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projets_crees',
        verbose_name="Créateur"
    )
    membres = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projets',
        verbose_name="Membres"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-date_creation']