import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Rule-Based ساده
rule_based_db = {
    "سردرد": "ممکن است سردرد شما ناشی از خستگی یا کم‌آبی باشد. استراحت و آب کافی کمک می‌کند.",
    "تب": "ممکن است تب شما به علت عفونت ویروسی باشد. مایعات زیاد بنوشید.",
    "گلودرد": "ممکن است گلودرد شما ناشی از سرماخوردگی باشد. استراحت و مایعات گرم مصرف کنید."
}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("سلام! من دستیار پزشکی هستم. علائم خود را بنویسید:")

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text
    for symptom, advice in rule_based_db.items():
        if symptom in text:
            await message.answer(f"✅ {advice}\nℹ این فقط یک راهنمایی اولیه است.")
            return
    # Wizard Mode
    await message.answer("🤖 به نظر می‌رسد علائم شما نیاز به بررسی دارد. مراقب باشید و اگر بدتر شد، به پزشک مراجعه کنید.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
