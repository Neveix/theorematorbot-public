from tg_bot_base import EvaluatedScreen, EvaluatedMenuDefault, ButtonRows
from src.managers.theoremator_manager import TheorematorManager
from src.managers.yookassa_manager import Payment

async def regular_payment(bot_manager: TheorematorManager, user_id: int, payment: Payment) -> None:
    amount = payment.amount.value
    bot_manager.global_user_data.user_balance_add(user_id, amount)
    bot_manager.logger.info(f"{payment.id} успешно оплачен ({amount} руб.)")
    bot_manager.user_screen_manager.clear_user_screen(user_id)
    screen = EvaluatedScreen(
        EvaluatedMenuDefault(
            f"Оплата {amount} рублей успешно прошла",
            ButtonRows()
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)

async def premium_payment(bot_manager: TheorematorManager, user_id: int, payment: Payment, payed_at: int) -> None:
    bot_manager.global_user_data.premium_activate(user_id, payed_at, payment.id)
    bot_manager.logger.info(f"Подписка Premium от платежа {payment.id} успешно активирована")
    bot_manager.user_screen_manager.clear_user_screen(user_id)
    screen = EvaluatedScreen(
        EvaluatedMenuDefault(
            f"Вы успешно подписались на Premium",
            ButtonRows()
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)

async def support_payment(bot_manager: TheorematorManager, user_id: int, payment: Payment, payed_at: int) -> None:
    bot_manager.global_user_data.support_activate(user_id, payed_at, payment.id)
    bot_manager.logger.info(f"Подписка на авторов бота ({payment.id}) успешно активирована")
    bot_manager.user_screen_manager.clear_user_screen(user_id)
    screen = EvaluatedScreen(
        EvaluatedMenuDefault(
            f"Вы успешно подписались на поддержку бота!",
            ButtonRows()
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    

async def handle_payment(bot_manager: TheorematorManager, user_id: int, 
        payment: Payment, created_at: int, payment_purpose: int):
    from src.managers.global_user_data_manager import \
        PAYMENT_PURPOSE_REGULAR, PAYMENT_PURPOSE_PREMIUM, PAYMENT_PURPOSE_SUPPORT
    bot_manager.global_user_data.payment_set_succeeded(payment.id)
    if payment_purpose == PAYMENT_PURPOSE_REGULAR:
        await regular_payment(bot_manager, user_id, payment)
    elif payment_purpose == PAYMENT_PURPOSE_PREMIUM:
        await premium_payment(bot_manager, user_id, payment, created_at)
    elif payment_purpose == PAYMENT_PURPOSE_SUPPORT:
        await support_payment(bot_manager, user_id, payment, created_at)

async def job_payment_check(bot_manager: TheorematorManager, _) -> None:
    bot_manager.global_user_data.payments_remove_old()
    payments_data = bot_manager.global_user_data.payment_get_not_succeeded()
    if payments_data == []:
        return
    payments_dict = {payment_id : (user_id, created_at, payment_purpose) \
        for user_id, payment_id, created_at, payment_purpose in payments_data}
    created_at_stamps = [payment_data[2] for payment_data in payments_data]
    created_at_min = min(created_at_stamps)
    from datetime import datetime
    created_at_min_iso = datetime.fromtimestamp(created_at_min).isoformat()
    created_at_min_iso = "2024-11-10T15:35:45"
    response = await bot_manager.yookassa_manager.payments_succeeded_list(
        created_at_gte=created_at_min_iso
    )
    try:
        response_payments = response["items"]
    except KeyError:
        bot_manager.logger.warning(
            f"error getting items of job_payment_check {response=}")
        return
    for payment_json in response_payments:
        payment = Payment.from_json(payment_json)
        if payment.status != "succeeded":
            continue
        
        try:
            user_id, created_at, payment_purpose = payments_dict[payment.id]
            await handle_payment(bot_manager, user_id, payment, created_at, payment_purpose)
            bot_manager.logger.info(f"successful payment {payment.id}")
        except KeyError:
            continue