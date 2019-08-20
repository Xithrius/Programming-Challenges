import youtube_dl
import json
import sys


with open('config.json') as f:
    data = json.load(f)

ytdl = youtube_dl.YoutubeDL(data)
ytdl.extract_info(sys.argv[1], download=True)
