from data.constant import BOT_TOKEN
from aiogram import Bot, types
from aiogram import Dispatcher

bot: Bot = Bot(token = BOT_TOKEN)
dp: Dispatcher = Dispatcher()