# taches/utils.py
from datetime import datetime
from django.db.models import F  # ← Ajoute cette ligne !
from django.utils import timezone
from .models import Tache
from accounts.models import User


def calculer_statistiques_professeur(professeur, annee, trimestre=None):
    """
    Calcule les statistiques d'un professeur sur une période
    Retourne: (taux_reussite, montant_prime, total_taches, taches_reussies)
    """
    # Filtrer les tâches du professeur
    taches = Tache.objects.filter(
        assigne_a=professeur,
        date_limite__year=annee
    )

    # Filtrer par trimestre si spécifié
    if trimestre:
        if trimestre == 1:  # Jan-Mar
            taches = taches.filter(date_limite__month__in=[1, 2, 3])
        elif trimestre == 2:  # Avr-Juin
            taches = taches.filter(date_limite__month__in=[4, 5, 6])
        elif trimestre == 3:  # Juil-Sept
            taches = taches.filter(date_limite__month__in=[7, 8, 9])
        elif trimestre == 4:  # Oct-Dec
            taches = taches.filter(date_limite__month__in=[10, 11, 12])

    total_taches = taches.count()

    if total_taches == 0:
        return {
            'taux': 0,
            'prime': 0,
            'total': 0,
            'reussies': 0,
            'a_droit_prime': False
        }

    # Tâches terminées dans les délais
    taches_reussies = taches.filter(
        statut='termine',
        date_fin_reelle__lte=F('date_limite')  # ← C'est ici que F() est utilisé
    ).count()

    taux = (taches_reussies / total_taches) * 100

    # Calcul de la prime
    prime = 0
    if taux >= 100:
        prime = 100000
    elif taux >= 90:
        prime = 30000

    return {
        'taux': round(taux, 2),
        'prime': prime,
        'total': total_taches,
        'reussies': taches_reussies,
        'a_droit_prime': prime > 0
    }


def calculer_primes_tous_professeurs(annee):
    """Calcule les primes pour tous les professeurs sur une année"""
    professeurs = User.objects.filter(role='professeur')
    resultats = []

    for prof in professeurs:
        stats = calculer_statistiques_professeur(prof, annee)
        if stats['a_droit_prime']:
            resultats.append({
                'professeur': prof,
                'statistiques': stats
            })

    return resultats