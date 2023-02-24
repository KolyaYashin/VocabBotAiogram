from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

button_yes = KeyboardButton(text='Да ✅')
button_no = KeyboardButton(text='Нет ❌')

keyboard_settings = ReplyKeyboardMarkup(keyboard=[[button_yes,button_no]], resize_keyboard=True)