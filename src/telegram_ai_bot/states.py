"""State definitions for the Telegram AI Bot."""

from aiogram.fsm.state import State, StatesGroup


class TextGeneration(StatesGroup):
    """States for text generation."""
    text = State()
    wait = State()


class ImageGeneration(StatesGroup):
    """States for image generation."""
    image = State()
    wait = State()


class CodeGeneration(StatesGroup):
    """States for code generation."""
    code = State()
    wait = State()


class ImageRecognition(StatesGroup):
    """States for image recognition."""
    vision = State()
    wait = State()


class WebSearch(StatesGroup):
    """States for web search."""
    internet = State()
    wait = State()


class Mailing(StatesGroup):
    """States for admin mailing."""
    message = State()