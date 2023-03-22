import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Command, Text
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from data.constant import MY_ID_TELEGRAM
from keyboard.buttons import keyboard_yes_no

router = Router()


def create_empty_user(user_id: int):
    if user_id not in users.user_data:
        users.user_data[user_id]={
            'en':'',
            'ru':'',
            'tag':'',
            'score':0,
            'state':'in_menu',
            'words_in_test':5,
            'include_tag': 1
        }


@router.message(Command(commands=['delete']))
async def proccess_start_delete(message: Message):
    user_id = message.from_user.id
    create_empty_user()
    users.user_data[user_id]['state'] = 'in_delete'
    await message.answer(LEXICON_RU['enter_en_word'])


@router.message(F.text, f.InDelete(users.user_data))
async def proccess_put_word_2delete(message: Message):
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    user_id = message.from_user.id
    select = sql.execute(f'SELECT * FROM words WHERE en={message.text} AND user_id={user_id}')
    if select.fetchone() is None:
        await message.answer(LEXICON_RU['havent_found'])
    else:
        await message.answer(LEXICON_RU['you_sure'],
                        reply_markup = keyboard_yes_no)
        users.user_data['en'] = message.text
    sql.close()
    db.close()


@router.callback_query(Text(text=['yes_pressed']))
async def proccess_delete_word(callback: CallbackQuery):
    user_id = callback.from_user.id
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    en = users.user_data['en']
    sql.execute(f'DELETE FROM words WHERE en = "{en}" AND user_id = {user_id}')
    db.commit()
    sql.close()
    db.close()


@router.callback_query(Text(text=['no_pressed']))
async def proccess_exit(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.answer(LEXICON_RU['stoped'])
    users.user_data[user_id] = 'in_menu'