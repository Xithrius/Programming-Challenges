import youtube_dl
import sys


data = {
    "format": "bestaudio/best",
    "outtmpl": "output/%(title)s.mp3",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": False,
    "no_warnings": False,
    "default_search": "auto",
    "source_address": "0.0.0.0"
}

ytdl = youtube_dl.YoutubeDL(data)
ytdl.extract_info(sys.argv[1], download=True)
