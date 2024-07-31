from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import asyncio
import os

from handlers import reg_handlers
from database.core import create_tables, send_daily_reminders

# Загрузка переменного окружения
load_dotenv()

# Получение токена из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Вызываем функцию для создания таблиц
create_tables()

reg_handlers(dp)

# Запуск процесса поллинга новых апдейтов
async def main():
    asyncio.create_task(send_daily_reminders())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())