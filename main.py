import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

AGE, GENDER, SYMPTOMS, DURATION, SEVERITY, SURVEY = range(6)

rule_based_db = {
    "سردرد": "ممکن است ناشی از خستگی یا کم‌آبی باشد. استراحت کنید و مایعات کافی بنوشید.",
    "تب": "ممکن است تب به علت عفونت ویروسی باشد. استراحت کنید و مایعات مصرف کنید.",
    "گلودرد": "ممکن است گلودرد شما ناشی از سرماخوردگی باشد. نوشیدنی‌های گرم مصرف کنید."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! به نویدمد خوش آمدید 😊\nسن شما چند سال است؟")
    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("جنسیت شما چیست؟")
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gender"] = update.message.text
    await update.message.reply_text("چه علائمی دارید؟")
    return SYMPTOMS

async def symptoms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["symptoms"] = update.message.text
    await update.message.reply_text("این علائم چند روز است ادامه دارد؟")
    return DURATION

async def duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["duration"] = update.message.text
    await update.message.reply_text("شدت علائم چقدر است؟ (کم / متوسط / شدید)")
    return SEVERITY

async def severity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["severity"] = update.message.text

    response = "🤖 تحلیل اولیه:\n"
    for symptom, advice in rule_based_db.items():
        if symptom in context.user_data["symptoms"]:
            response += f"✅ {advice}\n"
            response += "💊 پیشنهاد دارو: استامینوفن ۵۰۰ میلی‌گرم (در صورت نداشتن مشکل کبدی)\n"
            break
    else:
        response += "علائم شما نیاز به بررسی بیشتر دارد. با پزشک مشورت کنید.\n"

    await update.message.reply_text(response)
    await update.message.reply_text("آیا تجربه خوبی داشتید؟ (بله/خیر)")
    return SURVEY

async def survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ممنون از پاسخ شما! برای شروع دوباره /start را بزنید.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("فرآیند لغو شد. برای شروع دوباره /start را بزنید.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, symptoms)],
            DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, duration)],
            SEVERITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, severity)],
            SURVEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, survey)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
