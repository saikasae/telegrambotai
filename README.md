# Telegram AI Bot

A Telegram bot powered by AI, providing text generation, image generation, code generation, image recognition, and web search capabilities.

## Features

- **Text Generation**: Generate human-like text responses.
- **Image Generation**: Create images based on textual prompts.
- **Code Generation**: Produce code snippets with explanations in Russian.
- **Image Recognition**: Analyze and describe images.
- **Web Search**: Perform internet searches and synthesize results (beta).
- **Admin Features**: Send broadcast messages to all users (admin-only).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/akirasae/telegrambotai.git
   cd telegram-ai-bot
   ```

2. Install dependencies:
   ```bash
   pip install .
   ```

3. Set up environment variables in a `.env` file:
   ```
   TOKEN=your_telegram_bot_token
   AITOKEN=your_mistral_api_key
   GROUP=your_telegram_channel_id
   ```

4. Run the bot:
   ```bash
   python run.py
   ```

## Running Tests

Tests are configured to run automatically with `tox`. To run tests manually:
```bash
tox
```

## Project Structure

- `src/telegram_ai_bot/`: Core application code.
- `tests/`: Unit, integration, and functional tests.
- `examples/`: Example scripts demonstrating bot usage.
- `run.py`: Entry point to start the bot.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

MIT License. See [LICENSE](LICENSE) for details.