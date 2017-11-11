import copy
import json
import re

import requests
from pyquery import PyQuery as pq

from .base import BaseDiziCrawler


class DizimagCrawler(BaseDiziCrawler):
    def __init__(self):
        BaseDiziCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://dizimag4.co/" + self.episode['dizi_url'] + "/" + \
               str(self.episode['season']) + "-sezon-" + str(
            self.episode['episode']) + "-bolum-izle-dizi.html"

    def after_body_loaded(self, text):
        ajax_headers = copy.copy(BaseDiziCrawler.headers)
        ajax_headers['X-Requested-With'] = 'XMLHttpRequest'
        ajax_headers['Referer'] = self.generate_episode_page_url()

        page_dom = pq(text)
        kaynak_degis = page_dom(".alterlink").eq(0).attr("onclick")
        kaynak_degis = re.search(r"kaynakdegis\('([0-9]+)'", kaynak_degis).group(1)

        result = requests.post("https://dizimag4.co/service/partikule", headers=ajax_headers,
                               data={"id": kaynak_degis})

        if result.status_code == 200:
            self.after_sources_loaded(result.text)

        self.episode['site'] = 'dizimag'

    def after_sources_loaded(self, text):
        sources = json.loads(text)

        for key in sources.keys():
            if "videokalite" in key:
                if 'p' not in sources[key]:
                    sources[key] += 'p'
                video_link = {"res": sources[key],
                              "url": sources[key.replace("videokalite", "videolink")]}
                self.episode['video_links'].append(video_link)

            elif "altyazitype" in key:
                sub_link = {"lang": "tr",
                            "url": "http://www.dizimag1.co/dizi/" + sources[key] +
                                   "/" + self.episode['dizi_url'] + "/tr-" +
                                   self.episode['season'] + "-" + self.episode['episode'] + ".vtt",
                            "kind": "srt"}
                self.episode['subtitle_links'].append(sub_link)

                sub_link = {"lang": "en",
                            "url": "http://www.dizimag1.co/dizi/" + sources[key] +
                                   "/" + self.episode['dizi_url'] + "/en-" +
                                   self.episode['season'] + "-" + self.episode['episode'] + ".vtt",
                            "kind": "srt"}
                self.episode['subtitle_links'].append(sub_link)
