import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from handlers import reg_handlers
from database.core import create_tables, start_scheduler

# Load environment variables
load_dotenv()

# Get the token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Create bot and dispatcher instances
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Create tables in the database
create_tables()


async def main():
    reg_handlers(dp)
    # Start polling new updates
    start_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
