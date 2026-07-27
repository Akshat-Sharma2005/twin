# Digital Twin

An AI-powered chatbot that acts as my digital twin — answering questions about my background, skills, and experience on my behalf. Built with a tool-calling agent loop, deployed live via Docker on Render.

**Live demo:** https://twin-h1wx.onrender.com

## What it does

Visitors can chat with an AI version of me to learn about my career, projects, and skills. The assistant:
- Answers questions using a custom system prompt built from my background
- Uses **function calling** to record visitor interest (name/email) or log any question it couldn't answer
- Pushes real-time notifications to my **Telegram** when either of those tools fires, so I never miss a lead or a knowledge gap in my own profile

## Tech stack

| Layer | Tool |
|---|---|
| LLM | `openai/gpt-oss-120b` via Groq API (OpenAI-compatible client) |
| UI | Gradio `ChatInterface` with custom CSS/JS theming |
| Tool calling | OpenAI function-calling schema, custom tool router |
| Notifications | Telegram Bot API |
| Deployment | Docker container on Render (free tier) |

## Architecture

```
User message
     │
     ▼
Gradio ChatInterface ──▶ Groq API (gpt-oss-120b)
     │                         │
     │                    tool_calls?
     │                         │
     │                 ┌───────┴────────┐
     │                 ▼                ▼
     │      record_user_details   record_unknown_question
     │                 │                │
     │                 └───────┬────────┘
     │                         ▼
     │                  Telegram push notification
     │                         │
     ◀─────────────── final response
```

## Running locally

```bash
git clone https://github.com/Akshat-Sharma2005/twin.git
cd twin
uv sync   # or: pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

```bash
python app.py
```

## Deployment

Deployed as a Docker container on [Render](https://render.com) (free tier). See `Dockerfile` for the build config. Environment variables are set via Render's dashboard rather than committed to the repo.

**Note:** the free tier spins down after 15 minutes of inactivity — the first request after idle can take 30–50 seconds to respond while the container wakes up.

## Project structure

```
twin/
├── app.py          # Gradio app + agent loop
├── context.py       # System prompt / background content
├── tools.py         # Function-calling tools + Telegram integration
├── styles.py         # Custom CSS/JS for the chat UI
├── Dockerfile
├── requirements.txt
└── .env              # (not committed — see .gitignore)
```
