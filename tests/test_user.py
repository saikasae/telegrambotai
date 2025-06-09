"""Unit tests for user handlers."""

import pytest
from unittest.mock import AsyncMock

from telegram_ai_bot.user import user_router, start_command, start_text_generation
from telegram_ai_bot.states import TextGeneration


@pytest.mark.asyncio
async def test_start_command():
    """Test the /start command handler."""
    class MockMessage:
        async def answer(self, text, reply_markup):
            self.text = text
            self.reply_markup = reply_markup

        @property
        def from_user(self):
            return type("User", (), {"id": 123})()

    class MockState:
        async def clear(self):
            self.cleared = True

    message = MockMessage()
    state = MockState()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("telegram_ai_bot.user.set_user", AsyncMock())
        await user_router.message(lambda m: True)(start_command)(message, state)
    assert message.text == "Welcome!"
    assert state.cleared is True


@pytest.mark.asyncio
async def test_start_text_generation():
    """Test the text generation initiation handler."""
    class MockMessage:
        async def answer(self, text, reply_markup):
            self.text = text
            self.reply_markup = reply_markup

    class MockState:
        async def set_state(self, state):
            self.state = state

    message = MockMessage()
    state = MockState()
    await user_router.message(lambda m: m.text == "Text Generation")(
        start_text_generation
    )(message, state)
    assert message.text == "Enter your prompt..."
    assert state.state == TextGeneration.text
