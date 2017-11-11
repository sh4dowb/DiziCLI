import re

import dizicli
from .diziay import DiziayCrawler
from .dizibox import DiziboxCrawler
from .dizilab import DizilabCrawler
from .dizimag import DizimagCrawler
from .dizimek import DizimekCrawler
from .dizipub import DizipubCrawler
from .dizist import DizistCrawler
from .sezonlukdizi import SezonlukDiziCrawler
from ._720pizle import _720pizleCrawler

dizisites = {
    "dizilab": DizilabCrawler,
    "dizipub": DizipubCrawler,
    "sezonlukdizi": SezonlukDiziCrawler,
    "dizimag": DizimagCrawler,
    "dizibox": DiziboxCrawler,
    "diziay": DiziayCrawler,
    "dizist": DizistCrawler,
    "dizimek": DizimekCrawler,
}

moviesites = {
    "720pizle": _720pizleCrawler
}


class DiziCrawler:
    def __init__(self, site, dizi_url, season_number, episode_number):
        self.site = site
        self.ignore_pattern = None
        if self.site in list(dizisites.keys()):
            self.dizicrawler = dizisites[self.site]()
        elif self.site == '':
            self.dizicrawler = None

        self.episode = {"dizi_url": dizicli.slugify(dizi_url),
                        "season": season_number,
                        "episode": episode_number}

    def get_sources(self):
        if self.dizicrawler is not None:
            self.episode = self.dizicrawler.get_sources(self.episode)
        else:
            for site in list(dizisites.keys()):
                self.dizicrawler = dizisites[site]()
                self.episode = self.dizicrawler.get_sources(self.episode)
                ok_to_return = 'video_links' in self.episode
                ok_to_return &= len(self.episode['video_links']) > 0
                if ok_to_return and self.ignore_pattern is not None:
                    for video_link in self.episode['video_links']:
                        ok_to_return &= (not self.ignore_pattern.match(video_link['url']))
                if ok_to_return:
                    break

        return self.episode

    def ignore(self, pattern):
        self.ignore_pattern = re.compile(pattern)


class MovieCrawler:
    def __init__(self, site, movie_url):
        self.site = site
        if self.site in list(moviesites.keys()):
            self.moviecrawler = moviesites[self.site]()
        elif self.site == '':
            self.moviecrawler = None

        self.movie = {"movie_url": dizicli.slugify(movie_url)}

    def get_sources(self):

        if self.moviecrawler is not None:
            self.movie = self.moviecrawler.get_sources(self.movie)
        else:
            for site in list(moviesites.keys()):
                self.moviecrawler = moviesites[site]()
                self.movie = self.moviecrawler.get_sources(self.movie)
                if 'video_links' in self.moviecrawler.movie and len(
                        self.moviecrawler.movie['video_links']) > 0:
                    break

        return self.movie
