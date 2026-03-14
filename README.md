<<<<<<< HEAD
Application de Gestion des Tâches Collaboratives
Description

Cette application web permet de gérer des projets et des tâches dans un environnement collaboratif destiné aux étudiants et aux professeurs.

Les utilisateurs peuvent :

créer des projets

ajouter des tâches

assigner des tâches à d'autres utilisateurs

suivre l'avancement des tâches

L'application est développée avec Django et expose également une API REST pour permettre l'utilisation avec un frontend moderne.

Technologies utilisées
Backend

Python

Django

Django REST Framework

Frontend

HTML

CSS

JavaScript

Django Templates

Base de données

SQLite

Installation du projet
1. Cloner le projet

git clone https://github.com/ton-utilisateur/ton-projet.git

cd ton-projet

2. Créer un environnement virtuel

python -m venv env

Activer l'environnement :

Windows
env\Scripts\activate

Linux / Mac
source env/bin/activate

3. Installer les dépendances

pip install -r requirements.txt

4. Appliquer les migrations

python manage.py migrate

5. Créer un super utilisateur

python manage.py createsuperuser

6. Lancer le serveur

python manage.py runserver

L'application sera accessible à l'adresse :

http://127.0.0.1:8000

Fonctionnalités principales

Authentification des utilisateurs

Gestion des profils

Création et gestion des projets

Création et gestion des tâches

Attribution des tâches aux utilisateurs

