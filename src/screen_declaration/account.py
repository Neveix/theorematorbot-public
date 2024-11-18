from tg_bot_base import StaticScreen, DynamicScreen, Menu, ButtonRows, ButtonRow, Button, Screen
from tg_bot_base import FunctionCallbackData as FCD
from tg_bot_base import StepBackCallbackData as SBCD
from tg_bot_base import MenuCallbackData as MCD

from src.managers.theoremator_manager import TheorematorManager

def account_screen(bot_manager: "TheorematorManager", user_id: int) -> list[Menu]:
    balance = bot_manager.global_user_data.user_balance_get(user_id)
    return [Menu(f"Ваш баланс : {balance}",
        ButtonRows(
            ButtonRow(
                Button("Пополнить баланс", MCD("account_deposit")),
            ), ButtonRow(
                Button("Подписка Premium", MCD("account_premium")),
            ), ButtonRow(
                Button("Поддержать авторов", SBCD()),
            ), ButtonRow(
                Button("Назад", SBCD()),
            )
        )
    )]

def account() -> Screen:
    return DynamicScreen(
        account_screen
        , name = "account"
    )

def account_deposit() -> Screen:
    from src.button_callbacks.account.deposit import deposit_fixed, deposit_custom_step_1
    return StaticScreen(
        Menu("Пополнить баланс",
            ButtonRows(
                ButtonRow(
                    Button("20р", FCD( deposit_fixed, amount = 20)),
                    Button("50р", FCD( deposit_fixed, amount = 50)),
                    Button("100р", FCD(deposit_fixed, amount = 100)),
                ), ButtonRow(
                    Button("150р", FCD(deposit_fixed, amount = 150)),
                    Button("200р", FCD(deposit_fixed, amount = 200)),
                    Button("300р", FCD(deposit_fixed, amount = 300)),
                ), ButtonRow(
                    Button("Своя сумма", FCD(deposit_custom_step_1)),
                ), ButtonRow(
                    Button("Назад", SBCD()),
                )
            )
        ), name = "account_deposit"
    )

def account_premium() -> Screen:
    return DynamicScreen(
        account_premium_screen, name = "account_premium"
    )

def account_premium_screen(bot_manager: "TheorematorManager", user_id: int) -> list[Menu]:
    is_premium, _, _ = bot_manager.global_user_data.premium_get(user_id)
    from src.button_callbacks.account.premium import premium_subscription, premium_unsubscription
    button_rows = ButtonRows()
    if not is_premium:
        button = Button("Подписаться на Premium", FCD(premium_subscription))
    else:
        button = Button("Отписаться от Premium-подписки", FCD(premium_unsubscription))
    button_rows.extend(
        ButtonRow(
            button
        ),ButtonRow(
            Button("Назад", SBCD()),
        )
    )
    return [
        Menu("Тут вы можете управлять своей подпиской",
            button_rows)
    ]