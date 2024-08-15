import os

import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Command
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message
from aiogram import Router, F
from data.create_empty import create_empty_user
from keyboard.buttons import menu_keyboard

global MY_ID_TELEGRAM
MY_ID_TELEGRAM = os.environ['MY_TG_ID']
admin_ids = [MY_ID_TELEGRAM]
router = Router()


@router.message(Command(commands=['start']))
async def proccess_start(message: Message):
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host="postgres_db",  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    create_empty_user(message.from_user.id)
    user_id = message.from_user.id
    count = sql.execute(f'SELECT COUNT(*) FROM users WHERE user_id={user_id}')
    if next(count)[0]==0:
        sql.execute(f'INSERT INTO users VALUES ({user_id}, 0, 0, 0, 1000, 5, 0)')
        db.commit()
    await message.answer(LEXICON_RU['welcome'])
    sql.close()
    db.close()


@router.message(Command(commands=['help']))
async def proccess_help(message: Message):
    await message.answer(LEXICON_RU['help'])


@router.message(Command(commands = ['stop']))
async def proccess_stop(message: Message):
    user_id = message.from_user.id
    create_empty_user(user_id)
    await message.answer('Операция остановлена. Чтобы выйти в меню нажмите /menu')
    users.user_data[user_id]['state'] = 'in_menu'


@router.message(Command(commands = ['menu']))
async def proccess_menu(message: Message):
    user_id = message.from_user.id
    create_empty_user(user_id)
    users.user_data[user_id]['state'] = 'in_menu'
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host="postgres_db",  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    user_rating = int(sql.execute(f'SELECT rating FROM users WHERE user_id={user_id}').fetchone()[0])
    await message.answer(f'Рейтинг - {user_rating}',reply_markup=menu_keyboard)
    sql.close()
    db.close()


@router.message( F.text.startswith('/admin'),f.IsAdmin(admin_ids))
async def proccess_admin(message: Message, text: str):
    db = tables.psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                                 user=os.environ['POSTGRES_USER'],
                                 password=os.environ['POSTGRES_PASSWORD'],
                                 host="postgres_db",  # Это имя контейнера с базой данных
                                 port="5432")
    sql = db.cursor()
    table = sql.execute(f'SELECT * FROM users')
    user_to_delete: int
    try:
        user_to_delete = int(text)
    except ValueError as e:
        await message.answer("введи число")
        return
    await message.answer(str(table.fetchmany(5)))
    if next(sql.execute(f'SELECT COUNT() FROM users WHERE (user_id = {user_to_delete})'))[0] != 0:
        with db:
            sql.execute(f'DELETE FROM users WHERE (user_id = {user_to_delete})')
            await message.answer(f'пользователь {user_to_delete} удалён')
    else:
        await message.answer('такого пользователя нет')
    sql.close()
    db.close()
