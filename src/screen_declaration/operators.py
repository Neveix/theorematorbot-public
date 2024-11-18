from tg_bot_base import StaticScreen, Menu, ButtonRows, ButtonRow, Button, Screen
from tg_bot_base import FunctionCallbackData as FCD
from tg_bot_base import StepBackCallbackData as SBCD

from src.button_callbacks.operations.operators.rank import operation_rank_step_1
from src.button_callbacks.operations.operators.mlis import operation_mlis_step_1
from src.button_callbacks.operations.operators.islis import operation_islis_step_1
from src.button_callbacks.operations.operators.find_basis import operation_find_basis_step_1
from src.button_callbacks.operations.operators.chars import operation_chars_step_1

def operators() -> Screen:
    return StaticScreen(
        Menu("Операции с линейными операторами",
            ButtonRows(
                ButtonRow(
                    Button("Макс. линейно независимая подсистема", FCD(operation_mlis_step_1)),
                ), ButtonRow(
                    Button("Ранг", FCD(operation_rank_step_1)),
                    Button("Найти базис", FCD(operation_find_basis_step_1)),
                ), ButtonRow(
                    Button("Проверка на линейную независимость", FCD(operation_islis_step_1)),
                ), ButtonRow(
                    Button("Ядро/Образ/Ранг/Дефект", FCD(operation_chars_step_1)),
                ), ButtonRow(
                    Button("Назад", SBCD()),
                )
            )
        ), name = "operators"
    )
    