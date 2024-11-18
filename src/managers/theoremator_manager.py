from typing import TYPE_CHECKING
from logging import Logger
from tg_bot_base import BotManager

if TYPE_CHECKING:
    from src.managers.global_user_data_manager import GlobalUserDataManager

class TheorematorManager(BotManager): # type: ignore
    def __init__(self) -> None:
        super().__init__()
        self.commands_collection = None
        self.logger: Logger | None = None
        from src.managers.user_data_manager import TheorematorUserDataManager
        self.user_data_manager: TheorematorUserDataManager = TheorematorUserDataManager(self)
        self.global_user_data: "GlobalUserDataManager" = None
        from src.managers.yookassa_manager import YookassaManager
        from src.config.access import yookassa_shop_id, yookassa_secret_key
        self.yookassa_manager = YookassaManager(yookassa_shop_id, yookassa_secret_key)
    def set_logger(self, logger: Logger) -> None:
        self.logger = logger
    def create_menus(self) -> None:
        from src.screen_declaration.main import main
        self.screen_manager.extend_screen(*main(self))
    def init_global_user_data(self, global_user_data: "GlobalUserDataManager"):
        self.global_user_data = global_user_data
        global_user_data.create_tables()