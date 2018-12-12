# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
import argparse
import os
import sys
import json
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

    #config['outtmpl'] = 'data/audio/%(title)s.%(ext)s'
    config['outtmpl'] = os.path.join(output_dir, '%(id)s.%(ext)s')
    youtube_link = base_url + video_id

    with youtube_dl.YoutubeDL(config) as ydl:
        ydl.download([youtube_link])


if __name__ == '__main__':
    pass
