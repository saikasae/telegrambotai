"""Utility to trim conversation history."""

from typing import List, Dict, Any


async def trim_history(history: List[Dict[str, Any]], max_length: int = 4096, max_messages: int = 5) -> List[Dict[str, Any]]:
    """Trim conversation history to fit within length and message limits."""
    if not history:
        return []
    if len(history) > max_messages:
        history = history[-max_messages:]
    current_length = sum(len(str(message.get("content", ""))) for message in history)
    while history and current_length > max_length:
        if len(history) == 1:
            if current_length > max_length:
                history[0]["content"] = history[0]["content"][: max_length - 100] + "..."
            break
        removed_message = history.pop(0)
        current_length -= len(str(removed_message.get("content", "")))
    return history