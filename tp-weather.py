import requests
import json
import sys
import click
import os
from loguru import logger
from datetime import datetime
from dotenv import load_dotenv


class OpenWeatherMap:
    def __init__(self, city, country, url, api_key):
        self.city = city
        self.country = country
        self.api_key = api_key
        self.url = url
        self.data = None
        self.processedData = {}
        logger.info(f"Initialization of the process to get weather data from {self.city}, {self.country}")

    # Convertit les valeurs en Kelvin en degré Celsius 
    def kelvinToCelsius(self, kelvin):
        return kelvin - 273.15

    # Envoie une requête api et convertit le résultat en json
    def get_data(self):
        try:
            response = requests.get(f"{self.url}{self.city},{self.country}&appid={self.api_key}")
            response.raise_for_status()
            self.data = json.loads(response.text)
            logger.success(f"Request to get weather forecast data from {self.city}, {self.country} succeeded !!!")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Request to get weather forecast data from {self.city}, {self.country} failed... : \nError {e.response.status_code} : {e.response.reason}")
            sys.exit(1)

    # Convertit le résultat brut obtenu de la requête en le format attendu
    def convert_data(self):
        self.processedData["forecast_location"] = f"{self.data["city"]["name"]}({self.data["city"]["country"]})"
        self.processedData["forecast_min_temp"] = 100
        self.processedData["forecast_max_temp"] = -100
        self.processedData["forecast_details"] = []
        forecast_details = {}

        # On traite unitairement chaque donnée reçue
        for forecast_unit in self.data["list"]:
            # On extrait la date du jour et on en fait un objet Datetime plus facilement manipulable
            date = datetime.strptime(forecast_unit["dt_txt"], '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
            temperature = round(self.kelvinToCelsius(forecast_unit["main"]["temp"]), 1)

            # Si aucune donnée pour cette journée n'a encore été traitée, on initialise un dictionnaire vide pour cette date
            # Pour chaque date on stocke le nombre et la somme des échantillons de température afin d'en faire la moyenne plus tard
            if date not in forecast_details:
                forecast_details[date] = {"date": date, "measure_count": 0, "temperature_sum": 0}

            forecast_details[date]["measure_count"] += 1
            forecast_details[date]["temperature_sum"] += temperature

            # On met à jour la valeur de température minimale
            if temperature < self.processedData["forecast_min_temp"]:
                self.processedData["forecast_min_temp"] = temperature

            # On met à jour la valeur de température maximale
            if temperature > self.processedData["forecast_max_temp"]:
                self.processedData["forecast_max_temp"] = temperature

        # On traite les données organisées par jour
        for detail in forecast_details:
            self.processedData["forecast_details"].append({
                    "date": forecast_details[detail]["date"],
                    "temp": round(forecast_details[detail]["temperature_sum"]/forecast_details[detail]["measure_count"], 1),
                    "measure_count": forecast_details[detail]["measure_count"]
                }
            )

    # Sauvegarde le résultat précédemment obtenu dans un fichier au format JSON
    def save_to_file(self):
        # On crée le dossier pour stocker les forecasts s'il n'existe pas
        directory = "forecasts"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"forecasts/{self.city}-{self.country}_forecast.json"
        logger.info(f"Starting to write the weather data from {self.city}({self.country}) in {filename}")
        try:
            with open(filename, "w") as file:
                json.dump(self.processedData, file, indent=3)
            logger.success(f"Forecast for {self.city}({self.country}) was successfully written in {filename}")
        except OSError as e:
            logger.error(f"Could not write in file {filename}\nError {e.errno} : {e.strerror}")
            sys.exit(2)


# Callback appelé pour valider l'input country code
def validate_country_code(ctx, param, value):
    if len(value) != 2 or not value.isalpha():
        raise click.BadParameter("The country code should be a 2 letters code")
    return value.upper()


# Callback appelé pour valider l'input country code
def validate_city(ctx, param, value):
    if not all(c.isalpha() or c.isspace() for c in value):
        raise click.BadParameter("The city name should only contain letters or spaces")
    return value


# Ici on permet à l'utilisateur de rentrer des inputs au démarrage du script
@click.command()
@click.option('--city', prompt="City", callback=validate_city, help="Enter the city for which you want the forecast")
@click.option('--country', prompt="Country code", callback=validate_country_code, help="Enter the country code for the city for which you want the forecast (ex : US, FR, etc...)")
def main(city, country):
    url = "https://api.openweathermap.org/data/2.5/forecast?q="
    # On charge les variables d'environnement présentes dans le fichier .env
    load_dotenv()
    # On accède à la variable d'environnement contenant la clé API
    api_key = os.getenv("API_KEY")
    weather = OpenWeatherMap(city, country, url, api_key)
    weather.get_data()
    weather.convert_data()
    weather.save_to_file()


if __name__ == "__main__":
    main()
