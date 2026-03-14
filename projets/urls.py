# projets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_projets, name='liste_projets'),
    path('creer/', views.creer_projet, name='creer_projet'),
    path('<int:projet_id>/', views.detail_projet, name='detail_projet'),
    path('<int:projet_id>/modifier/', views.modifier_projet, name='modifier_projet'),
    path('<int:projet_id>/supprimer/', views.supprimer_projet, name='supprimer_projet'),
    path('<int:projet_id>/ajouter-membre/', views.ajouter_membre, name='ajouter_membre'),
    path('<int:projet_id>/retirer-membre/<int:user_id>/', views.retirer_membre, name='retirer_membre'),
]