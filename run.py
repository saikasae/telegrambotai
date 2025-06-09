"""Main entry point for the Telegram AI Bot."""

import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.telegram_ai_bot.admin import admin_router
from src.telegram_ai_bot.database.models import async_main
from src.telegram_ai_bot.user import user_router
from src.telegram_ai_bot.utils.description import set_default_description


async def on_startup():
    """Initialize database on bot startup."""
    await async_main()


async def main():
    """Start the Telegram bot."""
    load_dotenv()
    bot = Bot(
        token=os.getenv("TOKEN"),
        default=DefaultBotProperties(parse_mode="Markdown"),
    )
    dp = Dispatcher()
    dp.include_routers(user_router, admin_router)
    dp.startup.register(on_startup)
    await set_default_description(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped")
