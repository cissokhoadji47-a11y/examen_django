# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from projets.models import Projet
from taches.models import Tache
from django.db.models import Q
from datetime import date


def accueil(request):
    """Page d'accueil"""
    if request.user.is_authenticated:
        return redirect('liste_projets')
    return render(request, 'accounts/accueil.html')


def inscription(request):
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role', 'etudiant')

        # Vérifications
        if password != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return render(request, 'accounts/inscription.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur existe déjà')
            return render(request, 'accounts/inscription.html')

        # Création de l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        login(request, user)
        messages.success(request, f'Bienvenue {username} !')
        return redirect('liste_projets')

    return render(request, 'accounts/inscription.html')


def connexion(request):
    """Connexion utilisateur"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bon retour {username} !')
            return redirect('liste_projets')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')

    return render(request, 'accounts/connexion.html')


@login_required
def deconnexion(request):
    """Déconnexion"""
    logout(request)
    messages.success(request, 'À bientôt !')
    return redirect('accueil')


@login_required
def profil(request):
    """Gestion du profil utilisateur"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.bio = request.POST.get('bio', '')

        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        messages.success(request, 'Profil mis à jour avec succès')

        # Changement de mot de passe
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if old_password and new_password:
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Mot de passe changé avec succès')
            else:
                messages.error(request, 'Ancien mot de passe incorrect')

        return redirect('profil')

    return render(request, 'accounts/profil.html')

# accounts/views.py (ajoute ces fonctions à la fin)

def apropos(request):
    """Page À propos"""
    return render(request, 'accounts/apropos.html')

def contact(request):
    """Page Contact"""
    return render(request, 'accounts/contact.html')

def aide(request):
    """Page Aide"""
    return render(request, 'accounts/aide.html')