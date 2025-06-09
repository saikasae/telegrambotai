"""Admin functionality for the Telegram AI Bot."""

from aiogram import Router
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram_ai_bot.database.requests import get_users
from telegram_ai_bot.states import Mailing

admin_router = Router(name="admin")


class AdminFilter(Filter):
    """Filter to check if the user is an admin."""

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [667393044]


@admin_router.message(AdminFilter(), Command("mailing"))
async def start_mailing(message: Message, state: FSMContext):
    """Initiate a mailing process for admins."""
    await state.set_state(Mailing.message)
    await message.answer("Please enter the message to send...")


@admin_router.message(Mailing.message)
async def send_mailing_message(message: Message, state: FSMContext):
    """Send the mailing message to all users and clear the state."""
    await state.clear()
    await message.answer("Mailing started")
    users = await get_users()
    for user in users:
        try:
            await message.send_copy(chat_id=user.tg_id)
        except Exception as e:
            print(f"Error sending message to {user.tg_id}: {e}")
    await message.answer("Mailing completed")