# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
import os
import youtube_dl

def download(video_id, output_dir):
    base_url = 'https://www.youtube.com/watch?v='

    config = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192"
        }]
    }

    config['outtmpl'] = os.path.join(output_dir, '%(id)s.%(ext)s')
    youtube_link = base_url + video_id

    with youtube_dl.YoutubeDL(config) as ydl:
        ydl.download([youtube_link])

