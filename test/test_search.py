# -*- coding: utf-8 -*-
"""
"""
import argparse
import os
import sys
import unittest

import audiotube


class TestSearch(unittest.TestCase):

    def test_fetch_result_ids(self):
        developer_key = os.getenv('DEVELOPER_KEY')
        search = audiotube.Search(developer_key)


if __name__ == '__main__':
    unittest.main()
