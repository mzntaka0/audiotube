# -*- coding: utf-8 -*-
"""
"""
import json
from logging import getLogger, StreamHandler, Formatter, INFO
import xml.etree.ElementTree as ET
from urllib import request as urllib

from googleapiclient.discovery import build
from tqdm import tqdm

logger = getLogger(__name__)
logger.setLevel(INFO)
handler = StreamHandler()
handler_format = Formatter('[%(asctime)s] - %(message)s')
handler.setFormatter(handler_format)
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)


# FIXME ganna be duplicated.
class Search(object):
    """
    Search class for YouTube

    Args:
        * developer_key (string): developer key to access Google YouTube API(v3)
        * caption_mode (string): select mode for caption type. ['standard', 'ASR', 'both']
                - standard -> handmade caption
                - ASR -> captioned by ASR(Auto Speech Recognition)
                - both -> get both standard and ASR

    Usage:
    >>> search = audiotube.Search(developer_key)
    >>> result = search.run('keyword for search e.g. political speech')
    """
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    caption_mode = ['standard', 'ASR', 'both']  # need 'both'?

    def __init__(self, developer_key, caption_mode='standard'):
        self.youtube = self._load_youtube_object(developer_key)
        self.caption_mode = caption_mode
        self.DEVELOPER_KEY = developer_key  # XXX: It's not so secure.

    def run(self, keyword):
        results_dict = self.fetch_result_ids(keyword)
        desired_ids = self.select_desired_captions(results_dict['video'])
        logger.info('Done to select. [Num] caption_id: {}, caption_id/video_id ratio: {:.1f} %'
                .format(len(desired_ids), len(desired_ids) * 100 / float(len(results_dict['video'])))
                )
        return desired_ids

    def fetch_result_ids(self, keyword):
        nextPageToken = None 
        maxResults = 50  # 50 is maximum num restrected by api
        results_dict = {
                'video': [],
                'channel': [],
                'playlist': []
                }
        logger.info('Start downloading keyword matched videos..')
        while True:
            try:
                response = self.from_keyword(keyword, nextPageToken, maxResults)

                if not response['items']:  # TODO: is there the status that never match this condition? have to check.
                    break
                nextPageToken = response['nextPageToken']
                for result in response.get("items", []):
                    result_key = result["id"]["kind"].split('#')[1]  # expect ['video', 'channel', 'playlist']
                    results_dict[result_key].append(result['id']['{}Id'.format(result_key)])
            except KeyError:  # to request over 500. this is a kind of tricky.
                logger.info('Additional request.')
                continue
        logger.info('Done downloading.. [Num] video_id: {}, channel_id: {}, playlist_id: {}'
                .format(*[len(results_dict[key]) for key in ['video', 'channel', 'playlist']]))
        return results_dict

    def _search(self, keyword, pagetoken, max_results=50):
        response = self.youtube.search().list(
            q=keyword,
            part="id,snippet",
            pageToken=pagetoken,
            maxResults=max_results
        ).execute()
        return response

    def select_desired_captions(self, video_ids):
        accepted_video_ids = list()
        logger.info('Start selecting video_id which made by {}. It may take time..'.format(self.caption_mode))
        for video_id in tqdm(video_ids):
            request = urllib.urlopen(
                "https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=" + video_id + "&key=" + self.DEVELOPER_KEY)
            response = request.read()
            data = json.loads(response)
            for item in data["items"]:
                lang = item["snippet"]["language"]
                trackKind = item["snippet"]["trackKind"]  # "standard" -> manual, "ASR" -> auto
                if lang == "ja" and trackKind == "standard":  # FIXME: need to change to caption_mode
                    caption_id = item["id"]
                    accepted_video_ids.append(video_id)
        return accepted_video_ids

    # TODO: parse response dict for easily using.
    def from_keyword(self, keyword, pagetoken=None, max_results=50):
        response = self._search(keyword, pagetoken, max_results=max_results)
        return response

    def _load_youtube_object(self, developer_key):
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=developer_key)
        return youtube


if __name__ == '__main__':
    devkey = 'AIzaSyCmYPi1rwlPB-imJbRr3b7iGCod1Xx22Ic'
    search = Search(devkey, caption_mode='ASR')
    search.select_desired_captions(['nbJ-2G2GXL0'])
