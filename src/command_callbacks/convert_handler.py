from typing import TYPE_CHECKING, Callable, Coroutine

from telegram import Update
from telegram.ext import ContextTypes

if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager

def convert_handler(bot_manager: "TheorematorManager", extended_handler: \
        Callable[["TheorematorManager",Update, ContextTypes], Coroutine]
    ) -> Callable[[Update, ContextTypes], Coroutine]:
    """
Converts extended_handler to normal handler
"""
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await extended_handler(bot_manager, update, context)
    return handler