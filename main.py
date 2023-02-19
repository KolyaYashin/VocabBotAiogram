from aiogram import Bot, Dispatcher
from data.constant import BOT_TOKEN, MY_ID_TELEGRAM
from aiogram.types import Message, BotCommand
from aiogram.filters import Text, Command
import filters as f
from aiogram import F
import data.create_tables as tables


users: dict = {}
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
admin_ids = [MY_ID_TELEGRAM]

@dp.message(Command(commands=['start']))
async def proccess_start(message: Message):
    db = tables.sqlite3.connect('data/words.db')
    sql = db.cursor()
    if message.from_user.id not in users:
        users[message.from_user.id]={
            'en':'',
            'ru':'',
            'tag':'',
            'score':0
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

@dp.message(Command(commands=['add']))
async def proccess_add(message: Message):
    await message.answer('Введите новое слово на английском')


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