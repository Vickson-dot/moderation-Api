DOCUMENTATION TECHNIQUE : API DE MODERATION AUTOMATISEE
1. Présentation du Projet
2. Cette API fournit un système complet de gestion de contenu avec analyse de toxicité en temps réel. Elle intègre le modèle de Deep Learning Detoxify pour automatiser la détection de contenus inappropriés et permettre une intervention humaine ciblée.
3. 2. Architecture Technique
4. Framework : Django 5.x / Django REST Framework
Moteur d'IA : Detoxify (basé sur l'architecture Transformer)
5. Authentification : Token-based Authentication
6. Base de données : SQLite (environnement de développement)

3. Installation et Configuration
4. Prérequis
5. Python 3.10+
6. Pip (gestionnaire de paquets)
Procédure d'installation
7.Environnement virtuel :
7. python -m venv venv
venv\Scripts\activate
8. 
8. Installation des dépendances :
9. pip install django djangorestframework django-cors-headers detoxify torch
10. Initialisation de la base de données :
11. python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
12.Une fois le compte super-utilisateur (superuser) créé et la connexion établie sur /admin/ :

Se rendre dans la section Tokens.

Cliquer sur le bouton Add Token.
Sélectionner l'utilisateur correspondant et enregistrer. Le jeton s'affichera alors à l'écran.
Il sélectionne son utilisateur et enregistre. Le token s'affichera à l'écran

12. 4. "Monsieur, pour tester l'API, j'ai exclu la base de données locale par sécurité. Il vous suffira de lancer python manage.py migrate puis python manage.py createsuperuser pour accéder à l'interface de modération et aux endpoints protégés."
13. 
14. Spécifications du Système de Modération
13. L'analyse est déclenchée automatiquement via un signal Django lors de la sauvegarde d'un objet Message
14. Paramètre	Seuil / Valeur	Action
Seuil de Toxicité	> 0.7	Statut : "flagged" (quarantaine)
Seuil de Signalement	>= 3 reports	Statut : "flagged" (automatique)
Catégories analysées	Toxicity, Insult, Threat, Obscene	Enregistrement dans ModerationResult

5. Guide des Endpoints API
6. A. Gestion des Message
7. POST /api/messages/ : Soumission d'un nouveau contenu.
8. POST /api/messages/{id}/report/ : Signalement d'un message par un utilisateur

B. Interface de Modération (Admin uniquement)
GET /api/moderation/pending/ : Liste des messages en attente de révision (statuts pending ou flagged).
POST /api/moderation/{id}/approve/ : Validation manuelle d'un message.
POST /api/moderation/{id}/reject/ : Rejet définitif et masquage du contenu.

C. Analytique
GET /api/moderation/stats/ : Récupération des indicateurs de performance (KPI) de la plateforme.