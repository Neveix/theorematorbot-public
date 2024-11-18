
from src.managers.theoremator_manager import TheorematorManager

async def handle_premium(bot_manager: TheorematorManager, user_id: int, premium_subscription_payment: str) -> None:
    payment = await bot_manager.yookassa_manager.payment_create(
        "Платёж за подписку Premium",
        10,
        payment_method_id = premium_subscription_payment
    )
    bot_manager.logger.info(f"handling premium {premium_subscription_payment=} {payment.status=}")
    if payment.status == "succeeded":
        bot_manager.global_user_data.premium_update_time(user_id)
    elif payment.status == "canceled":
        bot_manager.global_user_data.premium_deactivate(user_id)

async def job_premium_check(bot_manager: TheorematorManager, _) -> None:
    premiums = bot_manager.global_user_data.premium_get_old(60)
    tasks = [handle_premium(
        bot_manager, user_id, premium_subscription_payment)
        for user_id, premium_subscription_payment in premiums
    ]
    from asyncio import gather
    await gather(*tasks)