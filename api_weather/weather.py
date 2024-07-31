import logging
import requests

API_KEY = 'db8cb5339666eb1847b967c2ef7d936e'
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Создаем логгер
logging.basicConfig(level=logging.INFO)

# Функция для получения температуры по названию города
def get_temperature(city: str) -> str:
    try:
        # Выполняем запрос к API
        response = requests.get(WEATHER_API_URL, params={
            'q': city,
            'appid': API_KEY,
            'units': 'metric',  # Используем метрические единицы (Цельсий)
            'lang': 'ru'  # Используем русский язык для описания
        })
        
        # Проверяем статус ответа
        if response.status_code != 200:
            # Проверяем код ошибки
            if response.status_code == 401:
                error_message = "Ошибка авторизации: проверьте ваш API ключ."
            else:
                error_message = f"Ошибка: {response.json().get('message', 'Не удалось получить данные о погоде.')}"
            
            # Логируем ошибку в консоль
            logging.error(f"Ошибка при запросе к API: {error_message}")
            
            # Возвращаем сообщение для пользователя
            return "Произошла ошибка при получении данных о погоде."

        # Извлекаем данные из ответа
        data = response.json()
        
        # Извлекаем температуру из ответа
        temperature = data['main']['temp']
        
        # Формируем строку с температурой
        temperature_info = f"Температура в городе {city}: {temperature}°C"
        return temperature_info

    except Exception as e:
        # Логируем исключение в консоль
        logging.error(f"Ошибка при получении температуры: {e}")
        return "Произошла ошибка при получении данных о погоде."
