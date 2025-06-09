"""Unit tests for database operations."""

import pytest
from sqlalchemy import select

from telegram_ai_bot.database.models import User, async_session
from telegram_ai_bot.database.requests import set_user, get_users


@pytest.mark.asyncio
async def test_set_user():
    """Test adding a new user to the database."""
    async with async_session() as session:
        await set_user(123456)
        user = await session.scalar(select(User).where(User.tg_id == 123456))
        assert user.tg_id == 123456


@pytest.mark.asyncio
async def test_get_users():
    """Test retrieving all users from the database."""
    async with async_session() as session:
        session.add(User(tg_id=123456))
        await session.commit()
    users = await get_users()
    assert any(user.tg_id == 123456 for user in users)