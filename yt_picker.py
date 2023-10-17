from pytube import YouTube, Playlist
import pytube.exceptions
from moviepy.editor import *
import os
import re
import threading

# Audio file downloading function
def file_downloading(yt: YouTube, folder_name: str = ""):
    # Finding the stream with best quality
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    # Making a path for temporary files
    try:
        # Loading audio stream to temporary file
        filename = audio_stream.download()
        # Converting temporary file to the .mp3 format
        audio = AudioFileClip(filename)
        # Making directory, if it doesn't exist
        if not os.path.exists(f'temp/{folder_name}'):
            os.makedirs(f'temp/{folder_name}')
        return audio
        # Deleting temporary file
        # os.remove(filename)
    except pytube.exceptions.AgeRestrictedError:
        print("Отмена: 18+ контент :(")
    except:
        print("Непредвиденная ошибка!")

# YouTube link checking function
def check_link(url = None):
    if url == None:
        print("Вы не указали ссылку!")
        return False
    elif re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$',url):
        return True
    elif re.match(r'^(https?\:\/\/)?(music\.youtube\.com)\/.+$', url):
        return True
    else:
        print('Ссылка неправильная!')
        return False

# Get link for direct run of this script
def get_link():
    while True:
        url = input("Вставьте ссылку на YouTube видео: ")
        if check_link(url):
            return url


# Функция для загрузки видео с YouTube и сохранения аудио в формате mp3
def download_audio(url):
    # Создаем объект YouTube из ссылки
    try:
        yt = YouTube(url)
    except pytube.exceptions.RegexMatchError:
        return "Не найдено видео по ссылке!"
    except:
        return "Непредвиденная ошибка!"
    # Проверяем длительность видео
    if yt.length > 1200:
        return "Извини, видео слишком длинное :(\nМаксимальная длительность - 20 минут."
    # Находим аудиодорожку с наилучшим качеством
    print(yt.streams)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    # Формируем путь для сохранения в директорию "music"
    output_path = os.path.join('temp', os.path.splitext(audio_stream.default_filename)[0] + ".mp3")
    # Проверяем, существует ли файл с таким же именем в папке "music"
    if os.path.exists(output_path):
        return output_path
    else:
        # Загружаем аудио во временный файл
        filename = audio_stream.download()
        # Конвертируем временный файл в mp3 формат
        audio = AudioFileClip(filename)
        # Создаем директорию "music", если ее нет
        if not os.path.exists('temp'):
            os.makedirs('temp')
        audio.write_audiofile(output_path)
        # Удаляем временный файл
        os.remove(filename)
        print(f"Аудио из видео {url} успешно загружено и сохранено в формате mp3")
    return f"Файл сохранен в: {output_path}"

def download_playlist(url, folder_name):
    try:
        p = Playlist(url)
    except pytube.exceptions.RegexMatchError:
        return "Не найден плейлист по ссылке!"
    except:
        return "Непредвиденная ошибка!"
    for yt in p.videos:
        # Находим аудиодорожку с наилучшим качеством
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        # Формируем путь для сохранения в директорию "music"
        output_path = os.path.join(f'../../OneDrive/Рабочий стол/Music/{folder_name}',
                                   os.path.splitext(audio_stream.default_filename)[0] + ".mp3")
        # Проверяем, существует ли файл с таким же именем в папке "music"
        if os.path.exists(output_path):
            print(f"Файл '{os.path.basename(output_path)}' уже существует в папке 'music'. Загрузка отменена.")
        else:
            thread = threading.Thread(target=file_downloading, args=(yt, folder_name))
            thread.start()

VARIANTS = (1, 2, 3, 4)
# Пример использования
if __name__ == '__main__':
    try:
        user_pick = int(input("1.Видео\n2.Аудио\n3.Плейлист (аудио)\n4.Плейлист (аудио)\nВыберите цифру (1-3):"))
    except ValueError:
        print("Вы ввели не цифру!")
        exit()
    except:
        print("Непредвиденная ошибка!")
        exit()
    if user_pick in VARIANTS:
        if user_pick == 1:
            pass
        elif user_pick == 2:
            url = get_link()
            print(download_audio(url))
        elif user_pick == 3:
            url = get_link()
            name_folder = input("Укажи название папки для плейлиста: ")
            print(download_playlist(url, name_folder))
        else:
            pass
    else:
        print("Нет такого варианта!")
