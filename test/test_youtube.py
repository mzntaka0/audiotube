# -*- coding: utf-8 -*-
"""
"""
import unittest

import audiotube
from dotenv import load_dotenv
load_dotenv()


class TestYouTube(unittest.TestCase):

    def test_fetch_result_ids(self):
        youtube = audiotube.YouTube()
        results = youtube.search('python')
        print(results)
        assert isinstance(results, audiotube.objects.YouTubeAudios)
        assert isinstance(results[0], audiotube.objects.YouTubeAudio)


if __name__ == '__main__':
    unittest.main()
