# Prévisions Météorologiques avec OpenWeatherMap

Ce projet Python utilise [l'API OpenWeatherMap](https://openweathermap.org/api) pour récupérer et traiter les prévisions météorologiques pour une ville donnée. Les données sont sauvegardées au format JSON dans un dossier `forecasts`.

## Table des matières

- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation](#utilisation)

## Technologies utilisées

- Python 3.x
- [Requests](https://pypi.org/project/requests/) - Pour effectuer des requêtes HTTP
- [Click](https://pypi.org/project/click/) - Pour gérer les options en ligne de commande
- [Loguru](https://pypi.org/project/loguru/) - Pour la gestion des logs
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Pour charger les variables d'environnement
- [JSON](https://docs.python.org/3/library/json.html) - Pour manipuler les données au format JSON

## Installation

1. **Cloner le dépôt** 
2. **Créer un environnement virtuel** :
   ```bash
   cd nom-du-projet
   python -m venv venv
3. **Activer l'environnement virtuel** :
    - Pour Windows :
    ```bash
    .\venv\Scripts\activate
    ```
    - Pour macOS/Linux :
    ```bash
    source venv/bin/activate
4. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
5. **Configurer la clé API** :
Créez un fichier .env à la racine du projet et ajoutez votre clé API OpenWeatherMap
   ```bash
   API_KEY=your_api_key
   ```

## Utilisation
Pour exécuter le script et obtenir les prévisions météorologiques, utilisez la commande suivante (ci-dessous, un exemple avec Paris) :
```bash
python tp-weather.py --city "Paris" --country "FR"
```
Vous pouvez également lancer le programme sans argument et rentrer directement les informations dans le prompt affiché par le script :
```bash
python tp-weather.py
```
Les données de prévision seront ensuite sauvegardées dans un fichier JSON dans le sous-dossier `forecasts`