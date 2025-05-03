import yt_dlp
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

api_key = "7801225750:AAEqJnAvQgGI7pXXKemNkW3yp4qrdz1JOIU"
bot = telebot.TeleBot(api_key)

user_links = {}  # ذخیره لینک‌ها بر اساس chat_id

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "سلام! اول لینک ویدیوی یوتیوب را بفرست.")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()
    print(text)


    if "youtube.com" in text or "youtu.be" in text:
        user_links[chat_id] = {"url": text}
        bot.send_message(chat_id, "حالا کیفیت مورد نظر را وارد کن (مثلاً: 360)")
    elif text.isdigit() and chat_id in user_links:
        quality = int(text)
        url = user_links[chat_id]["url"]

        try:
            ydl_opts = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [])
            
            # فیلتر کردن فرمتی که هم صدا و تصویر دارد و کیفیت خواسته‌شده است
            selected = next((f for f in formats 
                             if f.get("height") == quality 
                             and f.get("acodec") != "none" 
                             and f.get("vcodec") != "none" 
                             and f.get("url")), None)

            if selected:
                link = info["url"]
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text="دانلود", url=link))
                bot.send_message(chat_id, f"لینک کیفیت {quality}p آماده است:", reply_markup=markup)
            else:
                bot.send_message(chat_id, "این کیفیت پیدا نشد.")

        except Exception as e:
            bot.send_message(chat_id, f"خطا: {e}")
    else:
        bot.send_message(chat_id, "لطفاً اول لینک ویدیو را بفرست، بعد کیفیت را.")

bot.polling()
