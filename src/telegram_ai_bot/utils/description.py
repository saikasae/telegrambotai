"""Utility to set the bot's description."""

async def set_default_description(bot):
    """Set the default description for the Telegram bot."""
    await bot.set_my_description(
        """
🔥 ChatGPT Bot for All Your Needs!

✨ Features:

◼️ Generate unique texts
◼️ Create stunning images
◼️ Write code with explanations
◼️ Recognize and describe your photos
◼️ Search the web (beta)

◼️ Answer any question you have!

Press "START" to explore endless possibilities! ⬇️
        """
    )