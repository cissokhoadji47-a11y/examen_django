# taches/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q, F
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import Tache
from projets.models import Projet
from .utils import calculer_statistiques_professeur, calculer_primes_tous_professeurs

User = get_user_model()


@login_required
def creer_tache(request, projet_id):
    """Crée une nouvelle tâche dans un projet"""
    projet = get_object_or_404(Projet, id=projet_id)

    # Vérifier que l'utilisateur est le créateur du projet
    if request.user != projet.createur:
        messages.error(request, "Seul le créateur du projet peut ajouter des tâches")
        return redirect('detail_projet', projet_id=projet.id)

    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        assigne_a_id = request.POST.get('assigne_a')
        date_limite = request.POST.get('date_limite')

        if titre and date_limite:
            tache = Tache.objects.create(
                titre=titre,
                description=description,
                projet=projet,
                date_limite=date_limite,
                statut='a_faire'
            )

            if assigne_a_id:
                try:
                    user = User.objects.get(id=assigne_a_id)
                    tache.assigne_a = user
                    tache.save()
                except User.DoesNotExist:
                    pass

            messages.success(request, f'Tâche "{titre}" créée avec succès')
            return redirect('detail_projet', projet_id=projet.id)
        else:
            messages.error(request, 'Le titre et la date limite sont obligatoires')

    membres = projet.membres.all()
    return render(request, 'taches/creer_tache.html', {
        'projet': projet,
        'membres': membres
    })


@login_required
def modifier_tache(request, tache_id):
    """Modifie une tâche existante"""
    tache = get_object_or_404(Tache, id=tache_id)
    projet = tache.projet

    if request.user != projet.createur and request.user != tache.assigne_a:
        messages.error(request, "Vous n'avez pas la permission de modifier cette tâche")
        return redirect('detail_projet', projet_id=projet.id)

    if request.method == 'POST':
        tache.titre = request.POST.get('titre', tache.titre)
        tache.description = request.POST.get('description', tache.description)
        tache.date_limite = request.POST.get('date_limite', tache.date_limite)

        assigne_a_id = request.POST.get('assigne_a')
        if assigne_a_id:
            try:
                tache.assigne_a = User.objects.get(id=assigne_a_id)
            except User.DoesNotExist:
                pass

        tache.save()
        messages.success(request, 'Tâche modifiée avec succès')
        return redirect('detail_projet', projet_id=projet.id)

    membres = projet.membres.all()
    return render(request, 'taches/modifier_tache.html', {
        'tache': tache,
        'projet': projet,
        'membres': membres
    })


@login_required
def supprimer_tache(request, tache_id):
    """Supprime une tâche"""
    tache = get_object_or_404(Tache, id=tache_id)
    projet = tache.projet

    if request.user != projet.createur:
        messages.error(request, "Seul le créateur du projet peut supprimer des tâches")
        return redirect('detail_projet', projet_id=projet.id)

    if request.method == 'POST':
        titre = tache.titre
        tache.delete()
        messages.success(request, f'Tâche "{titre}" supprimée avec succès')
        return redirect('detail_projet', projet_id=projet.id)

    return render(request, 'taches/supprimer_tache.html', {'tache': tache})


@login_required
def changer_statut(request, tache_id):
    """Change le statut d'une tâche"""
    tache = get_object_or_404(Tache, id=tache_id)
    projet = tache.projet

    if request.user != projet.createur and request.user != tache.assigne_a:
        messages.error(request, "Vous n'avez pas la permission de modifier cette tâche")
        return redirect('detail_projet', projet_id=projet.id)

    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')

        if nouveau_statut in ['a_faire', 'en_cours', 'termine']:
            tache.statut = nouveau_statut

            if nouveau_statut == 'termine' and tache.statut != 'termine':
                from django.utils import timezone
                tache.date_fin_reelle = timezone.now().date()

            tache.save()
            messages.success(request, f'Statut de la tâche mis à jour')

    return redirect('detail_projet', projet_id=projet.id)


# ===== NOUVELLES VUES POUR LES STATISTIQUES =====

@login_required
def statistiques_personnelles(request):
    """Vue des statistiques personnelles pour un professeur"""
    # Vérifier que l'utilisateur est un professeur
    if request.user.role != 'professeur':
        messages.error(request, "Cette page est réservée aux professeurs")
        return redirect('accueil')

    annee = request.GET.get('annee', datetime.now().year)
    trimestre = request.GET.get('trimestre')

    try:
        annee = int(annee)
        trimestre = int(trimestre) if trimestre else None
    except ValueError:
        annee = datetime.now().year
        trimestre = None

    stats = calculer_statistiques_professeur(request.user, annee, trimestre)

    # Récupérer les tâches pour les détails
    taches = Tache.objects.filter(
        assigne_a=request.user,
        date_limite__year=annee
    )

    if trimestre:
        if trimestre == 1:
            taches = taches.filter(date_limite__month__in=[1, 2, 3])
        elif trimestre == 2:
            taches = taches.filter(date_limite__month__in=[4, 5, 6])
        elif trimestre == 3:
            taches = taches.filter(date_limite__month__in=[7, 8, 9])
        elif trimestre == 4:
            taches = taches.filter(date_limite__month__in=[10, 11, 12])

    context = {
        'stats': stats,
        'taches': taches,
        'annee': annee,
        'trimestre': trimestre,
        'annees': range(2024, datetime.now().year + 2)
    }
    return render(request, 'taches/statistiques.html', context)


@login_required
@staff_member_required
def classement_primes(request):
    """Classement des primes pour l'administration"""
    # Vérifier que l'utilisateur est un professeur
    if request.user.role != 'professeur':
        messages.error(request, "Cette page est réservée aux professeurs")
        return redirect('accueil')

    annee = request.GET.get('annee', datetime.now().year)

    try:
        annee = int(annee)
    except ValueError:
        annee = datetime.now().year

    resultats = calculer_primes_tous_professeurs(annee)

    context = {
        'resultats': resultats,
        'annee': annee,
        'annees': range(2024, datetime.now().year + 2)
    }
    return render(request, 'taches/classement_primes.html', context)