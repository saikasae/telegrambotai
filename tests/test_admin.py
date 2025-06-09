"""Unit tests for admin functionality."""

import pytest

from telegram_ai_bot.admin import AdminFilter, admin_router, start_mailing
from telegram_ai_bot.states import Mailing


@pytest.mark.asyncio
async def test_admin_filter():
    """Test the AdminFilter functionality."""
    class MockMessage:
        def __init__(self, user_id):
            self.from_user = type("User", (), {"id": user_id})()

    filter_instance = AdminFilter()
    assert await filter_instance(MockMessage(667393044)) is True
    assert await filter_instance(MockMessage(123456789)) is False


@pytest.mark.asyncio
async def test_start_mailing():
    """Test the start_mailing handler."""
    class MockMessage:
        async def answer(self, text):
            self.text = text

    class MockState:
        async def set_state(self, state):
            self.state = state

    message = MockMessage()
    state = MockState()
    await admin_router.message(AdminFilter(), lambda m: True)(start_mailing)(
        message, state
    )
    assert message.text == "Please enter the message to send..."
    assert state.state == Mailing.message
