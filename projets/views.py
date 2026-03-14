# projets/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Projet
from taches.models import Tache

User = get_user_model()


@login_required
def liste_projets(request):
    """Affiche la liste des projets de l'utilisateur"""
    projets_crees = Projet.objects.filter(createur=request.user)
    projets_membre = Projet.objects.filter(membres=request.user).exclude(createur=request.user)

    # Ajouter des statistiques pour chaque projet
    for projet in projets_crees:
        total_taches = projet.taches.count()
        taches_terminees = projet.taches.filter(statut='termine').count()
        projet.progression = (taches_terminees / total_taches * 100) if total_taches > 0 else 0
        projet.total_taches = total_taches

    for projet in projets_membre:
        total_taches = projet.taches.count()
        taches_terminees = projet.taches.filter(statut='termine').count()
        projet.progression = (taches_terminees / total_taches * 100) if total_taches > 0 else 0
        projet.total_taches = total_taches

    context = {
        'projets_crees': projets_crees,
        'projets_membre': projets_membre,
    }
    return render(request, 'projets/liste_projets.html', context)


@login_required
def creer_projet(request):
    """Crée un nouveau projet"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')

        if titre:
            projet = Projet.objects.create(
                titre=titre,
                description=description,
                createur=request.user
            )
            projet.membres.add(request.user)  # Le créateur est automatiquement membre
            messages.success(request, f'Projet "{titre}" créé avec succès !')
            return redirect('liste_projets')
        else:
            messages.error(request, 'Le titre est obligatoire')

    return render(request, 'projets/creer_projet.html')


@login_required
def detail_projet(request, projet_id):
    """Affiche les détails d'un projet"""
    projet = get_object_or_404(Projet, id=projet_id)

    # Vérifier que l'utilisateur a accès au projet
    if request.user not in projet.membres.all() and request.user != projet.createur:
        messages.error(request, "Vous n'avez pas accès à ce projet")
        return redirect('liste_projets')

    taches = projet.taches.all()

    # Statistiques pour le projet
    total_taches = taches.count()
    taches_terminees = taches.filter(statut='termine').count()
    progression = (taches_terminees / total_taches * 100) if total_taches > 0 else 0

    from django.utils import timezone
    today = timezone.now().date()

    context = {
        'projet': projet,
        'taches': taches,
        'total_taches': total_taches,
        'taches_terminees': taches_terminees,
        'progression': progression,
        'today': today,
    }
    return render(request, 'projets/detail_projet.html', context)


@login_required
def modifier_projet(request, projet_id):
    """Modifie un projet existant"""
    projet = get_object_or_404(Projet, id=projet_id)

    # Vérifier que l'utilisateur est le créateur
    if request.user != projet.createur:
        messages.error(request, "Seul le créateur peut modifier ce projet")
        return redirect('detail_projet', projet_id=projet.id)

    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')

        if titre:
            projet.titre = titre
            projet.description = description
            projet.save()
            messages.success(request, 'Projet modifié avec succès')
            return redirect('detail_projet', projet_id=projet.id)
        else:
            messages.error(request, 'Le titre est obligatoire')

    return render(request, 'projets/modifier_projet.html', {'projet': projet})


@login_required
def supprimer_projet(request, projet_id):
    """Supprime un projet"""
    projet = get_object_or_404(Projet, id=projet_id)

    # Vérifier que l'utilisateur est le créateur
    if request.user != projet.createur:
        messages.error(request, "Seul le créateur peut supprimer ce projet")
        return redirect('detail_projet', projet_id=projet.id)

    if request.method == 'POST':
        titre = projet.titre
        # Supprimer d'abord toutes les tâches associées
        projet.taches.all().delete()
        # Puis supprimer le projet
        projet.delete()
        messages.success(request, f'Projet "{titre}" supprimé avec succès')
        return redirect('liste_projets')

    # Compter le nombre de tâches pour l'afficher dans la confirmation
    nb_taches = projet.taches.count()
    return render(request, 'projets/supprimer_projet.html', {
        'projet': projet,
        'nb_taches': nb_taches
    })


@login_required
def ajouter_membre(request, projet_id):
    """Ajoute un membre au projet"""
    projet = get_object_or_404(Projet, id=projet_id)

    if request.user != projet.createur:
        messages.error(request, "Seul le créateur peut ajouter des membres")
        return redirect('detail_projet', projet_id=projet.id)

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)

            # Vérifier si l'utilisateur est déjà membre
            if user in projet.membres.all():
                messages.warning(request, f'{username} est déjà membre du projet')
            else:
                projet.membres.add(user)
                messages.success(request, f'{username} a été ajouté au projet')

        except User.DoesNotExist:
            messages.error(request, f'Utilisateur "{username}" introuvable')

    return redirect('detail_projet', projet_id=projet.id)


@login_required
def retirer_membre(request, projet_id, user_id):
    """Retire un membre du projet"""
    projet = get_object_or_404(Projet, id=projet_id)

    if request.user != projet.createur:
        messages.error(request, "Seul le créateur peut retirer des membres")
        return redirect('detail_projet', projet_id=projet.id)

    user = get_object_or_404(User, id=user_id)

    # Ne pas pouvoir retirer le créateur
    if user == projet.createur:
        messages.error(request, "Vous ne pouvez pas retirer le créateur du projet")
    else:
        projet.membres.remove(user)
        messages.success(request, f'{user.username} a été retiré du projet')

    return redirect('detail_projet', projet_id=projet.id)