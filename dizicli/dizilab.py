import copy
import json
import re

import requests
from pyquery import PyQuery as pq

from .base import BaseDiziCrawler


class DizilabCrawler(BaseDiziCrawler):
    def __init__(self):
        BaseDiziCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://dizilab.net/" + self.episode['dizi_url'] + "/sezon-" + \
               str(self.episode['season']) + "/bolum-" + str(self.episode['episode'])

    def after_body_loaded(self, text):
        ajax_headers = copy.copy(BaseDiziCrawler.headers)
        ajax_headers['X-Requested-With'] = 'XMLHttpRequest'
        ajax_headers['Referer'] = self.generate_episode_page_url()

        page_dom = pq(text)
        kaynak = page_dom('.language.alternative').find('a').eq(0).attr('onclick')
        vid = kaynak[11:23]

        result = requests.post("http://dizilab.net/request/php/",
                               data={"vid": vid, "tip": "1", "type": "loadVideo"},
                               headers=ajax_headers)

        if result.status_code == 200:
            self.after_sources_loaded(result.text)

        self.episode['site'] = 'dizilab'

    def after_sources_loaded(self, text):
        redirect_url = json.loads(text)['html']
        redirect_url = pq(redirect_url)('#episode_player').attr("src")

        text = self.session.get(redirect_url).text

        m = re.search(r'sources: (.*?),\]', text, re.S)
        match = m.group(1) + "]"
        match = match.replace('\'', '"')
        sources = json.loads(match)

        for source in sources:
            if 'p' not in source['label']:
                source['label'] += 'p'
            video_link = {"res": source['label'], "url": source['file']}
            if source['type'] == "mp4":
                self.episode['video_links'].append(video_link)

        sources = json.loads(text)['sources']
        for source in sources:
            video_link = {"res": source['label'], "url": source['file']}
            self.episode['video_links'].append(video_link)
