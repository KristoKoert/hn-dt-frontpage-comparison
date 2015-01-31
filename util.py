#!/usr/bin/python3

from urllib.request import urlopen
import json

INDEX_FILE_PATH = 'data/index.json'
BACKUP_INDEXES_PATH = 'data/index_backup.json'
DT_KEY = "DataTau"
HN_KEY = "HackerNews"


def average(l):
    return sum(l) / len(l)


def download_html(url):
    return urlopen(url).read().decode('utf-8')


def write_json(data, path):
    json.dump(data,
              open(path, 'w+'),
              sort_keys=True,
              indent=4,
              separators=(',', ': '))
