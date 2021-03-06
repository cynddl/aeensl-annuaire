# Annuaire des anciens élèves de l'ENS de Lyon

Prototype d'annuaire pour l'Association des anciens élèves de l'ENS de Lyon (AEENSL). Il permet actuellement de créer et renouveler ses cotisations.

## Installation

Le projet est implémenté en Python, autour du framework django. Les dépendances suivantes sont requises :

- Python 3
- PostgreSQL

Pour générer un environnement de développement avec [venv](https://docs.python.org/3/library/venv.html):

```bash
    python -m venv anciens-venv

    # Activer l'environnement avec bash/zsh
    source anciens-venv /bin/activate

    pip install requirements.txt
````

Pour lancer le serveur :

    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py runserver
