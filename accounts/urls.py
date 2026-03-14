# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('profil/', views.profil, name='profil'),
    path('', views.accueil, name='accueil'),

    # Nouvelles pages
    path('apropos/', views.apropos, name='apropos'),
    path('contact/', views.contact, name='contact'),
    path('aide/', views.aide, name='aide'),
]