# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
import glob
from pathlib import Path
import os
import youtube_dl
import urllib


# FIXME: ganna be duplicated.
class Download(object):

    def __init__(self):
        pass

    def run(self, video_ids: list, output_dir: Path = 'result'):
        if os.path.exists(output_dir):
            raise OSError(17)

    def download(self, video_id: str, output_dir: Path):
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

    def directory_init(self, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)

    #保存したmp3から字幕を取得
    def mp3totext(self, content_id: str):
        #英語の場合はhl=en
        url = 'http://video.google.com/timedtext?hl=en&lang=en&name=&v=' + content_id
        with urllib.request.urlopen(url) as response:
            XmlData = response.read()
        print(XmlData)
        root = ET.fromstring(XmlData)
        start = []
        dur = []
        txt = []
        for i, child in enumerate(root):
            start.append(child.get('start'))
            dur.append(child.get('dur'))
            txt.append(child.text)
        return start, dur, txt

    #字幕をテキストに出力
    def write_data(self, start, dur, txt, filename):
        print(filename)
        y, sr = librosa.load(filename, sr=44100)
        #basename = os.path.splitext(filename)[0]
        basename = os.path.splitext(os.path.split(filename)[1])[0]
        for i in range(len(start)):
            #テキストへの書き込み
            f = open('bigger_data/txt/' + basename+'_'+str(i)+'.txt', 'w')
            f.write(txt[i].replace('\n', '').replace(' ', ''))
            f.close()
            #音声の切り取り
            time_start = math.floor(float(start[i])*sr)
            time_end = time_start + math.floor(float(dur[i])*sr)
            snd = y[time_start:time_end]
            #TODO: ファイル名の長さが固定前提になってるのを可変にする
            librosa.output.write_wav('bigger_data/audio/' + basename + '_' + str(i) + '.wav', snd, sr=44100)

    def main(self, root):
        filenames = glob.glob(os.path.join(root, '*.wav'))
        print(filenames)

        for filename in filenames:
            #content_id = filename[-15:-4]
            content_id = os.path.splitext(os.path.split(filename)[1])[0]
            print(content_id)
            start, dur, txt = self.mp3totext(content_id)
            self.write_data(start, dur, txt, filename)


if __name__ == '__main__':
    download = Download()
    download.main('.')
