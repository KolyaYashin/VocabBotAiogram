import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Text,Command
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from data.constant import MY_ID_TELEGRAM
from keyboard import buttons


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
    await message.answer(text = 'Хочешь ли ты при добавлении нового слова писать его тэг? (напиши да/нет)',
                        reply_markup=buttons.keyboard_settings)


@router.callback_query(Text(text=['yes_pressed']))
async def proccess_button_yes_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    users.user_data[user_id]['include_tag'] = 1
    sql.execute(f'UPDATE users SET include_tag = 1 WHERE user_id = {user_id}')
    db.commit()
    await callback.message.answer(f'{users.user_data[user_id]["include_tag"]}, {users.user_data[user_id]["words_in_test"]}')
    sql.close()
    db.close()
    users.user_data[user_id]['state'] = 'in_menu'

@router.callback_query(Text(text=['no_pressed']))
async def proccess_button_yes_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    users.user_data[user_id]['include_tag'] = 0
    sql.execute(f'UPDATE users SET include_tag = 0 WHERE user_id = {user_id}')
    db.commit()
    await callback.message.answer(f'{users.user_data[user_id]["include_tag"]}, {users.user_data[user_id]["words_in_test"]}')
    sql.close()
    db.close()
    users.user_data[user_id]['state'] = 'in_menu'




@router.message(Command(commands=['settings']))
async def proccess_settings(message: Message):
    await message.answer('Ты можешь изменить количество слов, которое будет в тестах. \n'
                        'А также добавлять ли тэг в новые слова (если выключено, у новых слов будет стандартный тэг default).'
                        '\nВернуться в меню - /menu')
    user_id = message.from_user.id
    create_empty_user(user_id)
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    query = next(sql.execute(f'SELECT set_test_words AS words, include_tag AS tag FROM users WHERE user_id = {user_id}'))
    print(query)
    users.user_data[user_id]['include_tag'] = bool(query[1])
    users.user_data[user_id]['words_in_test'] = int(query[0])
    await message.answer(f'{users.user_data[user_id]["include_tag"]}, {users.user_data[user_id]["words_in_test"]}')
    users.user_data[user_id]['state'] = 'in_settings'
    sql.close()
    db.close()
