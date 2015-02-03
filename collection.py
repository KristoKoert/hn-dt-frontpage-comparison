#!/usr/bin/python3

from uuid import uuid4
from indexation import append_to_index
from util import download_html, time_and_log

URLS = {
    'hn': 'http://news.ycombinator.com',
    'dt': 'http://www.datatau.com'
}


@time_and_log
def download_frontpages():
    """Downloads current frontpages

    :returns: The html files in a dict
    :rtype: dict

    """
    return {
        'hn': download_html(URLS['hn']),
        'dt': download_html(URLS['dt'])
    }


def store_frontpages(frontpages):
    """Stores the frontpage and return the paths to the files.

    :param html_files:  A front page fo either HN or DT
    :returns: Paths to the files
    :rtype: str

    """
    hn_path = 'data/raw_html/' + str(uuid4()) + ".html"
    dt_path = 'data/raw_html/' + str(uuid4()) + ".html"
    with open(hn_path, "w+") as hn_file, open(dt_path, 'w+') as dt_file:
        hn_file.write(frontpages['hn'])
        dt_file.write(frontpages['dt'])
    return {
        URLS['hn']: hn_path,
        URLS['dt']: dt_path
    }


def run():
    append_to_index(store_frontpages(download_frontpages()))
