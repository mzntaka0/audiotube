# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals

from typing import List

from bs4 import BeautifulSoup
from urllib.request import urlopen

from audiotube.objects import YouTubeAudios


class YouTube:

    @staticmethod
    def search(search_term: str, search_num: int = 50, return_url: bool = False) -> List[str]:
        search_term = search_term.replace(" ", '+')
        urls = YouTube.collect_urls(search_term, search_num)

        if not return_url:
            youtube_audios = YouTubeAudios()
            urls = youtube_audios.append_from_urls(urls)
        return urls

    @staticmethod
    def collect_urls(search_term: str, search_num: int = 50):
        urls = list()
        page = 1
        while len(urls) < search_num:
            urls.extend(YouTube.raw_search(search_term, page))
            page += 1
        return urls[:search_num]

    @staticmethod
    def raw_search(search_term: str, page: int = 1):
        url = "https://www.youtube.com/results?search_query={}&page={}".format(search_term, page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        vids = soup.findAll(attrs={'class': 'yt-uix-tile-link'})
        urls = ['https://www.youtube.com{}'.format(vid['href']) for vid in vids]
        return YouTube.result_perser(urls)

    @staticmethod
    def result_perser(urls):
        filter_terms = ['googlead', 'start_radio', 'channel']
        for term in filter_terms:
            urls = filter(YouTube.url_filter(term), urls)
        return list(urls)

    @staticmethod
    def url_filter(term):
        return lambda url: term not in url

    @staticmethod
    def urls2id(urls):
        erase_part = "https://www.youtube.com/watch?v="
        return list(map(lambda url: url.replace(erase_part, ""), urls))


if __name__ == '__main__':
    youtube = YouTube()
    results = youtube.search('python')
    print(results)
    print(results[3])
    for result in results:
        print(result.transcription)
