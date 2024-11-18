from typing import TYPE_CHECKING

from telegram import Update
if TYPE_CHECKING:
    from ..theoremator_manager import TheorematorManager

class OperationSum:
    def __init__(self, bot_manager: "TheorematorManager"):
        self.bot_manager = bot_manager
    async def step_1(self, update: Update, **kwargs):
        pass
    