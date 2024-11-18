from src.managers.theoremator_manager import TheorematorManager

def init_bot() -> TheorematorManager:
    bot_manager = TheorematorManager()
    bot_manager.yookassa_manager.return_url = "https://t.me/theorematorbot"
    bot_manager.create_menus()
    from os import mkdir
    try:
        mkdir("./db")
    except FileExistsError:
        pass
    from src.managers.global_user_data_manager import GlobalUserDataManager
    bot_manager.init_global_user_data(
        GlobalUserDataManager("./db/global_user_data.db"))
    from tg_bot_base import Command
    from src.command_callbacks.convert_handler import convert_handler
    from src.command_callbacks.start import start
    bot_manager.command_manager.add(Command("start", convert_handler(bot_manager, start)))
    from src.command_callbacks.admin import admin
    bot_manager.command_manager.add(Command("admin", convert_handler(bot_manager, admin)))
    return bot_manager

#def init_yookassa() -> None:
#    from yookassa import Configuration
#    from src.config.access import yookassa_secret_key, yookassa_shop_id
#    Configuration.account_id = yookassa_shop_id
#    Configuration.secret_key = yookassa_secret_key