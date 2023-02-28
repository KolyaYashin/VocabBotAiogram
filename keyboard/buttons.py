from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_ru import LEXICON_RU

button_yes = InlineKeyboardButton(text=LEXICON_RU['yes'], callback_data='yes_pressed')
button_no = InlineKeyboardButton(text=LEXICON_RU['no'], callback_data='no_pressed')



keyboard_settings = InlineKeyboardMarkup(inline_keyboard=[[button_yes,button_no]])