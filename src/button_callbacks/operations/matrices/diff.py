from typing import TYPE_CHECKING
from telegram import Message
from src.button_callbacks.operations.templates import \
    binary_operation_step_1, binary_operation_step_2, binary_operation_step_3
from libs.engine.engine import Matrix
if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager

async def operation_diff_step_1(user_id: int, bot_manager: "TheorematorManager", **kwargs) -> None:
    await binary_operation_step_1(
        user_id=user_id, 
        bot_manager=bot_manager, 
        next_operation=operation_diff_step_2)
    
async def operation_diff_step_2(message: Message, user_id: int, bot_manager: "TheorematorManager", **kwargs) -> None:
    await binary_operation_step_2(
        message=message,
        user_id=user_id, 
        bot_manager=bot_manager, 
        next_operation=operation_diff_step_3)
    
async def operation_diff_step_3(message: Message, user_id: int, bot_manager: "TheorematorManager", **kwargs) -> None:
    await binary_operation_step_3(
        message=message,
        user_id=user_id, 
        bot_manager=bot_manager,
        operation=Matrix.diff)
    