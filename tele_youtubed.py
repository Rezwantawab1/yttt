import yt_dlp
import telebot
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup

api_key = "7801225750:AAEqJnAvQgGI7pXXKemNkW3yp4qrdz1JOIU"
bot = telebot.TeleBot(api_key)

user_links = {}

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "سلام! اول لینک یوتیوب را بفرست.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()
    print(text)
    

    # اگر متن شبیه لینک یوتیوب بود
    if "youtube.com" in text or "youtu.be" in text:
        try:
            ydl_opts = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=False)
                formats = info.get("formats", [])

            # ذخیره لینک و فرمت‌ها
            user_links[chat_id] = {
                "url": text,
                "formats": formats
            }

            bot.reply_to(message, "حالا کیفیت مورد نظر را وارد کن (مثلاً 360):")

        except Exception as e:
            bot.reply_to(message, f"خطا در گرفتن اطلاعات ویدیو: {e}")
    # اگر کاربر کیفیت وارد کرد
    elif text.isdigit() and chat_id in user_links:
        quality = int(text)
        formats = user_links[chat_id]["formats"]
        selected = next((f for f in formats if f.get("height") == quality and f.get("url")), None)

        if selected:
            link = selected["url"]
            button1 = InlineKeyboardButton(text="download link" , url=link)
            send = InlineKeyboardMarkup(row_width=1)
            send.add(button1)
            bot.send_message(chat_id, f"لینک ویدیو با کیفیت {quality}p" , reply_markup=send)
        else:
            bot.send_message(chat_id, "این کیفیت در دسترس نیست.")
    else:
        bot.reply_to(message, "اول لینک ویدیو را بفرست، بعد کیفیت را.")

bot.polling()
