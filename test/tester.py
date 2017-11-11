from pprint import pprint

from dizicli.crawler import DiziCrawler

dc = DiziCrawler('', 'family guy', 1, 1)
dc.ignore(r'.*(tunefiles|expires|ttl=).*')
episode = dc.get_sources()
assert len(episode['video_links']) > 0
pprint('No site test successful')
pprint(episode)

episode = DiziCrawler('diziay', 'the flash', 4, 3).get_sources()
assert len(episode['video_links']) > 0
pprint('Diziay test successful')

episode = DiziCrawler('dizist', 'travelers', 2, 2).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizist test successful')

episode = DiziCrawler('dizimag', 'the-walking-deaddd', 8, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizimag test successful')

episode = DiziCrawler('dizipub', 'the-office', 1, 2).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizipub test successful')

episode = DiziCrawler('dizilab', 'rick-and-morty', 3, 6).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizilab test successful')

episode = DiziCrawler('sezonlukdizi', 'the-big-bang-theory', 11, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Sezonlukdizi test successful')

episode = DiziCrawler('dizibox', 'doctor-who', 10, 8).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizibox test successful')

episode = DiziCrawler('dizimek', 'how i met your mother', 1, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizimek test successful')
