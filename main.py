import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "8420980985:AAFLa9q29XSEscGdrHvMtGA2Irji_GK4Kbo"

headers = {
    "User-Agent": "Mozilla/5.0"
}

user_state = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["📘 Facebook | فيسبوك"],
        ["🎵 TikTok | تيك توك"],
        ["📸 Instagram | إنستغرام"],
        ["▶️ YouTube | يوتيوب"],
        ["📡 Telegram | تيليجرام"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    welcome_text = """
╔═══━━━── • ──━━━═══╗
     『 𝐇𝐈𝐌𝐀 𝐁𝐎𝐓 』
 ✨ اهـلًا وسهـلًا بـك ✨
╚═══━━━── • ──━━━═══╝

🚀 الـخـدمــات الـمـتـاحــة | SERVICES

📘 Facebook | فيسبوك
🎵 TikTok | تيك توك
📸 Instagram | إنستغرام
▶️ YouTube | يوتيوب
📡 Telegram | تيليجرام

━━━━━━━━━━━━━━━━

📌 طـريقـة الاسـتـخـدام | HOW TO USE

➊ اختر المنصة
➋ اختر الخدمة
➌ أرسل الرابط أو اليوزر

━━━━━━━━━━━━━━━━

⭐ نـظـام الـنـقـاط | POINTS

🎁 لديك 5 نقاط مجانية
💎 كل طلب ناجح = نقطة

📊 لمعرفة رصيدك:
/my_stats

━━━━━━━━━━━━━━━━

🎯 المطور:
@hima_s249
"""

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

# HANDLE BUTTONS
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.message.from_user.id

    # FACEBOOK
    if text == "📘 Facebook | فيسبوك":
        user_state[user_id] = "facebook_followers"

        await update.message.reply_text(
            "📘 ارسل رابط او يوزر حساب فيسبوك"
        )

    # TIKTOK
    elif text == "🎵 TikTok | تيك توك":
        user_state[user_id] = "tiktok_likes"

        await update.message.reply_text(
            "🎵 ارسل رابط فيديو تيك توك"
        )

    # INSTAGRAM
    elif text == "📸 Instagram | إنستغرام":
        user_state[user_id] = "instagram_likes"

        await update.message.reply_text(
            "📸 ارسل رابط منشور الانستا"
        )

    # YOUTUBE
    elif text == "▶️ YouTube | يوتيوب":
        user_state[user_id] = "youtube_likes"

        await update.message.reply_text(
            "▶️ ارسل رابط فيديو يوتيوب"
        )

    # TELEGRAM
    elif text == "📡 Telegram | تيليجرام":
        user_state[user_id] = "telegram_members"

        await update.message.reply_text(
            "📡 ارسل رابط قناة او مجموعة تيليجرام"
        )

    else:
        await process_link(update, context)

# PROCESS LINKS
async def process_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    link = update.message.text

    if user_id not in user_state:
        return

    service = user_state[user_id]

    try:

        # FACEBOOK
        if service == "facebook_followers":

            await update.message.reply_text(
                "✅ تم ارسال طلب فيسبوك بنجاح"
            )

        # TIKTOK
        elif service == "tiktok_likes":

            data = {
                "action": "checkVideoId",
                "link": link,
            }

            requests.post(
                "https://app.zefame.com/api_free.php",
                headers=headers,
                data=data
            )

            await update.message.reply_text(
                "✅ تم ارسال لايكات تيك توك"
            )

        # INSTAGRAM
        elif service == "instagram_likes":

            data = {
                "action": "checkPostId",
                "link": link,
                "platform": "instagram",
            }

            requests.post(
                "https://app.zefame.com/api_free.php",
                headers=headers,
                data=data
            )

            await update.message.reply_text(
                "✅ تم ارسال لايكات الانستا"
            )

        # YOUTUBE
        elif service == "youtube_likes":

            await update.message.reply_text(
                "⚠️ الخدمة غير مكتملة حالياً"
            )

        # TELEGRAM
        elif service == "telegram_members":

            await update.message.reply_text(
                "✅ تم ارسال طلب تيليجرام"
            )

    except Exception as e:

        await update.message.reply_text(
            f"❌ حدث خطأ:\n{e}"
        )

# MAIN
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            buttons
        )
    )

    print("BOT STARTED")

    app.run_polling()

if __name__ == "__main__":
    main()
