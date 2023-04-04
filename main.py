from create_bot import dp, bot
import handlers
from main_menu import set_main_menu



if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.include_router(handlers.general_handlers.router)
    dp.include_router(handlers.settings_handlers.router)
    dp.include_router(handlers.add_handlers.router)
    dp.include_router(handlers.delete_handlers.router)
    dp.run_polling(bot)