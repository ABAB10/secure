# AuthSecure

Ce projet est une application Django sécurisée pour la gestion des utilisateurs, avec audit des connexions et fonctionnalités de sécurité avancées.

## Prérequis

- Python 3.10 ou supérieur (recommandé)
- pip (gestionnaire de paquets Python)
- Virtualenv (optionnel mais recommandé)

## Installation

### 1. Cloner le dépôt

```bash
git clone <lien-de-mon-depot-git>
cd authsecure
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv

# Sur Windows: 
venv\Scripts\activate
# Sur Mac:
source venv/bin/activate  
```

### 3. Installer les dépendances nécessaires

```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient :

- Django==5.1.7
- Pillow==10.3.0
- python-dotenv==1.0.1
- argon2-cffi==23.1.0

Si vous avez besoin de l’installer manuellement :

```bash
pip install Django==5.1.7 Pillow==10.3.0 python-dotenv==1.0.1 argon2-cffi==23.1.0
```

### 4. Configuration de l'environnement

Créez un fichier `.env` à la racine du projet et ajoutez-y vos variables d’environnement (exemple : clé secrète Django).

Exemple de contenu :

```
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

Adaptez selon votre configuration.

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Créer un superuser (compte admin)

```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur de développement

```bash
python manage.py runserver
```

Visitez [http://127.0.0.1:8000](http://127.0.0.1:8000) dans votre navigateur.

## Fonctionnalités principales

- Authentification, inscription, gestion du profil utilisateur
- Audit des actions utilisateurs (logs IP, User-Agent…)
- Mot de passe sécurisé (Argon2)
- Utilisation de variables d’environnement simples (`.env`)


## Licence

Ce projet est sous licence MIT