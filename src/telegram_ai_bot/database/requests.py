"""Database operations for the Telegram AI Bot."""

from sqlalchemy import select

from telegram_ai_bot.database.models import User, async_session


async def set_user(tg_id: int):
    """Add a new user to the database if they don't exist."""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_users():
    """Retrieve all users from the database."""
    async with async_session() as session:
        return await session.scalars(select(User))