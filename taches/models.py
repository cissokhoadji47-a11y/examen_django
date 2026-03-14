from django.db import models
from django.conf import settings
from django.db.models import F
from projets.models import Projet


class Tache(models.Model):
    """
    Modèle représentant une tâche
    """
    STATUT_CHOIX = [
        ('a_faire', 'À faire'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name='taches',
        verbose_name="Projet"
    )
    assigne_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='taches',
        verbose_name="Assigné à"
    )
    date_limite = models.DateField(verbose_name="Date limite")
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOIX,
        default='a_faire',
        verbose_name="Statut"
    )
    date_fin_reelle = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin réelle"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titre} - {self.projet.titre}"

    def est_dans_les_delais(self):
        """
        Vérifie si la tâche a été terminée dans les délais
        """
        if self.statut == 'termine' and self.date_fin_reelle:
            return self.date_fin_reelle <= self.date_limite
        return False

    def sauvegarder_terminaison(self):
        """
        Marque la tâche comme terminée avec la date du jour
        """
        from django.utils import timezone
        self.statut = 'termine'
        self.date_fin_reelle = timezone.now().date()
        self.save()

    class Meta:
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"
        ordering = ['date_limite', 'statut']