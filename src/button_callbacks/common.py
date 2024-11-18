from typing import TYPE_CHECKING, Any
from tg_bot_base import EvaluatedScreen, EvaluatedMenuDefault, EvaluatedMenuPhoto, ButtonRows, ButtonRow, Button
from tg_bot_base import FunctionCallbackData as FCD
# from tg_bot_base import StepBackCallbackData as SBCD
# from tg_bot_base import MenuCallbackData as MCD
from telegram import InputMediaPhoto, Update
if TYPE_CHECKING:
    from src.managers.theoremator_manager import TheorematorManager

async def leave(user_id: int, bot_manager: "TheorematorManager", update: Update, **kwargs) -> None:
    bot_manager.user_data_manager.get(user_id).after_input = None
    await bot_manager.user_screen_manager.step_back(user_id)
    
def generate_default_screen(text: str) -> EvaluatedScreen:
    return EvaluatedScreen(
        EvaluatedMenuDefault(
            text,
            ButtonRows(
                ButtonRow(
                    Button("Назад", FCD(leave))
                )
            )
        )
    )

def generate_input_error(error_message: str | None = None) -> EvaluatedScreen:
    text = "Неправильный ввод"
    if error_message is not None:
        text += " : " + error_message
    return EvaluatedScreen(
        EvaluatedMenuDefault(
            text,
            ButtonRows(
                ButtonRow(
                    Button("Назад", FCD(leave))
                )
            )
        )
    )

def list_to_button_rows(button_rows_as_list: list[list[list[str, Any]]] | None) -> ButtonRows:
    button_rows = ButtonRows()
    if button_rows_as_list is None:
        return button_rows
    for button_row_as_list in button_rows_as_list:
        button_row = ButtonRow()
        for button_as_list in button_row_as_list:
            button = Button(
                button_as_list[0],
                button_as_list[1]
            )
            button_row.append(button)
        button_rows.append(button_row)
    return button_rows

def list_to_evaluated_screen(screen_as_list: list[dict[str,Any]]) -> EvaluatedScreen:
    result = EvaluatedScreen()
    for menu_as_dict in screen_as_list:
        photo_bytes: bytes = menu_as_dict.get("photo")
        if photo_bytes:
            photo = InputMediaPhoto(photo_bytes)
            menu = EvaluatedMenuPhoto(photo)
        else:
            text = menu_as_dict.get("text")
            button_rows_as_list = menu_as_dict.get("reply_markup")
            button_rows = list_to_button_rows(button_rows_as_list)
            parse_mode = menu_as_dict.get("parse_mode")
            menu = EvaluatedMenuDefault(
                text=text,
                button_rows=button_rows,
                parse_mode=parse_mode
            )
        result.extend(menu)
    return result
