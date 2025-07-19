import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

AGE, GENDER, SYMPTOMS, DURATION, SEVERITY = range(5)

rule_based_db = {
    "سردرد": "ممکن است ناشی از خستگی یا کم‌آبی باشد. استراحت کنید و مایعات کافی بنوشید.",
    "تب": "ممکن است تب به علت عفونت ویروسی باشد. استراحت کنید و مایعات مصرف کنید.",
    "گلودرد": "ممکن است گلودرد شما ناشی از سرماخوردگی باشد. نوشیدنی‌های گرم مصرف کنید."
}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! به نویدمد خوش آمدید 😊\nسن شما چند سال است؟")
    return AGE

def age(update: Update, context: CallbackContext):
    context.user_data["age"] = update.message.text
    update.message.reply_text("جنسیت شما چیست؟")
    return GENDER

def gender(update: Update, context: CallbackContext):
    context.user_data["gender"] = update.message.text
    update.message.reply_text("چه علائمی دارید؟")
    return SYMPTOMS

def symptoms(update: Update, context: CallbackContext):
    context.user_data["symptoms"] = update.message.text
    update.message.reply_text("این علائم چند روز است ادامه دارد؟")
    return DURATION

def duration(update: Update, context: CallbackContext):
    context.user_data["duration"] = update.message.text
    update.message.reply_text("شدت علائم شما چقدر است؟ (کم / متوسط / شدید)")
    return SEVERITY

def severity(update: Update, context: CallbackContext):
    context.user_data["severity"] = update.message.text
    response = "🤖 تحلیل اولیه:\n"
    for symptom, advice in rule_based_db.items():
        if symptom in context.user_data["symptoms"]:
            response += f"✅ {advice}\n💊 پیشنهاد دارو: استامینوفن ۵۰۰ میلی‌گرم.\n"
            break
    else:
        response += "علائم شما نیاز به بررسی بیشتری دارد."
    update.message.reply_text(response)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("لغو شد.")
    return ConversationHandler.END

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

if __name__ == "__main__":
    dispatcher = Dispatcher(bot, None, workers=0)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            GENDER: [MessageHandler(Filters.text & ~Filters.command, gender)],
            SYMPTOMS: [MessageHandler(Filters.text & ~Filters.command, symptoms)],
            DURATION: [MessageHandler(Filters.text & ~Filters.command, duration)],
            SEVERITY: [MessageHandler(Filters.text & ~Filters.command, severity)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)

    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
