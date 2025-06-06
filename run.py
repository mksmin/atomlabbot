# import libraries
import asyncio
import logging

# import from libraries
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# import from modules
from app.handlers import admin_router, users_router
from app.database import db_helper
from config import get_id_chat_root, logger, settings
from config import BotNotification as bn


async def start() -> Bot:
    bot_token = settings.bot.token
    bot_class = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    return bot_class  # Возвращает объект 'Bot'


async def main(bot) -> None:
    """
    load token from .env
    register decorators with Dispatcher()
    create database
    delete updates from telegram servers
    start bot with token
    :return: None
    """
    dp = Dispatcher()
    dp.include_routers(admin_router, users_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)  # Пропускаем накопленные сообщения
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def on_startup() -> None:
    if bn.bot_start:
        root_user_id = await get_id_chat_root()
        await bot.send_message(chat_id=root_user_id, text="Бот запущен")
    return


async def on_shutdown() -> None:
    await db_helper.dispose()
    logger.info('db disposed')

    if bn.bot_start:
        root_user_id = await get_id_chat_root()
        await bot.send_message(chat_id=root_user_id, text="Бот останавливается")
    return

# Run tg_bot and start log
if __name__ == '__main__':
    FORMAT = '[%(asctime)s]  %(levelname)s: —— %(message)s'
    logging.basicConfig(level=logging.INFO,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format=FORMAT)
    try:
        bot = asyncio.run(start())
        asyncio.run(main(bot))
    except KeyboardInterrupt:
        logger.warning('Произошел KeyboardInterrupt')
