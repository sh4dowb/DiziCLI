import requests

import dizicli


class BaseDiziCrawler:
    headers = dict()
    headers["Accept"] = "text/html,application/xhtml+xml," + \
                        "application/xml;q=0.9,image/webp,*/*;q=0.8"
    headers["Accept-Encoding"] = "gzip] = deflate] = sdch"
    headers["Accept-Language"] = "en-US,en;q=0.8"
    headers["Connection"] = "keep-alive"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) " + \
                            "AppleWebKit/537.36 (KHTML, like Gecko) " + \
                            "Ubuntu Chromium/51.0.2704.79 " + \
                            "Chrome/51.0.2704.79 " + \
                            "Safari/537.36"

    def __init__(self):
        self.episode = None
        self.session = requests.Session()
        self.session.headers.update(BaseDiziCrawler.headers)

    def get_sources(self, episode):
        self.episode = episode
        self.episode['video_links'] = list()
        self.episode['subtitle_links'] = list()

        result = self.session.get(self.generate_episode_page_url())
        if result.status_code == 200:
            try:
                self.after_body_loaded(result.text)
                self.episode['video_links'] = dizicli.sort_video_links(
                    self.episode['video_links'])
            except:
                pass

        return self.episode

    def generate_episode_page_url(self):
        pass

    def after_body_loaded(self, text):
        pass


class BaseMovieCrawler:
    headers = dict()
    headers["Accept"] = "text/html,application/xhtml+xml," + \
                        "application/xml;q=0.9,image/webp,*/*;q=0.8"
    headers["Accept-Encoding"] = "gzip] = deflate] = sdch"
    headers["Accept-Language"] = "en-US,en;q=0.8"
    headers["Connection"] = "keep-alive"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) " + \
                            "AppleWebKit/537.36 (KHTML, like Gecko) " + \
                            "Ubuntu Chromium/51.0.2704.79 " + \
                            "Chrome/51.0.2704.79 " + \
                            "Safari/537.36"

    def __init__(self):
        self.movie = None

    def get_sources(self, movie):
        self.movie = movie
        self.movie['video_links'] = list()
        self.movie['subtitle_links'] = list()

        result = requests.get(self.generate_movie_page_url())
        if result.status_code == 200:
            try:
                self.after_body_loaded(result.text)
                self.movie['video_links'] = dizicli.sort_video_links(
                    self.movie['video_links'])
            except:
                pass

        return self.movie

    def generate_movie_page_url(self):
        pass

    def after_body_loaded(self, text):
        pass
