````markdown
# TermChat: A Smart Terminal AI Chatbot with Multi-LLM Support

A beautiful terminal-based AI chatbot using Python, the Rich library for UI formatting, and support for multiple LLM providers including Google Gemini, OpenRouter, OpenAI, Claude, Grok, DeepSeek, Qwen, and HuggingFace.

## Features

- 🤖 **Multi-LLM Provider Support** - Choose from 8+ different AI providers
- 🔑 **Easy API Management** - Add, switch, and delete API keys on-the-fly
- 🎨 **Beautiful Terminal UI** with colored boxes, markdown support, and interactive elements
- 🔧 **Rich Command System** with commands for chat management and API configuration
- 📝 **Rich Text Formatting** with support for code blocks, tables, and markdown features
- ⚡ **First-Run Setup** - Automatic configuration wizard on first launch

## Supported LLM Providers

1. **Google (Gemini)** - Google's Gemini Pro model
2. **OpenRouter** - Access to multiple models through OpenRouter
3. **OpenAI** - GPT-3.5, GPT-4, and other OpenAI models
4. **Anthropic (Claude)** - Claude 3 Sonnet and other Claude models
5. **xAI (Grok)** - Grok Beta from xAI
6. **DeepSeek** - DeepSeek Chat models
7. **Qwen** - Alibaba's Qwen models
8. **HuggingFace** - Access to various open-source models

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/termchat.git
   cd termchat
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the chatbot (first-time setup will guide you):
   ```bash
   python termchat.py
   ```

## First Time Setup

When you run TermChat for the first time, it will:

1. Show you a list of available LLM providers
2. Ask you to select your preferred provider
3. Prompt for your API key (input is hidden for security)
4. Ask for the model name (with default suggestion)
5. Create a `.env` file with your configuration
6. Start the chatbot with your chosen provider and model

## Usage

### Starting a Chat

```bash
python termchat.py
```

### Available Commands

#### Basic Commands
- `/help` - Show available commands
- `/exit` - Exit the chatbot
- `/clear` - Clear the chat history and screen
- `/joke` - Tell a random programming joke
- `/history` - Show your chat history

#### API Management Commands
- `/addapi` - Add a new LLM provider API key
- `/switch` - Switch between configured LLM providers
- `/deleteapi` - Delete a saved API key

### Managing Multiple API Keys

#### Adding a New API Key
```
/addapi
```
This will:
- Show available LLM providers
- Let you select a provider
- Prompt for the API key
- Ask for the model name (with default suggestion)
- Save the configuration
- Optionally switch to the new provider

#### Switching Providers
```
/switch
```
This will:
- Show your saved API keys with their models
- Let you select which one to use
- Switch the active provider and model

#### Deleting an API Key
```
/deleteapi
```
This will:
- Show your saved API keys with their models
- Let you select which one to delete
- Remove both the API key and model configuration

## Example Model Names

When adding an API key, you can specify custom model names:

- **Google Gemini**: `gemini-pro`, `gemini-pro-vision`
- **OpenRouter**: `openai/gpt-4o-mini:free`, `anthropic/claude-3.5-sonnet`, `google/gemini-pro`
- **OpenAI**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`
- **Anthropic**: `claude-3-sonnet-20240229`, `claude-3-opus-20240229`
- **xAI (Grok)**: `grok-beta`
- **DeepSeek**: `deepseek-chat`, `deepseek-coder`
- **Qwen**: `qwen-turbo`, `qwen-plus`, `qwen-max`
- **HuggingFace**: `mistralai/Mistral-7B-Instruct-v0.2`, `meta-llama/Llama-2-7b-chat-hf`

## Getting API Keys

- **Google Gemini**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- **OpenRouter**: [https://openrouter.ai/keys](https://openrouter.ai/keys)
- **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Anthropic**: [https://console.anthropic.com/](https://console.anthropic.com/)
- **xAI (Grok)**: [https://x.ai/](https://x.ai/)
- **DeepSeek**: [https://platform.deepseek.com/](https://platform.deepseek.com/)
- **Qwen**: [https://dashscope.console.aliyun.com/](https://dashscope.console.aliyun.com/)
- **HuggingFace**: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

## Requirements

- Python 3.7+
- API key for at least one supported LLM provider

## Project Structure

```
termchat/
├── termchat.py              # Main application
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (auto-created)
├── .env.example            # Example environment file
├── README.md               # This file
└── utils/
    ├── __init__.py
    ├── commands.py         # Command handlers
    ├── env_manager.py      # API key and provider management
    ├── openrouter.py       # Universal LLM client
    └── ui.py              # UI utilities
```

## Customization

You can customize the chatbot by:

1. Adding new commands in `utils/commands.py`
2. Modifying UI themes in `utils/ui.py`
3. Adding support for more LLM providers in `utils/env_manager.py` and `utils/openrouter.py`

## Troubleshooting

### "No active provider configured" Error
- Use `/addapi` to add an API key
- Use `/switch` to select an active provider

### API Connection Errors
- Check your internet connection
- Verify your API key is correct
- Check if the provider's service is available

### First Run Setup Failed
- Delete the `.env` file and run again
- Manually create a `.env` file using `.env.example` as reference

## License

MIT

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
````