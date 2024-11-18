from typing import TYPE_CHECKING
from telegram import Message
from src.button_callbacks.operations.templates import \
    unary_operation_step_1, unary_operation_step_2
from libs.engine.engine import Matrix
if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager

async def operation_determinant_step_1(user_id: int, bot_manager: "TheorematorManager", **kwargs) -> None:
    await unary_operation_step_1(
        user_id = user_id,
        bot_manager = bot_manager,
        next_operation = operation_determinant_step_2
    )
    
async def operation_determinant_step_2(message: Message, user_id: int, bot_manager: "TheorematorManager", **kwargs) -> None:
    await unary_operation_step_2(
        user_id = user_id,
        message = message,
        bot_manager = bot_manager,
        operation = Matrix.determinant
    )