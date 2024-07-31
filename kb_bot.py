from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Инлайн клавиатура 
kb_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Выбор1', callback_data='choice1'),
         InlineKeyboardButton(text='Выбор2', callback_data='choice2')]
    ]
)

# Основная клавиатура
kb_reg = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Зарегистрироваться')]
    ],
    resize_keyboard=True
)