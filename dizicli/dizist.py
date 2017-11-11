import json
import re

import requests

from pyquery import PyQuery as pq
from .base import BaseDiziCrawler


class DizistCrawler(BaseDiziCrawler):
    def __init__(self):
        BaseDiziCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://www.dizist1.com/izle/" + self.episode['dizi_url'] + "-" + \
               str(self.episode['season']) + "-sezon-" + str(self.episode['episode']) + "-bolum"

    def after_body_loaded(self, text):
        page_dom = pq(text)
        player_address = page_dom("iframe[src^='/player']").attr("src")
        player_address = 'http://www.dizist1.com' + player_address

        text = requests.get(player_address).text

        m = re.search(r"var sources = JSON.parse\('(.*?)'\);", text)
        match = m.group(1)

        sources = json.loads(match)
        for source in sources:
            if 'p' not in source['label']:
                source['label'] += 'p'
            video_link = {"res": source['label'], "url": source['file']}
            if source['type'] == "mp4":
                self.episode['video_links'].append(video_link)

        self.episode['site'] = 'dizist'
