from aiogram import Bot, Dispatcher
from data.constant import BOT_TOKEN, MY_ID_TELEGRAM
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
import filters as f
from aiogram import F
import data.create_tables as tables
import data.user_session as users

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
admin_ids = [MY_ID_TELEGRAM]

@dp.message(Command(commands=['start']))
async def proccess_start(message: Message):
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    if message.from_user.id not in users.user_data:
        users.user_data[message.from_user.id]={
            'en':'',
            'ru':'',
            'tag':'',
            'score':0,
            'state':'in_menu',
            'words_in_test':5,
            'include_tag': 1
        }
    user_id = message.from_user.id
    count = sql.execute(f'SELECT COUNT(*) FROM users WHERE user_id={user_id}')
    if next(count)[0]==0:
        sql.execute(f'INSERT INTO users VALUES ({user_id}, 0, 0, 0, 1000, 5, 1)')
        db.commit()
    await message.answer('/help для справки')
    sql.close()
    db.close()

@dp.message(Command(commands=['help']))
async def proccess_help(message: Message):
    await message.answer('Список команд ...')



@dp.message( F.text.startswith('/admin'),f.IsAdmin(admin_ids))
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


@dp.message(Command(commands=['setting']))
async def proccess_settings(message: Message):
    await message.answer('Ты можешь изменить  количество слов в тесте'
        'изначально - 5')


@dp.message(Command(commands=['add']))
async def proccess_add(message: Message):
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    user_id = message.from_user.id
    incl_tag = next(sql.execute(f"SELECT include_tag FROM users WHERE user_id={user_id}"))[0]
    if user_id not in users.user_data:
        users.user_data[user_id] = {
            'en':'',
            'ru':'',
            'tag':'',
            'score':0,
            'state':'in_menu',
            'words_in_test':5,
            'include_tag': incl_tag
        }

    users.user_data[user_id]['state']='in_add_en'
    await message.answer('Введите слово на английском')
    sql.close()
    db.close()

@dp.message(F.text, f.InAddEn(users.user_data))
async def proccess_add_en(message: Message):
    user_id = message.from_user.id
    en = message.text
    users.user_data[user_id]['en'] = en
    users.user_data[user_id]['state'] = 'in_add_ru'
    await message.answer('Введите перевод слова')

@dp.message(F.text, f.InAddRu(users.user_data))
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
        sql.execute(f'INSERT INTO words VALUES ({rows_count+1}, {user_id}, {users.user_data[user_id]["en"]}), '
                    f'{users.user_data[user_id]["ru"]}, {users.user_data[user_id]["tag"]}, DATE("now", "localtime"), '
                    'DATE("now", "localtime"), 0, 0, 0, 1)')
        db.commit()
        sql.close()
        db.close()
        await message.answer(f'Слово {users.user_data[user_id]["en"]} успешно добавлено!')
        users.user_data[user_id]['state'] = 'in_menu'


@dp.message(F.text, f.InAddTag(users.user_data))
async def proccess_add_tag(message: Message):
    user_id = message.from_user.id
    tag = message.text
    users.user_data[user_id]['tag'] = tag
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    rows_count = next(sql.execute("SELECT COUNT(*) FROM words"))[0]
    sql.execute(f'INSERT INTO words VALUES ({rows_count+1}, {user_id}, "{users.user_data[user_id]["en"]}", '
                f'"{users.user_data[user_id]["ru"]}", "{users.user_data[user_id]["tag"]}", DATE("now", "localtime"), '
                'DATE("now", "localtime"), 0, 0, 0, 1)')
    db.commit()
    sql.close()
    db.close()
    await message.answer(f'Слово {users.user_data[user_id]["en"]} успешно добавлено!')
    users.user_data[user_id]['state'] = 'in_menu'





async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/help',
            description='Справка для бота'),
        BotCommand(command='/add',
            description='Добавить слово'),
        BotCommand(command='/settings',
            description='Настройка некоторых параметров')]
    await bot.set_my_commands(main_menu_commands)



if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
