# -*- coding: utf-8 -*-
"""
"""
import argparse
import codecs
import datetime
import glob
import json
import math
import os
import requests
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from urllib import request as urllib
from urllib.error import HTTPError

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import librosa

class Search(object):
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    def __init__(self, developer_key):
        self.youtube = self._load_youtube_object(developer_key)

    def get_all(self, keyword):
        nextPageToken = None 
        maxResults = 50  # 50 is maximum num restrected by api
        result_dict = {
                'videos': [],
                'channels': [],
                'playlist': []
                }
        while True:
            try:
                response = self.youtube.search().list(
                    q=keyword,
                    part="id,snippet",
                    pageToken=nextPageToken,
                    maxResults=maxResults
                ).execute()
                if not response['items']:
                    break
                nextPageToken = response['nextPageToken']
                for result in response.get("items", []):
                    result_key = result["id"]["kind"].split('#')[1]  # expect ['video', 'channel', 'playlist']
                    result_dict[result_key].append(result['id']['{}Id'.format(result_key)])
                    #if result["id"]["kind"] == "youtube#video":
                    #    videos.append([result["snippet"]["title"], result["id"]["videoId"]])
                    #elif result["id"]["kind"] == "youtube#channel":
                    #    channels.append([result["snippet"]["title"], result["id"]["channelId"]])
                    #elif result["id"]["kind"] == "youtube#playlist":
                    #    playlists.append([result["snippet"]["title"], result["id"]["playlistId"]])
            except KeyError:
                print('Additional request.')
                continue
        return result_dict

    # TODO: parse response dict for easily using.
    def from_keyword(self, keyword, pagetoken=None, max_results=50):
        response = self._search(keyword, pagetoken, max_results=maxResults)
        return response
    
    def _valid_key(self):
        pass

    def _load_youtube_object(self, developer_key):
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
            developerKey=developer_key)
        return youtube

    def _parse_response(self, response):
        videos = []
        channels = []
        playlists = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for result in response.get("items", []):
            if result["id"]["kind"] == "youtube#video":
                videos.append("%s (%s)" % (result["snippet"]["title"],
                                            result["id"]["videoId"]))
            elif result["id"]["kind"] == "youtube#channel":
                channels.append("%s (%s)" % (result["snippet"]["title"],
                                            result["id"]["channelId"]))
            elif result["id"]["kind"] == "youtube#playlist":
                playlists.append("%s (%s)" % (result["snippet"]["title"],
                                                result["id"]["playlistId"]))



    def _search(self, keyword, pagetoken, max_results=50):
        search_response = youtube.search().list(
            q=keyword,
            part="id,snippet",
            pageToken=pagetoken,
            maxResults=max_results
        ).execute()
        return search_response

    def _get_next_page_token(self):
        pass

    def _get_title(self):
        pass

    def _get_video_id(self):
        pass




if __name__ == '__main__':
    pass

