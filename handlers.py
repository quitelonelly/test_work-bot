from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from api_weather.weather import get_temperature
from kb_bot import kb_inline, kb_reg
from state.register import RegisterState
from database.core import insert_user, get_users, handle_message

# Handlers
async def cmd_start(message: types.Message):
    await message.answer(f"Добро пожаловать в наш бот!", reply_markup=kb_reg)

async def cmd_help(message: types.Message):
    await message.answer(f"Доступные команды: <b>/start /help /echo /photo</b>", parse_mode="HTML")

async def cmd_echo(message: types.Message):
    text_to_echo = message.text[len("/echo "):].strip()
    if text_to_echo:
        await message.answer(text_to_echo)
    else:
        await message.answer("Пожалуйста, укажите текст после команды <b>/echo</b>, чтобы бот мог его повторить.", parse_mode="HTML")

async def cmd_choice(message: types.Message):
    await message.answer(f"Выбирайте!", reply_markup=kb_inline)

async def process_choice1(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Вы выбрали\n<b>Выбор1</b>", parse_mode="HTML")
    await callback_query.answer()

async def process_choice2(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Вы выбрали\n<b>Выбор2</b>", parse_mode="HTML")
    await callback_query.answer()

async def handler_register(message: types.Message, state: FSMContext):
    await message.answer("⭐️Давайте начнем регистрацию!⭐️\nПодскажите, как к вам обращаться?")
    await state.set_state(RegisterState.regName)

async def register_name(message: types.Message, state: FSMContext):
    await message.answer(f"☺️ Приятно познакомиться {message.text}!\nТеперь укажите ваш возраст!")
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regAge)

async def register_age(message: types.Message, state: FSMContext):
    await state.update_data(regage=message.text)
    reg_data = await state.get_data()
    reg_name = reg_data.get("regname")
    reg_age = reg_data.get("regage")
    reg_tgid = message.from_user.id

    result = insert_user(reg_name, reg_age, reg_tgid)
    await message.answer(result, parse_mode="HTML")
    await state.clear()

async def cmd_photo(message: types.Message):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию после команды <b>/photo</b>, чтобы бот мог обработать изображение.", parse_mode="HTML")
        return

    photo = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)
    downloaded_file = await message.bot.download_file(file_info.file_path)

    with open("downloaded_image.jpg", "wb") as f:
        f.write(downloaded_file.read())

    from PIL import Image
    image = Image.open("downloaded_image.jpg")
    width, height = image.size

    await message.reply(f"Размер изображения: <b>{width}x{height}</b>", parse_mode="HTML")

async def cmd_users(message: types.Message):
    result = get_users()
    await message.answer(result, parse_mode="html")

async def cmd_weather(message: types.Message):
    city_name = message.text[len("/weather "):].strip()
    if not city_name:
        await message.reply("Пожалуйста, укажите название города после команды /weather.")
        return

    temperature_info = get_temperature(city_name)
    await message.reply(temperature_info, parse_mode="HTML")
    
async def cmd_message_handler(message: types.Message):
    await handle_message(message)



def reg_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=["start"]))
    dp.message.register(cmd_help, Command(commands=["help"]))
    dp.message.register(cmd_echo, Command(commands=["echo"]))
    dp.message.register(cmd_choice, Command(commands=["choice"]))
    dp.message.register(cmd_users, Command(commands=["users"]))
    dp.message.register(cmd_photo, Command(commands=["photo"]))
    dp.message.register(cmd_weather, Command(commands=['weather']))
    
    dp.message.register(handler_register, F.text == "Зарегистрироваться")
    dp.message.register(register_name, RegisterState.regName)
    dp.message.register(register_age, RegisterState.regAge)
    
    dp.callback_query.register(process_choice1, lambda c: c.data == 'choice1')  
    dp.callback_query.register(process_choice2, lambda c: c.data == 'choice2')

    dp.message.register(cmd_message_handler)
