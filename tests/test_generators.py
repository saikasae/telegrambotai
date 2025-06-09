"""Unit tests for AI generation functions."""

import pytest
from unittest.mock import AsyncMock, patch

from telegram_ai_bot.generators import text_generation, image_generation, code_generation, encode_image_to_base64


@pytest.mark.asyncio
async def test_text_generation():
    """Test text generation with mocked Mistral client."""
    with patch("telegram_ai_bot.generators.Mistral") as MockMistral:
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_chunk = type("Chunk", (), {"data": type("Data", (), {"choices": [type("Choice", (), {"delta": type("Delta", (), {"content": "Test response"})})]})})
        mock_response.__aiter__.return_value = [mock_chunk]
        mock_client.chat.stream_async.return_value = mock_response
        MockMistral.return_value = mock_client
        result = await text_generation([{"role": "user", "content": "Hello"}])
        assert result == "Test response"


@pytest.mark.asyncio
async def test_image_generation():
    """Test image generation with mocked clients."""
    with patch("telegram_ai_bot.generators.Mistral") as MockMistral, patch("telegram_ai_bot.generators.AsyncClient") as MockAsyncClient:
        mock_text_client = AsyncMock()
        mock_image_client = AsyncMock()
        mock_response_text = AsyncMock()
        mock_response_image = AsyncMock()
        mock_chunk = type("Chunk", (), {"data": type("Data", (), {"choices": [type("Choice", (), {"delta": type("Delta", (), {"content": "Improved prompt"})})]})})
        mock_response_text.__aiter__.return_value = [mock_chunk]
        mock_text_client.chat.stream_async.return_value = mock_response_text
        mock_response_image.data = [type("Data", (), {"b64_json": "base64string"})]
        mock_image_client.images.generate.return_value = mock_response_image
        MockMistral.return_value = mock_text_client
        MockAsyncClient.return_value = mock_image_client
        result = await image_generation("Create an image")
        assert result == "base64string"


@pytest.mark.asyncio
async def test_code_generation():
    """Test code generation with mocked Mistral client."""
    with patch("telegram_ai_bot.generators.Mistral") as MockMistral:
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_chunk = type("Chunk", (), {"data": type("Data", (), {"choices": [type("Choice", (), {"delta": type("Delta", (), {"content": "Code response"})})]})})
        mock_response.__aiter__.return_value = [mock_chunk]
        mock_client.chat.stream_async.return_value = mock_response
        MockMistral.return_value = mock_client
        result = await code_generation("Write a function")
        assert result == "Code response"


def test_encode_image_to_base64(tmp_path):
    """Test image to base64 encoding."""
    image_path = tmp_path / "test.jpg"
    image_path.write_bytes(b"fake image data")
    result = encode_image_to_base64(str(image_path))
    assert result == "ZmFrZSBpbWFnZSBkYXRh"