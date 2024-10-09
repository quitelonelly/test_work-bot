from aiogram import types
from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from API.request import get_weather
from database.core import insert_request

# Command handler for /start
async def cmd_start(message: types.Message):
    response = f"🤩Приветствую, {message.from_user.full_name}!"
    await message.answer(response)
    await insert_request(message.from_user.id, "/start", response)

# Command handler for /weather
async def cmd_weather(message: types.Message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        response = "Пожалуйста, укажите город после команды /weather. Пример: /weather Москва"
        await message.answer(response)
        await insert_request(message.from_user.id, "/weather", response)
        return

    city_name = command_parts[1].strip()
    weather_info = get_weather(city_name)
    await message.answer(weather_info)
    await insert_request(message.from_user.id, f"/weather {city_name}", weather_info)

# Function to register handlers
def reg_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=["start"]))
    dp.message.register(cmd_weather, Command(commands=["weather"]))