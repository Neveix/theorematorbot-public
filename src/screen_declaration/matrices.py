from tg_bot_base import StaticScreen, Menu, ButtonRows, ButtonRow, Button, Screen
from tg_bot_base import FunctionCallbackData as FCD
from tg_bot_base import StepBackCallbackData as SBCD
# from tg_bot_base import MenuCallbackData as MCD

from src.button_callbacks.operations.matrices.add import operation_add_step_1
from src.button_callbacks.operations.matrices.diff import operation_diff_step_1
from src.button_callbacks.operations.matrices.mult import operation_mult_step_1
from src.button_callbacks.operations.matrices.inverse import operation_inverse_step_1
from src.button_callbacks.operations.matrices.transpose import operation_transpose_step_1
from src.button_callbacks.operations.matrices.determinant import operation_determinant_step_1

def matrices() -> Screen:
    return StaticScreen(
        Menu("Операции с матрицами",
            ButtonRows(
                ButtonRow(
                    Button("+", FCD(operation_add_step_1)),
                    Button("-", FCD(operation_diff_step_1)),
                    Button("*", FCD(operation_mult_step_1)),
                ), ButtonRow(
                    Button("Обратная матрица", FCD(operation_inverse_step_1)),
                ), ButtonRow(
                    Button("Транспонировать", FCD(operation_transpose_step_1)),
                    Button("Определитель", FCD(operation_determinant_step_1)),
                ), ButtonRow(
                    Button("Назад", SBCD()),
                )
            )
        ), name = "matrices"
    )
    