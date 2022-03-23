import requests
import random
from time import sleep
import re
import json
from bs4 import BeautifulSoup

visited_pages = dict()

RE_PATTERN = re.compile(r"(^https:\/\/shikimori.one\/.*)")
HEADERS = [{'user-agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)'},
           {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'},
           {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'},
           {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}]


def parse_page(url, depth=0):
    if depth > 3:
        return

    print(f"[parsing] {url} with depth = {depth}")
    response = requests.get(url, headers=HEADERS[random.randint(0, 3)])
    print(f"[status-code] {response.status_code}")
    sleep(random.uniform(0.75, 1.25))
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    visited_pages[url] = links
    print(f"[visited pages] {len(visited_pages.keys())}")

    for link in links:
        if RE_PATTERN.match(link) and link not in visited_pages.keys():
            parse_page(url=link, depth=depth + 1)


if __name__ == '__main__':
    parse_page(url="https://shikimori.one/Bodyancheq", depth=0)
    with open("link_data3.json", "w", encoding="utf-8") as linkfile:
        json.dump(visited_pages, linkfile, indent=4, ensure_ascii=False)
