import os
import telebot
from yt_dlp import YoutubeDL

# توكن البوت الخاص بك
TOKEN = '8809324669:AAFvR4kDBHP3HmSGDWaLrCleBjW8hlIY3q4'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ أهلاً بك في خدمة ProService IQ! البوت يعمل الآن من السيرفر السحابي المستقر 24/7. أرسل رابط الفيديو للتحميل.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        sent_msg = bot.reply_to(message, "⏳ جاري المعالجة والتحميل من السيرفر... انتظر قليلاً")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video_output.mp4',
                'quiet': True,
                'no_warnings': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video_output.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video, caption="تم التحميل بنجاح بواسطة ProService IQ ✅")
            
            os.remove('video_output.mp4')
            bot.delete_message(message.chat.id, sent_msg.message_id)
        except Exception:
            bot.edit_message_text("❌ حدث خطأ أثناء التحميل. تأكد من أن الرابط عام وصحيح.", message.chat.id, sent_msg.message_id)
    else:
        bot.reply_to(message, "يرجى إرسال رابط فيديو صحيح.")

if __name__ == "__main__":
    print("🚀 السيرفر استلم الكود والبوت يعمل الآن...")
    bot.polling(none_stop=True)
