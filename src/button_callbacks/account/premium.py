from typing import TYPE_CHECKING
from tg_bot_base import EvaluatedScreen, EvaluatedMenuDefault, ButtonRows
from src.button_callbacks.common import generate_default_screen
if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager

async def premium_subscription(user_id: int, bot_manager: "TheorematorManager", **kwargs):
    bot_manager.user_data_manager.get(user_id).directory_stack.append("premium_subscription")
    is_premium, _, _ = bot_manager.global_user_data.premium_get(user_id)
    if is_premium:
        screen = generate_default_screen("Вы уже подписаны на Premium")
        bot_manager.user_screen_manager.set_user_screen(user_id, screen)
        return
    payment = await bot_manager.yookassa_manager.payment_create(
        "Подписка на Premium", 10, save_payment_method = True
    )
    link: str = payment.confirmation.confirmation_url
    from telegram.constants import ParseMode
    screen = EvaluatedScreen(
        EvaluatedMenuDefault(
            f"Вы можете подписаться на Premium [по этой ссылке]({link})\n\n\
После подписки мы запомним этот платёж и сможем повторять его каждый месяц\n\n\
Вы всегда можете отказаться от Premium в настройках аккаунта\n\n\
Вернуться в начало: /start", 
            ButtonRows(),
            parse_mode = ParseMode.MARKDOWN_V2
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)

async def premium_unsubscription(user_id: int, bot_manager: "TheorematorManager", **kwargs):
    bot_manager.user_data_manager.get(user_id).directory_stack.append("premium_subscription")
    is_premium, _, _ = bot_manager.global_user_data.premium_get(user_id)
    if not is_premium:
        screen = generate_default_screen("Вы не подписаны на Premium")
        bot_manager.user_screen_manager.set_user_screen(user_id, screen)
        return
    bot_manager.global_user_data.premium_deactivate(user_id)
    screen = EvaluatedScreen(
        EvaluatedMenuDefault(
            "Вы успешно отписались от Premium \
Вернуться в начало: /start", 
            ButtonRows(),
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)