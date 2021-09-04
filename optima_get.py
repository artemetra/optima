# -*- coding: utf-8 -*-
from typing import Dict, Tuple, Union

import requests
from bs4 import BeautifulSoup as Soup

import os
import sys
import traceback
import pathlib

import re

from datetime import datetime

from utils import (print_and_exit as _exit, 
                    _time)

try:
    from header_config import header as raw_user_header
except ImportError as e:
    _exit(
        f"ImportError: Failed to import header! Maybe you haven't renamed 'template_header_config.py' to 'header_config.py'?\nFull error message:", 
        traceback.format_exc())


def check_if_logged_in(html: bytes) -> bool:
    result = Soup(html, features="lxml").find("div", class_="loginerrors mt-3")
    if not result:
        return True
    else:
        return False

def firefox_headers_to_dict(raw_header: str) -> Union[Tuple[str, Dict], Dict]:
    try:
        raw_pairs = raw_header.strip().split('\n')
        pairs = raw_pairs[1:] # Removes the request
        header_dictionary = {pair.partition(':')[0].strip(): pair.partition(':')[2].strip() for pair in pairs}

        request = raw_pairs[0]
        if host := header_dictionary.get('Host'): 
            url = 'https://' + host + request.split()[1] # concats the host and the relational link to the page into a full url
            return (header_dictionary, url)
        else: 
            url = None
            return header_dictionary
    except Exception:
        _exit(f"Something went wrong while parsing user header data! Make sure you pasted it correctly.\nFull exception:\n",
        traceback.format_exc())



def write_to_html(contents: bytes, file: str, joining = '') -> None:
    with open(file, 'a', encoding='utf-8') as f:
        f.write(joining)
        f.write(contents.decode('utf-8'))
    print(f"Successfully written to \"{file}\": {len(contents)} bytes, {len(contents.decode('utf-8'))} chars.")

def main(url: str, headers: dict, file: str, joining = '') -> None:
    html_content = requests.get(url, headers=headers).content
    if check_if_logged_in(html_content):
        write_to_html(html_content, file, joining)
    else:
        print("Error: Failed to log into the session. Your session cookie might be either expired or invalid, retry with a new header")

if __name__ == '__main__':
    os.chdir(pathlib.Path().resolve())
    dict_header = firefox_headers_to_dict(raw_user_header)
    main(dict_header[1], dict_header[0], f"ignore\\export at {_time()}.html")
