from data.constant import BOT_TOKEN
from aiogram import Bot
from aiogram import Dispatcher

bot: Bot = Bot(token = BOT_TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher()