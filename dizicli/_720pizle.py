import json
import re

import execjs
import requests

from pyquery import PyQuery as pq
from .base import BaseMovieCrawler


class _720pizleCrawler(BaseMovieCrawler):
    def __init__(self):
        BaseMovieCrawler.__init__(self)

    def generate_movie_page_url(self):
        return "http://720pizle.com/izle/altyazi/" + self.movie['movie_url'] + ".html"

    def after_body_loaded(self, text):
        page_dom = pq(text)
        player_address = "http://720pizle.com/player/plusplayer2.asp?v=" + page_dom(".plusplayerV2").text()

        text = requests.get(player_address, headers=BaseMovieCrawler.headers).text

        video_altyazi_test = re.search(r"(var altyazi(?s).*.\$\(d)", text).group(1)[:-3]
        ctx = execjs.compile('function b(){\n' + video_altyazi_test + 'return [video, altyazi];}')
        [sources, subs] = ctx.call("b")

        for source in sources:
            video_link = {"res": source['label'], "url": "http://720pizle.com" + source['file']}
            self.movie['video_links'].append(video_link)

        for source in subs:
            if source['label'][0] == 'T':
                source['label'] = 'tr'
            elif source['label'][0] == 'E':
                source['label'] = 'en'

            subtitle_link = {"lang": source['label'], "url": source['file'], "kind": "vtt"}
            self.movie['subtitle_links'].append(subtitle_link)
