import data.create_tables as tables
import data.user_session as users
from data.create_empty import create_empty_user
from aiogram.filters import Command, Text
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from data.constant import MY_ID_TELEGRAM
from keyboard.buttons import keyboard_yes_no_delete
from classes.classes import Dictionary

router = Router()



@router.message(Command(commands=['test']))
async def start_test(message:Message):
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    user_id = message.from_user.id
    count = next(sql.execute(f'SELECT set_test_words FROM users WHERE user_id={user_id}'))[0]
    create_empty_user(user_id)
    users.user_data['test_dictionary'] = Dictionary(count, 'data/words.db')
    users.user_data['state'] = 'in_test'
    sql.close()
    db.close()
    await message.answer(LEXICON_RU['test_start'] + str(count))