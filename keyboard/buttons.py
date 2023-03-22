from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_ru import LEXICON_RU

button_yes_settings = InlineKeyboardButton(text=LEXICON_RU['yes'], callback_data='yes_pressed_settings')
button_no_settings = InlineKeyboardButton(text=LEXICON_RU['no'], callback_data='no_pressed_settings')

keyboard_yes_no_settings = InlineKeyboardMarkup(inline_keyboard=[[button_yes_settings,button_no_settings]])


button_yes_delete = InlineKeyboardButton(text=LEXICON_RU['yes'], callback_data='yes_pressed_delete')
button_no_delete = InlineKeyboardButton(text=LEXICON_RU['no'], callback_data='no_pressed_delete')

keyboard_yes_no_delete = InlineKeyboardMarkup(inline_keyboard=[[button_yes_delete,button_no_delete]])