"""User interaction handlers for the Telegram AI Bot."""

import base64
import os
import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from telegram_ai_bot import keyboards as kb
from telegram_ai_bot.database.requests import set_user
from telegram_ai_bot.generators import (
    code_generation,
    image_generation,
    image_recognition,
    search_with_mistral,
    text_generation,
)
from telegram_ai_bot.middleware.subscribe_middleware import CheckSubscribeMiddleware
from telegram_ai_bot.states import (
    CodeGeneration,
    ImageGeneration,
    ImageRecognition,
    TextGeneration,
    WebSearch,
)
from telegram_ai_bot.utils.trim_history import trim_history

# Настраиваем logger для модуля
logger = logging.getLogger(__name__)

user_router = Router(name="user")
user_router.message.middleware(CheckSubscribeMiddleware())
user_router.callback_query.middleware(CheckSubscribeMiddleware())
history = {}


@user_router.callback_query()
async def handle_subscription_callback(callback: CallbackQuery, state: FSMContext):
    """Handle subscription callback queries."""
    if callback.data == "subscribe":
        await set_user(callback.from_user.id)
        await callback.bot.send_message(
            text="Welcome! Choose an option from the menu.",
            reply_markup=kb.get_main_keyboard(),
            chat_id=callback.from_user.id,
        )
        await state.clear()


@user_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Handle the /start command."""
    await set_user(message.from_user.id)
    await message.answer(text="Welcome!", reply_markup=kb.get_main_keyboard())
    await state.clear()


@user_router.message(F.text == "Back to Menu")
async def back_to_menu(message: Message, state: FSMContext):
    """Return to the main menu."""
    await set_user(message.from_user.id)
    await message.answer(
        text="You are back in the menu!", reply_markup=kb.get_main_keyboard()
    )
    await state.clear()


@user_router.message(TextGeneration.wait)
@user_router.message(ImageGeneration.wait)
@user_router.message(CodeGeneration.wait)
@user_router.message(ImageRecognition.wait)
@user_router.message(WebSearch.wait)
async def handle_wait_state(message: Message):
    """Inform user to wait during processing."""
    await message.answer(text="Please wait, the bot is processing your request...")


@user_router.message(F.text == "Text Generation")
async def start_text_generation(message: Message, state: FSMContext):
    """Initiate text generation process."""
    await state.set_state(TextGeneration.text)
    await message.answer(
        text="Enter your prompt...", reply_markup=kb.get_back_to_menu_keyboard()
    )


@user_router.message(TextGeneration.text)
async def process_text_generation(message: Message, state: FSMContext):
    """Process text generation request with rate limiting."""
    current_time = datetime.now()
    data = await state.get_data()
    last_request_time = data.get("last_request_time")
    if last_request_time:
        last_request_time = datetime.fromisoformat(last_request_time)
        if current_time - last_request_time < timedelta(seconds=10):
            remaining_time = 10 - (current_time - last_request_time).total_seconds()
            await message.answer(
                f"Please wait {int(remaining_time)} seconds before the next request."
            )
            return
    send_message = await message.answer(
        "The bot is thinking, please wait a moment..."
    )
    await state.set_state(TextGeneration.wait)
    if message.from_user.id not in history:
        history[message.from_user.id] = []
    history[message.from_user.id].append({"role": "user", "content": message.text})
    history[message.from_user.id] = await trim_history(
        history[message.from_user.id], max_length=4096, max_messages=5
    )
    answer = await text_generation(history[message.from_user.id])
    if not answer:
        raise ValueError("Empty response from model")
    history[message.from_user.id].append({"role": "assistant", "content": answer})
    history[message.from_user.id] = await trim_history(
        history[message.from_user.id], max_length=4096, max_messages=5
    )
    await send_message.answer(answer)
    await state.update_data(last_request_time=current_time.isoformat())
    await state.set_state(TextGeneration.text)


@user_router.message(F.text == "Image Generation")
async def start_image_generation(message: Message, state: FSMContext):
    """Initiate image generation process."""
    await state.set_state(ImageGeneration.image)
    await message.answer(
        text="Enter your prompt...", reply_markup=kb.get_back_to_menu_keyboard()
    )


@user_router.message(ImageGeneration.image)
async def process_image_generation(message: Message, state: FSMContext):
    """Process image generation request with rate limiting."""
    current_time = datetime.now()
    data = await state.get_data()
    last_request_time = data.get("last_request_time")
    if last_request_time:
        last_request_time = datetime.fromisoformat(last_request_time)
        if current_time - last_request_time < timedelta(seconds=10):
            remaining_time = 10 - (current_time - last_request_time).total_seconds()
            await message.answer(
                f"Please wait {int(remaining_time)} seconds before the next request."
            )
            return
    send_message = await message.answer(
        "The bot is generating an image, please wait a moment..."
    )
    await state.set_state(ImageGeneration.wait)
    answer = await image_generation(message.text)
    image_bytes = base64.b64decode(answer)
    await send_message.answer_photo(
        photo=BufferedInputFile(file=image_bytes, filename="generated_image.jpg")
    )
    generated_images_dir = "generated_images"
    if os.path.exists(generated_images_dir):
        for distribution in os.listdir(generated_images_dir):
            file_path = os.path.join(generated_images_dir, distribution)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(generated_images_dir)
    await state.update_data(last_request_time=current_time.isoformat())
    await state.set_state(ImageGeneration.image)


@user_router.message(F.text == "Code Generation")
async def start_code_generation(message: Message, state: FSMContext):
    """Initiate code generation process."""
    await state.set_state(CodeGeneration.code)
    await message.answer(
        text="Enter your prompt...", reply_markup=kb.get_back_to_menu_keyboard()
    )


@user_router.message(CodeGeneration.code)
async def process_code_generation(message: Message, state: FSMContext):
    """Process code generation request with rate limiting."""
    current_time = datetime.now()
    data = await state.get_data()
    last_request_time = data.get("last_request_time")
    if last_request_time:
        last_request_time = datetime.fromisoformat(last_request_time)
        if current_time - last_request_time < timedelta(seconds=10):
            remaining_time = 10 - (current_time - last_request_time).total_seconds()
            await message.answer(
                f"Please wait {int(remaining_time)} seconds before the next request."
            )
            return
    send_message = await message.answer(
        "The bot is generating code, please wait a moment..."
    )
    await state.set_state(CodeGeneration.wait)
    if message.from_user.id not in history:
        history[message.from_user.id] = []
    history[message.from_user.id].append({"role": "user", "content": message.text})
    history[message.from_user.id] = await trim_history(
        history[message.from_user.id], max_length=4096, max_messages=5
    )
    answer = await code_generation(message.text)
    if not answer:
        raise ValueError("Empty response from model")
    history[message.from_user.id].append({"role": "assistant", "content": answer})
    history[message.from_user.id] = await trim_history(
        history[message.from_user.id], max_length=4096, max_messages=5
    )
    await send_message.answer(answer)
    await state.update_data(last_request_time=current_time.isoformat())
    await state.set_state(CodeGeneration.code)


@user_router.message(F.text == "Image Recognition")
async def start_image_recognition(message: Message, state: FSMContext):
    """Initiate image recognition process."""
    await state.set_state(ImageRecognition.vision)
    await message.answer(
        text="Enter your prompt or send an image...", reply_markup=kb.get_back_to_menu_keyboard()
    )


@user_router.message(ImageRecognition.vision, F.photo)
async def process_image_recognition(message: Message, state: FSMContext):
    """Process image recognition request with rate limiting."""
    current_time = datetime.now()
    data = await state.get_data()
    last_request_time = data.get("last_request_time")
    if last_request_time:
        last_request_time = datetime.fromisoformat(last_request_time)
        if current_time - last_request_time < timedelta(seconds=10):
            remaining_time = 10 - (current_time - last_request_time).total_seconds()
            await message.answer(f"Please wait {int(remaining_time)} seconds before the next request.")
            return
    processing_message = await message.answer("The bot is processing the image, please wait a moment...")
    try:
        await state.set_state(ImageRecognition.wait)
        os.makedirs("images", exist_ok=True)  # Создаём директорию, если она отсутствует
        photo = message.photo[-1]
        get_file = await message.bot.get_file(photo.file_id)
        photo_path = f"images/{photo.file_id}.jpg"
        await message.bot.download(get_file.file_id, destination=photo_path, timeout=90)
        caption = message.caption or "Describe this image in detail"
        answer = await image_recognition(photo_path, caption)
        if answer is None:
            await message.answer("Sorry, an error occurred while processing the image. Please try again.")
        else:
            await processing_message.edit_text(answer)
        await state.update_data(last_request_time=current_time.isoformat())
        await state.set_state(ImageRecognition.vision)
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        await message.answer("An error occurred. Please try again.")
    finally:
        if os.path.exists(photo_path):
            os.remove(photo_path)


@user_router.message(F.text == "Web Search (beta)")
async def start_web_search(message: Message, state: FSMContext):
    """Initiate web search process."""
    await state.set_state(WebSearch.internet)
    await message.answer(
        text="Enter your search query...", reply_markup=kb.get_back_to_menu_keyboard()
    )


@user_router.message(WebSearch.internet)
async def process_web_search(message: Message, state: FSMContext):
    """Process web search request with rate limiting."""
    current_time = datetime.now()
    data = await state.get_data()
    last_request_time = data.get("last_request_time")
    if last_request_time:
        last_request_time = datetime.fromisoformat(last_request_time)
        if current_time - last_request_time < timedelta(seconds=10):
            remaining_time = 10 - (current_time - last_request_time).total_seconds()
            await message.answer(f"Please wait {int(remaining_time)} seconds before the next request.")
            return
    send_message = await message.answer("The bot is searching the web, please wait a moment...")
    await state.set_state(WebSearch.wait)
    res = await search_with_mistral(message.text)
    await send_message.answer(res)
    await state.update_data(last_request_time=current_time.isoformat())
    await state.set_state(WebSearch.internet)
    