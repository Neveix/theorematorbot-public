from typing import TYPE_CHECKING
from tg_bot_base import Screen
if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager


def main(bot_manager: "TheorematorManager") -> list[Screen]:
    result: list[Screen] = []
    from src.screen_declaration.welcome import welcome
    result.append(welcome())
    from src.screen_declaration.matrices import matrices
    result.append(matrices())
    from src.screen_declaration.operators import operators
    result.append(operators())
    from src.screen_declaration.account import account, account_deposit, account_premium
    result.append(account())
    result.append(account_deposit())
    result.append(account_premium())
    return result