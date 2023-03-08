from aiogram import Bot
from data.constant import MY_ID_TELEGRAM
from aiogram.types import BotCommand
from lexicon.lexicon_ru import LEXICON_RU
from create_bot import dp, bot
import handlers




async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/menu',
            description=LEXICON_RU['menu_descr']),
        BotCommand(command='/help',
            description=LEXICON_RU['help_descr']),
        BotCommand(command='/add',
            description=LEXICON_RU['add_descr']),
        BotCommand(command='/settings',
            description=LEXICON_RU['settings_descr'])]

    await bot.set_my_commands(main_menu_commands)



if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.include_router(handlers.general_handlers.router)
    dp.include_router(handlers.settings_handlers.router)
    dp.include_router(handlers.add_handlers.router)
    dp.run_polling(bot)
