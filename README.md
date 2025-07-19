# NavidMed Telegram Bot
این پروژه شامل یک ربات تلگرام برای مشاوره ساده پزشکی است.

## نحوه اجرای رایگان در Render:
- Web Service ایجاد کنید.
- Build Command:
pip install -r requirements.txt
- Start Command:
gunicorn web:app & python main.py
- Environment Variable:
TELEGRAM_BOT_TOKEN = [توکن شما]
