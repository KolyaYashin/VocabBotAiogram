import data.create_tables as tables
import data.user_session as users
from aiogram.filters import Command, Text
import filters.filters as f
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message
from aiogram import Router, F
from data.constant import MY_ID_TELEGRAM
from data.create_empty import create_empty_user


admin_ids = [MY_ID_TELEGRAM]
router = Router()



@router.message(Command(commands=['add']))
async def proccess_add(message: Message):
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    user_id = message.from_user.id
    create_empty_user(user_id)
    incl_tag = next(sql.execute(f"SELECT include_tag FROM users WHERE user_id={user_id}"))[0]
    print()
    users.user_data[user_id]['include_tag'] = int(incl_tag)
    users.user_data[user_id]['state']='in_add_en'
    await message.answer('Введите слово на английском')
    sql.close()
    db.close()

@router.message(F.text,~Text(startswith='/'), f.InAddEn(users.user_data))
async def proccess_add_en(message: Message):
    user_id = message.from_user.id
    en = message.text
    users.user_data[user_id]['en'] = en
    users.user_data[user_id]['state'] = 'in_add_ru'
    await message.answer('Введите перевод слова')

@router.message(F.text,~Text(startswith='/'), f.InAddRu(users.user_data))
async def proccess_add_ru(message: Message):
    user_id = message.from_user.id
    ru = message.text
    users.user_data[user_id]['ru'] = ru
    if users.user_data[user_id]['include_tag']:
        users.user_data[user_id]['state'] = 'in_add_tag'
        await message.answer('Введите тэг слова')
    else:
        users.user_data[user_id]['tag'] = 'none'
        db = tables.sqlite3.connect('data/words.db')
        sql = db.cursor()
        rows_count = next(sql.execute("SELECT COUNT(*) FROM words"))[0]
        sql.execute(f'INSERT INTO words VALUES ({user_id}, "{users.user_data[user_id]["en"]}", '
                f'"{users.user_data[user_id]["ru"]}", "{users.user_data[user_id]["tag"]}", DATE("now", "localtime"), '
                '0, 0, 0, 1)')
        db.commit()
        sql.close()
        db.close()
        await message.answer(f'Слово {users.user_data[user_id]["en"]}, {users.user_data[user_id]["ru"]},'
                            f' {users.user_data[user_id]["tag"]} успешно добавлено!')
        await message.answer('Вы можете либо добавить следующее слово, либо нажать на /menu')
        users.user_data[user_id]['state'] = 'in_add_en'


@router.message(F.text,~Text(startswith='/'), f.InAddTag(users.user_data))
async def proccess_add_tag(message: Message):
    user_id = message.from_user.id
    tag = message.text
    users.user_data[user_id]['tag'] = tag
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    rows_count = next(sql.execute("SELECT COUNT(*) FROM words"))[0]
    sql.execute(f'INSERT INTO words VALUES ( {user_id}, "{users.user_data[user_id]["en"]}", '
                f'"{users.user_data[user_id]["ru"]}", "{users.user_data[user_id]["tag"]}", DATE("now", "localtime"), '
                '0, 0, 0, 0)')
    db.commit()
    sql.close()
    db.close()
    await message.answer(f'Слово {users.user_data[user_id]["en"]}, {users.user_data[user_id]["ru"]}, '
                        f'{users.user_data[user_id]["tag"]} успешно добавлено!')
    await message.answer('Вы можете либо добавить следующее слово, либо нажать на /menu')
    users.user_data[user_id]['state'] = 'in_add_en'
