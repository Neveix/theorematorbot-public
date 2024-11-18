from typing import TYPE_CHECKING, Any, Callable
from tg_bot_base import EvaluatedMenuDefault, ButtonRows, ButtonRow, Button
from tg_bot_base import FunctionCallbackData as FCD
from telegram import Message
from src.button_callbacks.common import generate_default_screen, \
    generate_input_error, leave, list_to_evaluated_screen
from libs.engine.engine import Matrix
if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager

async def binary_operation_step_1(user_id: int, bot_manager: "TheorematorManager", next_operation: Callable) -> None:
    bot_manager.user_data_manager.get(user_id).directory_stack.append("operation")
    screen = generate_default_screen("Введите первую матрицу:")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(user_id, next_operation)
    
async def binary_operation_step_2(message: Message, user_id: int, bot_manager: "TheorematorManager"\
        , next_operation: Callable) -> None:
    # Проверка, есть ли текст в сообщении?
    if message.text is None:
        await bot_manager.user_screen_manager.set_user_screen(
            user_id, 
            generate_input_error())
        return
    matrix = Matrix.createMatrix(message.text)
    # Проверка, есть ли ошибка ввода матрицы?
    if matrix.getErrorCode() != 0:
        await bot_manager.user_screen_manager.set_user_screen(
            user_id, 
            generate_input_error(matrix.getErrorMsg()["text"]))
        return
    bot_manager.user_data_manager.get(user_id).operation_operand1 = matrix
    # Если всё хорошо
    await bot_manager.user_screen_manager.set_user_screen(
        user_id, 
        generate_default_screen("Введите вторую матрицу:"))
    await bot_manager.message_manager.get_message_and_run_method(user_id, next_operation)
    
async def binary_operation_step_3(message: Message, user_id: int, bot_manager: "TheorematorManager",\
        operation: Callable[[Matrix, Matrix], Matrix]) -> None:
    # Проверка, есть ли текст в сообщении?
    if message.text is None:
        await bot_manager.user_screen_manager.set_user_screen(
            user_id, 
            generate_input_error())
        return
    matrix2 = Matrix.createMatrix(message.text)
    # Проверка, есть ли ошибка ввода матрицы?
    if matrix2.getErrorCode() != 0:
        await bot_manager.user_screen_manager.set_user_screen(
            user_id, 
            generate_input_error(matrix2.getErrorMsg()["text"]))
        return
    matrix1 = bot_manager.user_data_manager.get(user_id).operation_operand1
    # Вычисляется результат
    matrix3 = operation(matrix1, matrix2)
    solution_as_list = matrix3.getTextSolution()
    # solution_as_list = matrix3.getImageSolution()
    solution = list_to_evaluated_screen(solution_as_list)
    # Если всё хорошо
    screen = solution
    screen.extend(
        EvaluatedMenuDefault("Вернуться назад?", 
            ButtonRows(
                ButtonRow(
                    Button("Назад", FCD(leave))
                )
            )
        ),
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)


async def unary_operation_step_1(user_id: int, bot_manager: "TheorematorManager", next_operation: Callable) -> None:
    bot_manager.user_data_manager.get(user_id).directory_stack.append("operation")
    screen = generate_default_screen("Введите матрицу:")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(user_id, next_operation)
    
async def unary_operation_step_2(message: Message, user_id: int, bot_manager: "TheorematorManager",\
        operation: Callable[[Matrix], Any]) -> None:
    # Проверка, есть ли текст в сообщении?
    if message.text is None:
        await bot_manager.user_screen_manager.set_user_screen(
            user_id, 
            generate_input_error())
        return
    matrix = Matrix.createMatrix(message.text)
    # Проверка, есть ли ошибка ввода матрицы?
    if matrix.getErrorCode() != 0:
        await bot_manager.user_screen_manager.set_user_screen(
            user_id, 
            generate_input_error(matrix.getErrorMsg()["text"]))
        return
    # Вычисляется результат
    matrix2 = operation(matrix)
    solution_as_list = matrix2.getTextSolution()
    # solution_as_list = matrix2.getImageSolution()
    solution = list_to_evaluated_screen(solution_as_list)
    # Если всё хорошо
    screen = solution
    screen.extend(
        EvaluatedMenuDefault("Вернуться назад?", 
            ButtonRows(
                ButtonRow(
                    Button("Назад", FCD(leave))
                )
            )
        ),
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    