from typing import TYPE_CHECKING
from tg_bot_base import UserDataManager, UserData
if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager

class TheorematorUserData(UserData):
    def __init__(self, user_id: int):
        super().__init__(user_id)
        self.reset_operation_attributes()
    def reset_operation_attributes(self) -> None:
        from libs.engine.engine import Matrix
        self.operation_operand1: Matrix | None = None

class TheorematorUserDataManager(UserDataManager):
    def __init__(self, bot_manager: "TheorematorManager"):
        super().__init__(bot_manager)
        self.__users_data: dict[int, TheorematorUserData] = {}
    def get(self, user_id: int) -> TheorematorUserData:
        user_data = self.__users_data.get(user_id)
        if user_data is None:
            user_data = TheorematorUserData(user_id)
            self.set(user_id, user_data)
        return user_data
    def reset(self, user_id: int):
        self.set(user_id, TheorematorUserData(user_id))
    def set(self, user_id: int, user_data: TheorematorUserData) -> None:
        self.__users_data[user_id] = user_data