from sqlalchemy import insert, select
from database.db import sync_engine
from database.models import metadata_obj, users_table

from aiogram.fsm.context import FSMContext

from datetime import datetime, timedelta
import asyncio
from aiogram import Bot, types


def create_tables():
    metadata_obj.create_all(sync_engine)
    
# Добавление пользователя в бд
def insert_user(name, age, tgid):
    # Проверяем, существует ли пользователь с таким телефоном
    if check_user(name):
        return f"Пользователь с именем <b>{name}</b> уже существует!"
    
    with sync_engine.connect() as conn:
        # Если пользователь не найден, добавляем новые данные
        stmt = insert(users_table).values(
            [
                {"username": name, "userage": age, "usertgid": tgid}
            ]
        )
        conn.execute(stmt)
        conn.commit()
        
        return f"☺️ Приятно познакомиться <b>{name}</b>!\n\nВаш возраст: <b>{age}</b>"
    
# Функция проверки, есть ли пользователь в БД
def check_user(name):
    with sync_engine.connect() as conn:
        stmt = select(users_table).where(users_table.c.username == name)
        result = conn.execute(stmt).fetchone()
        
        if result:
            return True
        else:
            return False
        
# Функция возвращает список пользователей
def get_users():
    with sync_engine.connect() as conn:
        # Получим всех юзеров из БД
        stmt = select(users_table)
        result = conn.execute(stmt).fetchall()
        
        # Создадим список для извлечение всех пользователей
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
  
# Функция возвращает список с tgid пользователей  
def get_all_tgids():
    with sync_engine.connect() as conn:
        stmt = select(users_table.c.usertgid)
        result = conn.execute(stmt).fetchall()
        
        # Извлекаем все tgid в виде списка
        tgids = [row[3] for row in result]
        return tgids
 
import os
from dotenv import load_dotenv 
   
# Загрузка переменного окружения
load_dotenv()

# Получение токена из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)

pending_reminders = {}

async def send_daily_reminder(tgid: int, name: str):
    try:
        # Определяем время отправки сообщения
        now = datetime.now()
        next_reminder_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now > next_reminder_time:
            next_reminder_time += timedelta(days=1)

        delay = (next_reminder_time - now).total_seconds()
        await asyncio.sleep(delay)

        # Отправляем сообщение
        reminder_message = await bot.send_message(
            tgid,
            f"Привет, <b>{name}</b>! 🌟\n\nКак ты сегодня?",
            parse_mode="HTML"
        )

        # Сохраним сообщение-напоминание и время его отправки
        pending_reminders[tgid] = {
            "message_id": reminder_message.message_id,
            "sent_at": datetime.now()
        }

        # Ждем 15 минут
        await asyncio.sleep(900)  

        if tgid in pending_reminders:

            await bot.send_message(tgid, "Вы забыли ответить")
            del pending_reminders[tgid] 

    except Exception as e:
        print(f"Ошибка при отправке ежедневного напоминания: {e}")
        
async def send_daily_reminders():
    while True:
        users = select_users()
        for user in users:
            name = user["username"]
            tgid = user["usertgid"]
            # Отправляем напоминание каждому пользователю
            await send_daily_reminder(tgid, name)
        
        # Пауза между напоминаниями
        await asyncio.sleep(24 * 60 * 60)
        
async def on_message_received(message: types.Message, state: FSMContext):
    tgid = message.from_user.id
    
    if tgid in pending_reminders:
        await bot.send_message(tgid, "Спасибо за ваш ответ!")
        del pending_reminders[tgid]