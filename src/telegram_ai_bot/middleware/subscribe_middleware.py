"""Middleware to check user subscription status."""

import os
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from telegram_ai_bot import keyboards


class CheckSubscribeMiddleware(BaseMiddleware):
    """Middleware to ensure users are subscribed to the Telegram channel."""

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        """Check subscription status before processing the event."""
        user = event.from_user
        group = os.getenv("GROUP")
        try:
            user_subscription_status = await event.bot.get_chat_member(
                chat_id=group, user_id=user.id
            )
            status = str(user_subscription_status).split()[0][8:-1]
            if status == "left":
                await event.answer(
                    "👋 Hello! Since our bot is free, we kindly ask you to subscribe to our channel. "
                    "You'll find lots of interesting content about AI!\n"
                    "After subscribing, press the corresponding button.",
                    reply_markup=keyboards.get_subscription_keyboard(),
                )
                return
            return await handler(event, data)
        except Exception as e:
            print(f"Error checking subscription: {e}")
            await event.answer("An error occurred! Please try again.")
            return