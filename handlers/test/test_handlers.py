import data.create_tables as tables
from data.user_session import user_data

from data.create_empty import create_empty_user
from aiogram.filters import Command
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message
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
    user_data[user_id]['test_dictionary'] = Dictionary(count, 'data/words.db')
    user_data[user_id]['test_gen'] = user_data[user_id]['test_dictionary']()
    user_data[user_id]['current_word'] = next(user_data[user_id]['test_gen'])
    user_data[user_id]['state'] = 'in_test'
    sql.close()
    db.close()
    await message.answer(LEXICON_RU['test_start'] + str(count))
    await message.answer(LEXICON_RU['word_in_en']+(user_data[user_id]['current_word'].en))


@router.message(f.InTest(user_data), Command(commands=['stop']))
async def stop_in_test(message: Message):
    await message.answer(LEXICON_RU['test_ended'])
    await message.answer(LEXICON_RU['back_2menu'])


@router.message(F.text, f.InTest(user_data))
async def check_word(message: Message):
    user_id = message.from_user.id
    user_translate = message.text
    real_translate = user_data[user_id]['current_word'].ru
    if user_translate == real_translate:
        await message.answer(LEXICON_RU['correct_answer'])
        user_data[user_id]['test_dictionary'].delete_word(real_translate)
        try:
            user_data[user_id]['current_word'] = next(user_data[user_id]['test_gen'])
            await message.answer(LEXICON_RU['next_word']+(user_data[user_id]['current_word'].en))
        except StopIteration:
            await message.answer(LEXICON_RU['test_ended'])
            await message.answer(LEXICON_RU['back_2menu'])
    else:
        await message.answer(LEXICON_RU['wrong_answer']+real_translate)
        try:
            user_data[user_id]['current_word'] = next(user_data[user_id]['test_gen'])
            await message.answer(LEXICON_RU['next_word']+(user_data[user_id]['current_word'].en))
        except StopIteration:
            await message.answer(LEXICON_RU['test_ended'])
            await message.answer(LEXICON_RU['back_2menu'])
