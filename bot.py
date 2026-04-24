import os
import telebot
from logic import download_audio
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 
                    "Приветттт!>-< Я музыкальный бот!\n\n"
                    "Отправь мне ссылку на YouTube видео, и я скачаю аудио в формате mp<3.\n\n"
                    "Команды:\n"
                    "/start - Запустить бота\n"
                    "/help - Помощь\n")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, 
                    "Как пользоваться:\n\n"
                    "1. Скопируй ссылочку на ютубчике\n"
                    "2. Отправь ссылку мне\n"
                    "3. Я скачаю аудио и отправлю тебе файл\n\n")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    
    if 'youtube.com' in url or 'youtu.be' in url:
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            
            status_msg = bot.send_message(message.chat.id, "Качаем...")
            
            # Генерируем уникальное имя файла
            import hashlib
            file_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            output_path = f"audio_{file_hash}.mp3"
            
            success, result = download_audio(url, output_path)
            
            if success:
                bot.edit_message_text("Отправляеммм...", 
                                    message.chat.id, 
                                    status_msg.message_id)
                
                with open(output_path, 'rb') as audio_file:
                    bot.send_audio(
                        message.chat.id, 
                        audio_file,
                        title=result.get('title', 'Аудио'),
                        performer=result.get('author', 'YouTube'),
                        duration=result.get('length', 0)
                    )
                
                os.remove(output_path)
                
                bot.delete_message(message.chat.id, status_msg.message_id)
                
                bot.send_message(message.chat.id, "Вуаля!!^o^")
            else:
                bot.edit_message_text(f"Ойййч {result}", 
                                    message.chat.id, 
                                    status_msg.message_id)
                
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибочка?? {str(e)}")
    else:
        bot.send_message(message.chat.id, 
                        "Пожалуйста, отправь ссылку на YouTube видео.\n"
                        "Пример: https://youtube.com/watch?v=VIDEO_ID")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    pass

if __name__ == "__main__":
    print("Я готов, босс")
    bot.polling(none_stop=True)