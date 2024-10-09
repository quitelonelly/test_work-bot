import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_weather(city_name):
    # Формирование URL запроса
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=ru"

    try:
        # Выполнение запроса к API
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверка на наличие ошибок HTTP
        data = response.json()

        # Извлечение необходимых данных о погоде
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Формирование ответа
        weather_info = (
            f"Город: {city_name}\n"
            f"Температура: {temperature} °C\n"
            f"Ощущаемая температура: {feels_like} °C\n"
            f"Описание погоды: {weather_description}\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
        return weather_info

    except requests.exceptions.RequestException as e:
        return f"Ошибка при выполнении запроса"
    
