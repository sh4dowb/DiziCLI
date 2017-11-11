import copy
import json

import requests
from furl import furl
from pyquery import PyQuery as pq

from .base import BaseDiziCrawler


class DiziboxCrawler(BaseDiziCrawler):
    def __init__(self):
        BaseDiziCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://www.dizibox1.com/" + self.episode['dizi_url'] + "-" + \
               str(self.episode['season']) + "-sezon-" + str(
            self.episode['episode']) + "-bolum-izle"

    def after_body_loaded(self, text):
        ajax_headers = copy.copy(BaseDiziCrawler.headers)
        ajax_headers['X-Requested-With'] = 'XMLHttpRequest'

        page_dom = pq(text)
        player_address = page_dom("iframe[src^='http://play.dizibox.net']").attr("src")
        f = furl(player_address)
        video_id = f.args['v']
        source_url = f.scheme + '://' + f.host + str(f.path) + "?p=GetVideoSources"

        result = requests.post(source_url, headers=ajax_headers, data={"ID": video_id})

        if result.status_code == 200:
            self.after_sources_loaded(result.text)

        self.episode['site'] = 'dizibox'

    def after_sources_loaded(self, text):
        sources = json.loads(text)['VideoSources']

        for source in sources:
            if 'p' not in source['label']:
                source['label'] += 'p'
            video_link = {"res": source['label'], "url": source['file']}
            if "mp4" in source['type']:
                self.episode['video_links'].append(video_link)
