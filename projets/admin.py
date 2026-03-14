# projets/admin.py
from django.contrib import admin
from .models import Projet

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'createur', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('titre', 'description')
    filter_horizontal = ('membres',)