from pytube import YouTube
yt = YouTube('https://www.youtube.com/watch?v=NG1qcc8BqVg&list=PL-v_SkI4d8jvG_96vNpzB9-tN3rkLHA3O&index=12')
yt.streams.filter(only_audio=True).order_by("abr").first().download()

# Пример использования
