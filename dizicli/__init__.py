import re

import sys


def slugify(value):
    import unicodedata
    if sys.version_info < (3, 0):
        value = str(value).decode()
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode()
    value = re.sub('[^\w\s-]', '', value).strip().lower()

    return re.sub('[-\s]+', '-', value)


def sort_video_links(video_links):
    return sorted(video_links, key=lambda k: re.search(r'\d+', k['res']).group())
