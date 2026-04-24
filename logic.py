from pytube import YouTube
import os
import re

def sanitize_filename(filename):
    """Очищает имя файла от недопустимых символов"""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    if len(filename) > 100:
        filename = filename[:100]
    return filename

def download_audio(url, output_path):
    """
    Скачивает аудио с YouTube и сохраняет в MP3
    
    Args:
        url (str): Ссылка на YouTube видео
        output_path (str): Путь для сохранения файла
    
    Returns:
        tuple: (success, result) - success булево значение, result сообщение или данные
    """
    try:
        yt = YouTube(url, on_progress_callback=None)
        
        video_info = {
            'title': yt.title,
            'author': yt.author,
            'length': yt.length,
            'views': yt.views
        }
        
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if not audio_stream:
            return False, "Не удалось найти аудиопоток для этого видео"
        
        print(f"Скачиваю: {yt.title}")
        downloaded_file = audio_stream.download(filename=output_path)
        
        if not output_path.endswith('.mp3'):
            mp3_path = output_path.rsplit('.', 1)[0] + '.mp3'
            os.rename(downloaded_file, mp3_path)
            output_path = mp3_path
        
        print(f"Скачивание завершено: {output_path}")
        return True, video_info
        
    except Exception as e:
        error_message = str(e)
        if "age" in error_message.lower():
            return False, "Видео имеет возрастное ограничение и не может быть скачано"
        elif "private" in error_message.lower():
            return False, "Это видео является приватным"
        elif "removed" in error_message.lower():
            return False, "Видео было удалено"
        else:
            return False, f"Ошибка при скачивании: {error_message}"

def get_video_info(url):
    """
    Получает информацию о видео без скачивания
    
    Args:
        url (str): Ссылка на YouTube видео
    
    Returns:
        dict: Информация о видео
    """
    try:
        yt = YouTube(url)
        return {
            'success': True,
            'title': yt.title,
            'author': yt.author,
            'length': yt.length,
            'views': yt.views,
            'description': yt.description[:200]  # Ограничиваем длину описания
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }