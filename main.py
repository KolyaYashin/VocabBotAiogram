from aiogram import Bot, Dispatcher
from data.constant import BOT_TOKEN, MY_ID_TELEGRAM
from aiogram.types import Message, BotCommand
from aiogram.filters import Text, Command
import filters as f
from aiogram import F


users: dict = {}
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
admin_ids = [MY_ID_TELEGRAM]

@dp.message(Command(commands=['start']))
async def proccess_start(message: Message):
    print(message.from_user.id)
    if message.from_user.id not in users:
        users[message.from_user.id]={
            'en':'',
            'ru':'',
            'tag':'',
            'score':0
        }
    await message.answer('/help для справки')

@dp.message(Command(commands=['help']))
async def proccess_help(message: Message):
    await message.answer('Список команд ...')

@dp.message(Command(commands=['add']))
async def proccess_add(message: Message):
    await message.answer('Введите новое слово на английском')


@dp.message(f.IsAdmin(admin_ids) and F.text == '/admin')
async def im_admin(message: Message):
    await message.answer("Ya u mami admin")

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