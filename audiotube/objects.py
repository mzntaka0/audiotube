# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals

import os
import tempfile

import youtube_dl
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi


# TODO: make both type of video and audio, creating abstract class as well
class YouTubeAudio:
    config = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192"
        }]
    }

    def __init__(self, url: str = None, dl: bool = False):
        self.dl = dl
        self._url = url
        self._id = self._parse_id()
        self.tmpfile = tempfile.NamedTemporaryFile(dir='/tmp/')
        self._transcription = None
        self._object = None

    def _parse_id(self):
        _id = self._url.split('watch?v=')[1]
        return _id

    def fetch_transcription(self):
        try:
            transcripted = YouTubeTranscriptApi.get_transcript(self.id)
        except youtube_transcript_api._api.YouTubeTranscriptApi.CouldNotRetrieveTranscript:
            return None
        return transcripted

    @property
    def url(self):
        return self._url

    @property
    def transcription(self):
        if not self._transcription:
            self._transcription = self.fetch_transcription()
        return self._transcription

    @property
    def id(self):
        return self._id

    @property
    def object(self):
        if not self._object:
            self._object = self.download()
        return self._object

    def __repr__(self):
        return '<Object: YouTubeAudio, url: {}>'.format(self._url)

    def __del__(self):
        if self._object:
            self.cleanup()

    def __enter__(self):
        if not self._object:
            self._object = self.download()
        return self._object

    def __exit__(self):
        self.cleanup()

    def cleanup(self):
        os.remove(self._object)

    def download(self):
        output_name = self.tmpfile.name + '-{}.{}'.format(self._id, self.config['postprocessors'][0]['preferredcodec'])
        self.config['outtmpl'] = output_name
        with youtube_dl.YoutubeDL(self.config) as ydl:
            ydl.download([self._url])
        return output_name

    def save(self, savedir: str = None):
        pass


class YouTubeAudios:

    def __init__(self, dl: bool = False):
        self.videos = list()
        self._counter = 0

    def __repr__(self):
        return '[<YouTube Videos> Num: {} {}'.format(len(self.videos), self.videos)

    def __getitem__(self, video_num: int):
        if not 0 <= video_num <= len(self.videos):
            raise IndexError('Index out of length. Maximum index: {}'.format(len(self.videos) - 1))
        return self.videos[video_num]

    def __len__(self):
        return len(self.videos)

    def __iter__(self):
        return self

    def __next__(self):
        if self._counter >= len(self.videos):
            self._counter = 0
            raise StopIteration()
        video = self.videos[self._counter]
        self._counter += 1
        return video

    def append(self, video: YouTubeAudio):
        self.videos.append(video)

    def append_from_url(self, url: str):
        self.videos.append(YouTubeAudio(url))

    # TODO: should yield as a generator
    def append_from_urls(self, urls: list):
        for url in urls:
            self.append(YouTubeAudio(url))
        return self
