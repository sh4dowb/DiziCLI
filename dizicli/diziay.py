import json
import re

import demjson
import execjs
import requests
from pyquery import PyQuery as pq

from .base import BaseDiziCrawler


class DiziayCrawler(BaseDiziCrawler):
    def __init__(self):
        BaseDiziCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://diziay.com/izle/" + self.episode['dizi_url'] + "-" + \
               str(self.episode['season']) + "-sezon-" + str(self.episode['episode']) + "-bolum/"

    def after_body_loaded(self, text):
        part_id = re.search('var FIRST_PART =([0-9]+);', text).group(1)
        result = self.session.post("http://diziay.com/ajax/getpart", data={'part_id':part_id})

        if result.status_code == 200:
            self.after_part_loaded(result.text)

        self.episode['site'] = 'diziay'

    def after_part_loaded(self, text):
        page_dom = pq(text)
        player_address = page_dom("iframe").attr("src")
        content =self.session.get(player_address).text

        self.after_sources_loaded(content)

    def after_sources_loaded(self, text):
        eval_text = re.search(r'(var source = .*?;)', text).group(1)
        js_func = "function b(){" + eval_text + "; return JSON.stringify(source);}"
        ctx = execjs.compile(js_func)
        sources = json.loads(ctx.call("b"))

        for source in sources:
            if 'p' not in source['label']:
                source['label'] += 'p'
            video_link = {"res": source['label'], "url": source['file']}
            if "mp4" in source['type']:
                self.episode['video_links'].append(video_link)
