# taches/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('creer/<int:projet_id>/', views.creer_tache, name='creer_tache'),
    path('<int:tache_id>/modifier/', views.modifier_tache, name='modifier_tache'),
    path('<int:tache_id>/supprimer/', views.supprimer_tache, name='supprimer_tache'),
    path('<int:tache_id>/changer-statut/', views.changer_statut, name='changer_statut'),

    # NOUVELLES URLS
    path('statistiques/', views.statistiques_personnelles, name='statistiques'),
    path('classement-primes/', views.classement_primes, name='classement_primes'),
]