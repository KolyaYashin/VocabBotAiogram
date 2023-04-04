import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Text,Command
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from data.constant import MY_ID_TELEGRAM
from keyboard.buttons import keyboard_yes_no_settings


admin_ids = [MY_ID_TELEGRAM]
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


@router.message(Command(commands=['tag']), f.InSettings(users.user_data))
async def proccess_change_incl_tag(message: Message):
    await message.answer(text = 'Хочешь ли ты при добавлении нового слова писать его тэг?',
                        reply_markup = keyboard_yes_no_settings)



@router.message(Command(commands=['count']), f.InSettings(users.user_data))
async def proccess_change_incl_tag(message: Message):
    await message.answer(text = 'Тесты на сколько слов хочешь проходить?')

@router.message(lambda message: message.text.isnumeric(), f.InSettings(users.user_data))
async def isnumeric(message: Message):
    new_count = int(message.text)
    user_id = message.from_user.id
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    sql.execute(f'UPDATE users SET set_test_words = {new_count} WHERE user_id = {user_id}')
    db.commit()
    sql.close()
    db.close()
    await message.answer(LEXICON_RU['new_count'] + str(new_count)+'\n'+ LEXICON_RU['back_2menu'])



@router.callback_query(Text(text=['yes_pressed_settings']), f.InSettings(users.user_data))
async def proccess_button_yes_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    users.user_data[user_id]['include_tag'] = 1
    sql.execute(f'UPDATE users SET include_tag = 1 WHERE user_id = {user_id}')
    db.commit()
    await callback.message.answer(LEXICON_RU['now_tag_included'])
    sql.close()
    db.close()
    users.user_data[user_id]['state'] = 'in_menu'
    await callback.message.answer(LEXICON_RU['back_2menu'])
    await callback.answer()

@router.callback_query(Text(text=['no_pressed_settings']), f.InSettings(users.user_data))
async def proccess_button_yes_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    users.user_data[user_id]['include_tag'] = 0
    sql.execute(f'UPDATE users SET include_tag = 0 WHERE user_id = {user_id}')
    db.commit()
    await callback.message.answer(LEXICON_RU['now_tag_disabled'])
    sql.close()
    db.close()
    users.user_data[user_id]['state'] = 'in_menu'
    await callback.message.answer(LEXICON_RU['back_2menu'])
    await callback.answer()





@router.message(Command(commands=['settings']))
async def proccess_settings(message: Message):
    await message.answer(LEXICON_RU['settings_start'] + LEXICON_RU['back_2menu'] + LEXICON_RU['change_tag'] + LEXICON_RU['change_count'])
    user_id = message.from_user.id
    create_empty_user(user_id)
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    query = next(sql.execute(f'SELECT set_test_words AS words, include_tag AS tag FROM users WHERE user_id = {user_id}'))
    users.user_data[user_id]['include_tag'] = bool(query[1])
    users.user_data[user_id]['words_in_test'] = int(query[0])
    if users.user_data[user_id]["include_tag"]:
        await message.answer(LEXICON_RU['settings_current_pos'] + str(users.user_data[user_id]["words_in_test"]))
    else:
        await message.answer(LEXICON_RU['settings_current_neg'] + str(users.user_data[user_id]["words_in_test"]))
    users.user_data[user_id]['state'] = 'in_settings'
    sql.close()
    db.close()
