import asyncio
from datetime import datetime, timedelta
from sqlalchemy import insert, select
from aiogram import Bot, types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import os

from .db import sync_engine
from .models import metadata_obj, users_table
from dotenv import load_dotenv

class UserStates(StatesGroup):
    waiting_for_response = State()

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()

pending_tasks = {}

def create_tables():
    metadata_obj.create_all(sync_engine)

def insert_user(name, age, tgid):
    if check_user(name):
        return f"Пользователь с именем <b>{name}</b> уже существует!"
    with sync_engine.connect() as conn:
        stmt = insert(users_table).values(
            [{"username": name, "userage": age, "usertgid": tgid}]
        )
        conn.execute(stmt)
        conn.commit()
        return f"☺️ Приятно познакомиться <b>{name}</b>!\n\nВаш возраст: <b>{age}</b>"

def check_user(name):
    with sync_engine.connect() as conn:
        stmt = select(users_table).where(users_table.c.username == name)
        result = conn.execute(stmt).fetchone()
        return result is not None

def get_users():
    with sync_engine.connect() as conn:
        stmt = select(users_table)
        result = conn.execute(stmt).fetchall()
        users_list = ""
        for row in result:
            user = f"ID: <b>{row[0]}</b>\nИмя: <b>{row[1]}</b>\nВозраст: <b>{row[2]}</b>\n\n"
            users_list += user
        return f"Вот список пользователей:\n\n{users_list}"

def select_users():
    with sync_engine.connect() as conn:
        stmt = select(users_table)
        result = conn.execute(stmt).fetchall()
        users_list = [{"id": row[0], "username": row[1], "userage": row[2], "usertgid": row[3]} for row in result]
        return users_list

pending_responses = {}

async def wait_for_response(chat_id, reply_message_id):
    # Add entry to pending_responses
    pending_responses[reply_message_id] = chat_id

    # Wait for 10 seconds
    await asyncio.sleep(10)

    # Check if response was received
    if reply_message_id in pending_responses:
        # If not received, send reminder
        await bot.send_message(chat_id, "Вы забыли ответить")
        # Remove the entry after reminder is sent
        del pending_responses[reply_message_id]


async def send_daily_message():
    users = select_users()
    for user in users:
        try:
            # Send message
            sent_message = await bot.send_message(user["usertgid"], "Привет! Как ты?")

            # Wait for response
            await wait_for_response(user["usertgid"], sent_message.message_id)

        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user['usertgid']}: {e}")
            
async def handle_message(message: types.Message):
    # Check if message is a reply to a message we are waiting for
    if message.reply_to_message and message.reply_to_message.message_id in pending_responses:
        # If so, remove the entry from pending_responses
        del pending_responses[message.reply_to_message.message_id]
        await message.answer("Спасибо за ответ!")

async def scheduler():
    while True:
        now = datetime.now()
        next_run = now.replace(hour=12, minute=1, second=0, microsecond=0)
        if now > next_run:
            next_run += timedelta(days=1)
        wait_time = (next_run - now).total_seconds()
        await asyncio.sleep(wait_time)
        await send_daily_message()

def start_scheduler():
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
