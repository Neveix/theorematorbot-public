from typing import TYPE_CHECKING
from telegram import Update
from telegram.ext import ContextTypes
if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager

async def admin(bot_manager: "TheorematorManager", update : Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    user_id = user.id
    #bot_manager.user_global_data.set_user_advanced_data(user.id,\
    #    user.first_name, user.last_name, user.username)
    #bot_manager.logger.info(f"{user_id} написал /start")
    screen_name = "admin_menu"
    bot_manager.user_data_manager.reset(user_id)
    await bot_manager.user_screen_manager.set_user_screen_by_name(user_id, screen_name)