# Telegram-AI
### Project with telegram bot which includes interaction with one of pretrained LLM models (from HuggingFace)
Ininitially, [facebook/blenderbot-400M-distill](https://huggingface.co/facebook/blenderbot-400M-distill) is used but it can be replaced with other LLMs. e. g.:
- [ai-forever/mGPT](https://huggingface.co/ai-forever/mGPT)

_For models above switch is provided in telegram bot functionality for each user_

### Project structure:
```
.
├── main.py
├── model.py
├── bot.py
├── logger.py
├── ...
```

**To launch this bot you need to specify `TELEGRAM_API_KEY` and `BOT_USERNAME` environments for correct work**
