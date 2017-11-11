import copy
import json
import re

import execjs
import requests
from pyquery import PyQuery as pq

from .base import BaseDiziCrawler


class DizipubCrawler(BaseDiziCrawler):
    def __init__(self):
        BaseDiziCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://dizipub.com/" + self.episode['dizi_url'] + "-" + \
               str(self.episode['season']) + "-sezon-" + str(self.episode['episode']) + "-bolum"

    def after_body_loaded(self, text):
        page_dom = pq(text)
        player_address = page_dom('.object-wrapper').eq(0).find('iframe').attr('src')

        result = self.session.get(player_address)

        if result.status_code == 200:
            if "sources" in result.text:
                self.after_sources_loaded(result.text)
            else:
                self.after_player_loaded(result.text)

        self.episode['site'] = 'dizipub'

    def after_player_loaded(self, text):
        page_dom = pq(text)
        player_address = page_dom('iframe').attr('src')

        result = self.session.get(player_address)

        if result.status_code == 200:
            self.after_sources_loaded(result.text)

    def after_sources_loaded(self, text):
        match = re.search(r'setup\((.*?)}\);', text, re.DOTALL).group(1) + '}'
        ctx = execjs.compile("function b(){\na=" + match + "\nreturn a['sources'];}")
        sources = ctx.call("b")

        for source in sources:
            if 'p' not in source['label']:
                source['label'] += 'p'
            video_link = {"res": source['label'], "url": source['file']}
            if source['type'] == "mp4":
                self.episode['video_links'].append(video_link)
