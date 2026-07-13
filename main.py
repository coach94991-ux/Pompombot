import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '8633686451:AAGjzV8OXtAmD625q_h2x613IV2swda5Z2M'
bot = telebot.TeleBot(BOT_TOKEN)

DEMO_VIDEO_URL = "https://t.me/+E465JANwfsYyMzNl"
ADMIN_CONTACT_URL = "https://t.me/PrimeTheRengoku"

@bot.message_handler(commands=['start'])
def send_welcome_post(message):
    try:
        with open("w.txt", "r", encoding="utf-8") as file:
            caption_text = file.read()
    except FileNotFoundError:
        caption_text = "Welcome to the bot!"

    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    premium_btn = InlineKeyboardButton(
        text="🔓 UNLOCK PREMIUM (₹70)",
        callback_data="send_fixed_qr"
    )
    demo_btn = InlineKeyboardButton(
        text="🎬 Demo video",
        url=DEMO_VIDEO_URL
    )
    contact_btn = InlineKeyboardButton(
        text="📞 Contact Admin",
        url=ADMIN_CONTACT_URL
    )

    markup.add(premium_btn, demo_btn, contact_btn)

    try:
        with open("w.jpg", "rb") as photo:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=caption_text,
                reply_markup=markup,
                parse_mode="Markdown"
            )
    except FileNotFoundError:
        bot.send_message(message.chat.id, caption_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "send_fixed_qr")
def handle_premium_payment(call):
    bot.answer_callback_query(call.id)

    try:
        with open("qr.jpg", "rb") as qr_photo:
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=qr_photo,
                caption="Please scan this QR code to complete your payment of ₹70. After payment, send the screenshot to the Admin using the Contact button above."
            )
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Error: qr.jpg file not found on the server.")


if __name__ == "__main__":
    print("Bot is successfully running...")
    bot.infinity_polling()
