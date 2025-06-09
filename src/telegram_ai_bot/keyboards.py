"""Keyboard builders for the Telegram AI Bot."""

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_main_keyboard():
    """Build the main menu keyboard."""
    builder = ReplyKeyboardBuilder()
    builder.button(text="Text Generation")
    builder.button(text="Image Generation")
    builder.button(text="Code Generation")
    builder.button(text="Image Recognition")
    builder.button(text="Web Search (beta)")
    builder.adjust(3, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def get_back_to_menu_keyboard():
    """Build a keyboard with a 'Back to Menu' button."""
    builder = ReplyKeyboardBuilder()
    builder.button(text="Back to Menu")
    return builder.as_markup(resize_keyboard=True)


def get_subscription_keyboard():
    """Build an inline keyboard for subscription prompts."""
    builder = InlineKeyboardBuilder()
    builder.button(text="Join Channel", url="https://t.me/dsfgdgdfgdfgsdfg")
    builder.button(text="✅ I Subscribed!", callback_data="subscribe")
    builder.adjust(1)
    return builder.as_markup()