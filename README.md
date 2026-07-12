# TaskFlow - Gestionnaire de tâches personnelles

## Description

TaskFlow est une application web développée avec Django permettant à un utilisateur de créer, organiser et suivre ses tâches quotidiennes.

## Fonctionnalités

- Page d'accueil et page à propos
- Liste des tâches avec statut et priorité
- Création, modification et suppression d'une tâche
- Gestion des statuts et priorités
- Inscription, connexion et déconnexion des utilisateurs
- Administration via Django Admin
- Tests automatisés

## Installation

### 1. Cloner le dépôt

git clone https://github.com/manalrakik/django-taskflow-groupe-01.git
cd django-taskflow-groupe-01

### 2. Créer et activer l'environnement virtuel (Windows)

python -m venv .venv
.venv\Scripts\Activate.ps1

### 3. Installer les dépendances

pip install -r requirements.txt

### 4. Appliquer les migrations

python manage.py migrate

### 5. Créer un superutilisateur

python manage.py createsuperuser

### 6. Lancer le serveur

python manage.py runserver

L'application est accessible à : http://127.0.0.1:8000/
L'admin est accessible à : http://127.0.0.1:8000/admin/

## Lancer les tests

python manage.py test

## Auteur

Manal Rakik - [Ta filière] - Année universitaire 2025-2026

## Lien du dépôt GitHub

https://github.com/manalrakik/django-taskflow-groupe-01