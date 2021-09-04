# -*- coding: utf-8 -*-
from typing import Dict, Tuple, Union
import requests
import os
import pathlib
from bs4 import BeautifulSoup as Soup
import re
import sys
import traceback

try:
    from header_config import header as user_header
except ImportError as e:
    print(f"ImportError: Failed to import header! Maybe you haven't renamed 'template_header_config.py' to 'header_config.py'?\nFull error message: {e}")
    sys.exit(-1)


def firefox_headers_to_dict(raw_header: str) -> Union[Tuple[str, Dict], Dict]:
    try:
        raw_pairs = raw_header.strip().split('\n')
        pairs = raw_pairs[1:] # Removes the request
        header_dictionary = {pair.partition(':')[0].strip(): pair.partition(':')[2].strip() for pair in pairs}

        request = raw_pairs[0]
        if host := header_dictionary.get('Host'): 
            url = host + request.split()[1] 
            return (url, header_dictionary)
        else: 
            url = None
            return header_dictionary
    except Exception:
        print(f"Something went wrong with parsing user header data! Make sure you pasted it correctly.\nFull exception:\n\n")
        print(traceback.format_exc())
        sys.exit(-1)


def write_to_html(url: str, headers: dict, file: str, joining = '') -> None:
    received_html = requests.get(url, headers=headers)
    with open(file, 'a', encoding='utf-8') as f:
        f.write(joining)
        f.write(received_html.content.decode('utf-8'))
    print(f"Successfully written to \"{file}\": {len(received_html.content)} bytes, {len(received_html.content.decode('utf-8'))} chars.")


if __name__ == '__main__':
    os.chdir(pathlib.Path().resolve())
    print(firefox_headers_to_dict(user_header))