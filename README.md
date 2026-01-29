DOCUMENTATION TECHNIQUE : API DE MODERATION AUTOMATISEE
1. Présentation du Projet:
Cette API fournit un système complet de gestion de contenu avec analyse de toxicité en temps réel. Elle intègre le modèle de Deep Learning Detoxify pour automatiser la détection de contenus inappropriés et permettre une intervention humaine ciblée via un panel d'administration.

2. Architecture Technique
Framework : Django 5.x / Django REST Framework

Moteur d'IA : Detoxify (basé sur l'architecture Transformer)

Authentification : Token-based Authentication

Base de données : SQLite (environnement de développement)

3. Installation et Configuration
Note à l'attention du correcteur : Par mesure de sécurité et de propreté, la base de données locale a été exclue du dépôt. Veuillez suivre la procédure ci-dessous pour initialiser l'environnement.

Prérequis
Python 3.10+

Pip (gestionnaire de paquets)

Procédure d'installation
Environnement virtuel :
python -m venv venv
venv\Scripts\activate

Installation des dépendances :
pip install django djangorestframework django-cors-headers detoxify torch

Initialisation du système :
python manage.py makemigrations,
python manage.py migrate,
python manage.py createsuperuser.

Obtention du Token d'authentification : Une fois connecté sur /admin/ :

Se rendre dans la section Tokens.

Cliquer sur Add Token.

Sélectionner l'utilisateur et enregistrer. Le jeton s'affichera pour vos tests API

4. Spécifications du Système de Modération
L'analyse est déclenchée automatiquement via un signal Django lors de la sauvegarde d'un objet Message.
Paramètre	Seuil / Valeur	Action
Seuil de Toxicité	> 0.7	Statut : "flagged" (quarantaine)
Seuil de Signalement	>= 3 reports	Statut : "flagged" (automatique)
Catégories analysées	Toxicity, Insult, Threat, Obscene	Log dans ModerationResult
5. Guide des Endpoints API: 
  L'API est accessible directement via les URLs ci-dessous. La racine du serveur redirige automatiquement vers l'interface d'administration pour une gestion facilitée

A. Gestion des Messages
POST /api/messages/ : Soumission d'un nouveau contenu pour analyse IA.

POST /api/messages/{id}/report/ : Signalement d'un message par un utilisateur.

B. Interface de modération(Accès Administrateur)
Ces endpoints permettent de gérer les contenus mis en quarantaine. Ils sont visibles et testables via l'interface Django REST Framework si vous êtes connecté.

Liste des messages en attente

URL : GET /api/moderation/pending/

Contenu : Affiche les messages avec le statut pending ou flagged.

Approbation manuelle

URL : POST /api/moderation/{id}/approve/

Action : Valide le message et le rend public.

Rejet définitif

URL : POST /api/moderation/{id}/reject/

Action : Marque le contenu comme rejeté et le masque.

C. Analytique et Surveillance

Statistiques (KPI)

URL : GET /api/moderation/stats/

Description : Rapport en temps réel (Volume total, % de toxicité, volume de signalements)

6. Interface d'Administration

Les tables de données suivantes sont directement administrables via l'interface graphique /admin/ :

Messages : Consultation de tous les contenus.

Moderation Results : Détails des scores envoyés par l'IA Detoxify.

Reports : Historique des signalements utilisateurs.

Moderation Actions : Journal des décisions prises par les modérateurs.