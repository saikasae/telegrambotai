"""Example usage of the Telegram AI Bot."""

import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.telegram_ai_bot.admin import admin_router
from src.telegram_ai_bot.database.models import async_main
from src.telegram_ai_bot.user import user_router
from src.telegram_ai_bot.utils.description import set_default_description


async def start_bot():
    """Start the Telegram bot with example configuration."""
    load_dotenv()
    bot = Bot(
        token=os.getenv("TOKEN"),
        default=DefaultBotProperties(parse_mode="Markdown"),
    )
    dp = Dispatcher()
    dp.include_routers(user_router, admin_router)
    dp.startup.register(async_main)
    await set_default_description(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
