from tg_bot_base import StaticScreen, Menu, ButtonRows, ButtonRow, Button, Screen
# from tg_bot_base import FunctionCallbackData as FCD
# from tg_bot_base import StepBackCallbackData as SBCD
from tg_bot_base import MenuCallbackData as MCD


def welcome() -> Screen:
    return StaticScreen(
        Menu("Добро пожаловать в Theoremator Bot",
            ButtonRows(
                    ButtonRow(
                    Button("Матрицы", MCD("matrices")),
                    Button("Линейные операторы", MCD("operators"))
                ),ButtonRow(
                    Button("Линейные пространства", MCD("matrices"))
                ),ButtonRow(
                    Button("Аккаунт", MCD("account")),
                    Button("Помощь", MCD("matrices"))
                )
            )
        ), name = "welcome"
    )