# -*- coding: utf-8 -*-
from typing import Dict, Tuple
import requests
import os
import pathlib
from bs4 import BeautifulSoup as Soup
import re

firefox_header = ""


def firefox_headers_to_dict(raw_header: str) -> Tuple[str, Dict]:
    raw_pairs = raw_header.split('\n')
    pairs = raw_pairs[1:] # Removes the request
    header_dictionary = {pair.partition(':')[0]: pair.partition(':')[2].strip() for pair in pairs}

    request = raw_pairs[0]
    url = header_dictionary.get('Host') + request.split()[1]
    return (url, header_dictionary)



    

os.chdir(pathlib.Path().resolve())
headers = {}
def write_to_html(url: str, headers: dict, file: str, joining = '') -> None:
    received_html = requests.get(url, headers=headers)
    with open(file, 'a', encoding='utf-8') as f:
        f.write(joining)
        f.write(received_html.content.decode('utf-8'))
    print(f"Successfully written to \"{file}\": {len(received_html.content)} bytes, {len(received_html.content.decode('utf-8'))} chars.")


if __name__ == '__main__':
    # for id in range(196588, 196600):
    #     write_to_html(f'https://b.optima-osvita.org/mod/lesson/view.php?id=47586&pageid={id}', 
    #                     headers, 
    #                     "bruh.html", 
    #                     f"\n\n\n\n===={id}====\n\n\n\n")
    print(firefox_headers_to_dict(firefox_header))