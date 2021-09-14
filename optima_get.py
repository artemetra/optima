# -*- coding: utf-8 -*-
from typing import Dict, Tuple, Union, List

import requests
from bs4 import BeautifulSoup as Soup

import os
import sys
import traceback
import pathlib

import re

from utils import (print_and_exit as _exit, 
                    _time)

try:
    from header_config import header as raw_user_header
except ImportError as e:
    _exit(
        f"Failed to import header! Maybe you haven't renamed 'template_header_config.py' to 'header_config.py'?\nFull traceback:", 
        traceback=traceback.format_exc(), err = ImportError)


def check_if_logged_in(html: bytes) -> bool:
    result = Soup(html, features="lxml").find("div", class_="login-form-wrapper")
    return True if not result else False

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

def collect_pages(html: bytes) -> List:
    try:
        res_set = Soup(html, features='lxml').find("div", class_='menuwrapper').find_all("a")
    except Exception as e:
        print(f"No other pages were found in this lesson or your link is not a lesson.\n[Error: {e}]")
        return []
    
    urls = [res.get("href") for res in res_set]
    print(f"Found {len(urls)} pages! Writing each...")
    return urls

def write_to_html(contents: bytes, file: str, joining = '') -> None:
    contents = Soup(contents, features='lxml').find("div", role="main")
    
    with open(file, 'a', encoding='utf-8') as f:
        f.write(joining)
        content_repr = contents.__repr__()
        f.write(content_repr)
    print(f"Successfully written to \"{file}\": {len(content_repr)} chars. (Preview: {content_repr[:10]} (...) {content_repr[-10:]})")

def main(init_url: str, headers: dict, file: str, joining = '') -> None:
    init_html_content = requests.get(init_url, headers=headers).content
    if check_if_logged_in(init_html_content):
        write_to_html(init_html_content, file, joining)
        if urls := collect_pages(init_html_content):
            for url in urls:
                html_content = requests.get(url, headers=headers).content
                write_to_html(html_content, file, joining)

    else:
        _exit("Failed to log into the session. Your session cookie is either expired or invalid, retry with a new header", err = ValueError)

if __name__ == '__main__':
    
    dict_header = firefox_headers_to_dict(raw_user_header)
    main(dict_header[1], dict_header[0], f"ignore\\export at {_time()}.html")
