#!/usr/bin/python3

from urllib.request import urlopen
from functools import wraps
from time import time
from bs4 import BeautifulSoup
import json

DT_KEY = "DataTau"
HN_KEY = "HackerNews"
LOG_FILE_PATH = "log"


def log(info):
    open(LOG_FILE_PATH, 'a+').write(info)


def time_and_log(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time()
        result = f(*args, **kwds)
        elapsed = time() - start
        log("%s took %d time to finish \n" % (f.__name__, elapsed))
        return result
    return wrapper


def average(l):
    return sum(l) / len(l)


def download_html(url):
    raw_html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(raw_html)
    return soup.prettify()


def write_json(data, path):
    json.dump(data,
              open(path, 'w+'),
              sort_keys=True,
              indent=4,
              separators=(',', ': '))
