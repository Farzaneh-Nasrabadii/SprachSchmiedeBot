cat > README.md << 'EOF'
# SprachSchmiedeBot 🇩🇪- German Language Learning Bot

A professional, multilingual Telegram bot for learning German language with rich curated resources.

## Features
- Multilingual interface (فارسی | English | Deutsch)
- Comprehensive learning resources (Audio, Video, Books, Tests, etc.)
- User progress tracking
- Premium features (planned)
- Scalable architecture (PostgreSQL + Redis + Async)

## Tech Stack
- Python 3.12
- python-telegram-bot v22
- SQLAlchemy + AsyncPG
- Redis
- Poetry
- Docker ready

## How to Run Locally
```bash
poetry shell
python -m bot.main
