from telegram.ext import Application

def init_application() -> Application:
    from src.config.access import bot_token
    return Application.builder().token(bot_token).build()
    

def run_application(application: Application) -> None:
    # job_queue = application.job_queue
    # Commands

    # Errors
    # application.add_error_handler(error)

    print("Запрашивание...")

    application.run_polling(poll_interval=0.1)