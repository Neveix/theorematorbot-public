
from typing import Any, Callable
from telegram.ext import CallbackContext, ContextTypes
from src.managers.theoremator_manager import TheorematorManager


class JobWrapper:
    def __init__(self, bot_manager: TheorematorManager):
        self.bot_manager = bot_manager
    def wrap(
        self, 
        function: Callable[[TheorematorManager, CallbackContext], Any]
    ) -> Callable[[CallbackContext], Any]:
        async def wrapped_function(context: ContextTypes.DEFAULT_TYPE) -> None:
            await function(self.bot_manager, context)
        return wrapped_function