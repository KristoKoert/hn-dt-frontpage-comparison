#!/usr/bin/python3

from uuid import uuid4
from index import append_to_index
from util import download_html

URLS = ['http://news.ycombinator.com', 'http://www.datatau.com']


def collect_data():
    """Web page HTML is downloaded and stored in a file, index is updated."""
    data = {}
    for url in URLS:
        path = 'data/raw_html/' + str(uuid4()) + ".html"
        open(path, 'w+').write(download_html(url))
        data[url] = path
    append_to_index(data)


def run():
    collect_data()
