import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Command
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message
from aiogram import Router, F
from data.constant import MY_ID_TELEGRAM



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

@router.message(Command(commands=['start']))
async def proccess_start(message: Message):
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    create_empty_user(message.from_user.id)
    user_id = message.from_user.id
    count = sql.execute(f'SELECT COUNT(*) FROM users WHERE user_id={user_id}')
    if next(count)[0]==0:
        sql.execute(f'INSERT INTO users VALUES ({user_id}, 0, 0, 0, 1000, 5, 1)')
        db.commit()
    await message.answer(LEXICON_RU['welcome'])
    sql.close()
    db.close()

@router.message(Command(commands=['help']))
async def proccess_help(message: Message):
    await message.answer('Список команд ...')

@router.message(Command(commands = ['stop']))
async def proccess_stop(message: Message):
    user_id = message.from_user.id
    create_empty_user(user_id)
    await message.answer('Операция остановлена. Чтобы выйти в меню нажмите /menu')
    users.user_data[user_id] = 'in_menu'

@router.message(Command(commands = ['menu']))
async def proccess_menu(message: Message):
    user_id = message.from_user.id
    create_empty_user(user_id)
    users.user_data[user_id] = 'in_menu'
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    user_rating = int(sql.execute(f'SELECT rating FROM users WHERE user_id={user_id}').fetchone()[0])
    await message.answer(f'Рейтинг - {user_rating}')
    sql.close()
    db.close()


@router.message( F.text.startswith('/admin'),f.IsAdmin(admin_ids))
async def proccess_admin(message: Message, text: str):
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    table = sql.execute(f'SELECT * FROM users')
    user_to_delete: int
    try:
        user_to_delete = int(text)
    except ValueError as e:
        await message.answer("введи число")
        return
    await message.answer(str(table.fetchmany(5)))
    if next(sql.execute(f'SELECT COUNT() FROM users WHERE (user_id = {user_to_delete})'))[0]!=0:
        with db:
            sql.execute(f'DELETE FROM users WHERE (user_id = {user_to_delete})')
            await message.answer(f'пользователь {user_to_delete} удалён')
    else:
        await message.answer('такого пользователя нет')
    sql.close()
    db.close()
