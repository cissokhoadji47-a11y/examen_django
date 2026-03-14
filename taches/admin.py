from django.contrib import admin
from .models import Tache

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('titre', 'projet', 'assigne_a', 'statut', 'date_limite')
    list_filter = ('statut', 'date_limite', 'projet')
    search_fields = ('titre', 'description')
    date_hierarchy = 'date_limite'