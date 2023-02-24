from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_yes = InlineKeyboardButton(text='Да ✅', callback_data='yes_pressed')
button_no = InlineKeyboardButton(text='Нет ❌', callback_data='no_pressed')



keyboard_settings = InlineKeyboardMarkup(inline_keyboard=[[button_yes,button_no]])