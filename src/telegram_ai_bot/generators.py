"""AI generation functions for text, images, code, and web search."""

import base64
import logging
import os
from typing import List, Dict, Any

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from g4f.client import AsyncClient
from mistralai import Mistral

load_dotenv()
logger = logging.getLogger(__name__)


async def text_generation(messages: List[Dict[str, Any]]) -> str:
    """Generate text using the Mistral AI model."""
    api_key = os.getenv("AITOKEN")
    model = "mistral-large-2411"
    client = Mistral(api_key=api_key)
    response = await client.chat.stream_async(model=model, messages=messages)
    full_response = ""
    async for chunk in response:
        content = chunk.data.choices[0].delta.content
        if content is not None:
            full_response += content
    return full_response or "Error: Empty response from AI"


async def image_generation(prompt: str) -> str:
    """Generate an image based on a text prompt."""
    client = AsyncClient()
    api_key = os.getenv("AITOKEN")
    model = "mistral-large-2411"
    client_text = Mistral(api_key=api_key)
    response = await client_text.chat.stream_async(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Improve the prompt for the Flux neural network, which generates images, in English: {prompt}",
            },
        ],
    )
    full_response = ""
    async for chunk in response:
        content = chunk.data.choices[0].delta.content
        if content is not None:
            full_response += content
    response = await client.images.generate(
        model="flux", prompt=full_response, response_format="b64_json"
    )
    return response.data[0].b64_json


async def code_generation(prompt: str) -> str:
    """Generate code with explanations in Russian."""
    api_key = os.getenv("AITOKEN")
    model = "codestral-2405"
    client = Mistral(api_key=api_key)
    response = await client.chat.stream_async(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Provide explanations in Russian only. Here's the prompt: {prompt}",
            }
        ],
    )
    full_response = ""
    async for chunk in response:
        content = chunk.data.choices[0].delta.content
        if content is not None:
            full_response += content
    return full_response or "Error: Empty response from AI"


async def image_recognition(image_path: str, text: str) -> str:
    """Recognize and describe an image with a given text prompt."""
    image = encode_image_to_base64(image_path)
    api_key = os.getenv("AITOKEN")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "pixtral-large-2411",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image}"},
                ],
            },
        ],
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=data,
        )
        response.raise_for_status()
        result = response.json()
        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"]
        return "Error: Unable to get response from AI"


def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def search_with_mistral(query: str) -> str:
    """Perform a web search and synthesize results using Mistral AI."""
    api_key = os.getenv("AITOKEN")
    model = "mistral-large-2411"
    client = Mistral(api_key=api_key)
    response = await client.chat.stream_async(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Formulate the most effective and relevant web search query to answer the user's message: '{query}'. Return only the search query text.",
            },
        ],
    )
    web_search_text = ""
    async for chunk in response:
        content = chunk.data.choices[0].delta.content
        if content is not None:
            web_search_text += content
    searcher = DDGS()
    search_data = searcher.text(
        web_search_text, safesearch="off", max_results=3, region="ru-ru"
    )
    web_data = []
    async with httpx.AsyncClient() as client_http:
        for result in search_data:
            try:
                response_http = await client_http.get(result["href"], timeout=10)
                response_http.raise_for_status()
                soup = BeautifulSoup(response_http.text, "html.parser")
                paragraphs = soup.find_all("p")
                page_text = " ".join(p.text for p in paragraphs)
                web_data.append(f"Source: {result['href']}\nContent: {page_text[:550]}...")
            except Exception as e:
                logger.error(f"Error parsing {result['href']}: {e}")
                web_data.append(f"Unable to retrieve content from {result['href']}")
    response = await client.chat.stream_async(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Using only the information from the provided web pages, answer the user's question. Synthesize information from different sources to provide a complete and accurate response. Avoid speculation and do not add information not present in the provided pages. Web content:\n\n{' '.join(web_data)}\n\nUser question: {query}",
            },
            {"role": "user", "content": query},
        ],
    )
    full_response = ""
    async for chunk in response:
        content = chunk.data.choices[0].delta.content
        if content is not None:
            full_response += content
    return full_response or "Error: Empty response from AI"