# -*- coding: utf-8 -*-
from re import findall


def get_item(lst, idx, default=None):
    try:
        return lst[idx]
    except:
        return default


def extract_from(data, pattern, if_not_found='', encode=True):
    if data == None:
        data = ""
    match = findall(pattern, data)
    item = get_item(match, 0, if_not_found)
    return item.encode('utf-8') if encode else item
