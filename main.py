import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# مراحل مکالمه
AGE, GENDER, SYMPTOMS, DURATION, SEVERITY, SURVEY = range(6)

# دیتابیس ساده برای Rule-Based
rule_based_db = {
    "سردرد": "ممکن است ناشی از خستگی یا کم‌آبی باشد. استراحت کنید و مایعات کافی بنوشید.",
    "تب": "ممکن است تب به علت عفونت ویروسی باشد. استراحت کنید و مایعات مصرف کنید.",
    "گلودرد": "ممکن است گلودرد شما ناشی از سرماخوردگی باشد. نوشیدنی‌های گرم مصرف کنید."
}

# شروع مکالمه
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! به نویدمد خوش آمدید 😊\nبرای شروع، چند سؤال ساده می‌پرسم. سن شما چند سال است؟ (می‌توانید رد کنید)")
    return AGE

def age(update: Update, context: CallbackContext):
    context.user_data["age"] = update.message.text
    update.message.reply_text("جنسیت شما چیست؟ (می‌توانید رد کنید)")
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

    # تحلیل Rule-Based
    response = "🤖 تحلیل اولیه:\n"
    for symptom, advice in rule_based_db.items():
        if symptom in context.user_data["symptoms"]:
            response += f"✅ {advice}\n"
            response += "💊 پیشنهاد دارو: استامینوفن ۵۰۰ میلی‌گرم (در صورت نداشتن مشکل کبدی).\nℹ این فقط یک پیشنهاد عمومی است، انتخاب با شماست.\n"
            break
    else:
        response += "علائم شما نیاز به بررسی بیشتری دارد. اگر ادامه داشت، با پزشک مشورت کنید.\n"

    update.message.reply_text(response)
    update.message.reply_text("برای بهبود سرویس، چند سؤال کوتاه پاسخ دهید. آیا تجربه خوبی داشتید؟ (بله/خیر)")
    return SURVEY

def survey(update: Update, context: CallbackContext):
    context.user_data["survey1"] = update.message.text
    update.message.reply_text("آیا پاسخ‌ها برایتان مفید بود؟ (بله/خیر)")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("فرآیند لغو شد. برای شروع دوباره /start را بزنید.")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            GENDER: [MessageHandler(Filters.text & ~Filters.command, gender)],
            SYMPTOMS: [MessageHandler(Filters.text & ~Filters.command, symptoms)],
            DURATION: [MessageHandler(Filters.text & ~Filters.command, duration)],
            SEVERITY: [MessageHandler(Filters.text & ~Filters.command, severity)],
            SURVEY: [MessageHandler(Filters.text & ~Filters.command, survey)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
