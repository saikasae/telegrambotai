"""Unit tests for keyboard builders."""

from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup

from telegram_ai_bot.keyboards import get_main_keyboard, get_back_to_menu_keyboard, get_subscription_keyboard


def test_main_keyboard():
    """Test the main menu keyboard structure."""
    keyboard = get_main_keyboard()
    assert isinstance(keyboard, ReplyKeyboardMarkup)
    assert len(keyboard.keyboard) == 3
    assert keyboard.keyboard[0][0].text == "Text Generation"


def test_back_to_menu_keyboard():
    """Test the back to menu keyboard structure."""
    keyboard = get_back_to_menu_keyboard()
    assert isinstance(keyboard, ReplyKeyboardMarkup)
    assert len(keyboard.keyboard) == 1
    assert keyboard.keyboard[0][0].text == "Back to Menu"


def test_subscription_keyboard():
    """Test the subscription keyboard structure."""
    keyboard = get_subscription_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)
    assert len(keyboard.inline_keyboard) == 2
    assert keyboard.inline_keyboard[0][0].text == "Join Channel"