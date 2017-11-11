import argparse
import json
import os
import subprocess
import sys
import webbrowser
from pprint import pprint

from dizicli import crawler
from dizicli.crawler import MovieCrawler


def download_callback(downloader):
    percent = "{0:.1f}" \
        .format(100 * (downloader.total_downloaded / float(downloader.total_length)))
    filled_length = int(80 * downloader.total_downloaded / downloader.total_length)
    bar = '█' * filled_length + '-' * (80 - filled_length)
    sys.stdout.write('\r%s |%s| %s%% %s' % (downloader.readable_speed, bar, percent, ''))
    sys.stdout.flush()
    if downloader.total_downloaded == downloader.total_length:
        sys.stdout.write('\n')


def run(argv):
    parser = argparse.ArgumentParser(description='Filmcli - Watch, Download, Crawl Movies')
    parser.add_argument('movie', metavar='Avatar', help='Name of the Movie', type=str)
    parser.add_argument('--site', metavar='720pizle', help='Website to crawl', type=str, default='',
                        choices=list(crawler.moviesites.keys()))
    parser.add_argument('-o', dest="output", metavar='output.json',
                        help='Output file for crawling result', type=str)
    parser.add_argument('--vlc', metavar='/vlc/binary/destination',
                        help='Link VLC executable to play the movie',
                        type=str)
    parser.add_argument('-d', dest="download",
                        help='If given, the movie is downloaded with highest quality.',
                        action='store_true', default=False)

    try:
        args = parser.parse_args(argv)
    except:
        return

    c = MovieCrawler(args.site, args.movie)
    movie = c.get_sources()

    out_text = json.dumps(movie)
    if args.output is not None:
        with open(args.output, 'w') as f:
            f.write(out_text)
    else:
        pprint(movie)
        print('\n\n')

    if args.vlc is not None and len(movie['video_links']) > 0:
        if args.vlc == 'web':
            webbrowser.open_new_tab(movie['video_links'][-1]['url'])
        else:
            subprocess.call([args.vlc, '-f', movie['video_links'][-1]['url']])

    if args.download and len(movie['video_links']) > 0:
        import pget
        dirname = os.path.join(os.getcwd(), movie['movie_url'])

        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        if os.path.isdir(dirname):
            videoname = os.path.join(dirname, 'Video.mp4')
            downloader = pget.Downloader(movie['video_links'][-1]['url'], videoname, 16)
            print("Downloading: %s" % videoname)
            downloader.subscribe(download_callback, 256)
            downloader.start_sync()
            if len(movie['subtitle_links']) > 0:
                for sub in movie['subtitle_links']:
                    subname = os.path.join(dirname, sub['lang'] + '.vtt')
                    downloader = pget.Downloader(sub['url'], subname, 1)
                    print("Downloading: %s" % subname)
                    downloader.subscribe(download_callback, 256)
                    downloader.start_sync()


def main():
    if sys.stdin.isatty():
        run(sys.argv[1:])
    else:
        argv = sys.stdin.read().split(' ')
        run(argv)
