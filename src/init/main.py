def main() -> None:
    from src.init.bot_manager import init_bot
    bot_manager = init_bot()
    from src.managers import log_manager
    log_manager.init_logging()
    bot_manager.message_manager.handle_message = log_manager.log_message_handler(
        bot_manager.message_manager.handle_message)
    bot_manager.screen_manager.handle_callback = log_manager.log_button_handler(
        bot_manager.callback_query_manager.callback_query_handler,
        bot_manager)
    bot_manager.set_logger(log_manager.logger)
    from src.init.application import init_application, run_application
    application = init_application()
    bot_manager.set_bot(application.bot)
    application.add_handlers(bot_manager.command_manager.get_all_handlers())

    # Callback Query
    application.add_handler(bot_manager.callback_query_manager.get_handler())

    # Messages
    application.add_handler(bot_manager.message_manager.get_handler())
    
    # Jobs
    from src.jobs.wrapper import JobWrapper
    job_wrapper = JobWrapper(bot_manager)
    from src.jobs.payment import job_payment_check
    job_payment_check_w = job_wrapper.wrap(job_payment_check)
    application.job_queue.run_repeating(
        job_payment_check_w, interval=7, first=1)
    from src.jobs.premium import job_premium_check
    job_premium_check_w = job_wrapper.wrap(job_premium_check)
    application.job_queue.run_repeating(
        job_premium_check_w, interval=7, first=1)
    
    run_application(application)