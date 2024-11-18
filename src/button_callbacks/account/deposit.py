from typing import TYPE_CHECKING
from tg_bot_base import EvaluatedScreen, EvaluatedMenuDefault, ButtonRows
from telegram import Message
from src.button_callbacks.common import generate_default_screen, generate_input_error
if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager

async def deposit_fixed(user_id: int, bot_manager: "TheorematorManager", \
        amount: int = 10, **kwargs) -> None:
    payment = await bot_manager.yookassa_manager.payment_create(
        f"Пополнение баланса на {amount} рублей",
        amount, False)
    from src.managers.global_user_data_manager import \
        PAYMENT_PURPOSE_REGULAR
    bot_manager.global_user_data.payment_add(user_id, payment.id, PAYMENT_PURPOSE_REGULAR)
    link: str = payment.confirmation.confirmation_url
    from telegram.constants import ParseMode
    screen = EvaluatedScreen(
        EvaluatedMenuDefault(
            f"Вы можете пополнить баланс [по этой ссылке]({link})\n \
Вернуться в начало: /start", 
            ButtonRows(),
            parse_mode = ParseMode.MARKDOWN_V2
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)

async def deposit_custom_step_1(user_id: int, bot_manager: "TheorematorManager", **kwargs):
    bot_manager.user_data_manager.get(user_id).directory_stack.append("deposit_custom")
    screen = generate_default_screen("Введите сумму для пополнения:")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(user_id, deposit_custom_step_2)
    
async def deposit_custom_step_2(message: Message, user_id: int, bot_manager: "TheorematorManager", **kwargs):
    if message.text is None:
        await bot_manager.user_screen_manager.set_user_screen(
            user_id, 
            generate_input_error())
        return
    try:
        value = int(message.text)
    except ValueError:
        await bot_manager.user_screen_manager.set_user_screen(
            user_id, 
            generate_input_error("Невозможно преобразовать к числу"))
        return
    if value < 10 or 50000 <= value:
        await bot_manager.user_screen_manager.set_user_screen(
            user_id, 
            generate_input_error("Число либо слишком маленькое, либо слишком большое"))
        return
    await deposit_fixed(user_id = user_id, bot_manager = bot_manager, amount = value, **kwargs)