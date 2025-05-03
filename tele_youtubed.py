import yt_dlp
import telebot
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup
from keep_alive import keep_alive
keep_alive()


api_key = "7801225750:AAEqJnAvQgGI7pXXKemNkW3yp4qrdz1JOIU"

bot = telebot.TeleBot(api_key)

#button



@bot.message_handler(commands=["start"])
def wellcome(message):
    bot.reply_to(message, "wellcome to my telegram bot") 


@bot.message_handler()

def yt_downloder(message):
        url = message.text
  
        
        print(url)
        ydl_opts = {
        'quiet' : True ,
        'skip_download' : True, 
        'format' : 'best[height<=360]',
        'noplaylist' : True , 

        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            dirk_link = info['url']
            button1 = InlineKeyboardButton(text="download link" , url=dirk_link)
            send = InlineKeyboardMarkup(row_width=1)
            send.add(button1)
            bot.send_message(message.chat.id ,"youer link",reply_markup=send )
bot.polling()