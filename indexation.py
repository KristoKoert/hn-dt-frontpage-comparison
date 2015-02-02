#!/usr/bin/python3

from datetime import datetime
from util import write_json
import json

INDEX_FILE_PATH = 'data/index.json'
BACKUP_INDEXES_PATH = 'data/index_backup.json'


def get_index():
    return json.load(open(INDEX_FILE_PATH, 'r'))


def get_index_backup():
    return json.load(open(BACKUP_INDEXES_PATH, 'r'))


def update_index(index):
    old_index = get_index()
    index_backup = get_index_backup()
    index_backup[str(datetime.now())] = old_index
    write_json(index, INDEX_FILE_PATH)
    write_json(index_backup, BACKUP_INDEXES_PATH)


def append_to_index(data):
    index_data = get_index()
    key = str(datetime.now())
    index_data[key] = data
    update_index(index_data)
