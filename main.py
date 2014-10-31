import sys
import os
import urllib2
import hashlib
import time
import re
import xbmcaddon
import xbmcplugin
from pulsar import provider
import shelve
import thread

begin = time.time()
__addon__ = xbmcaddon.Addon(str(sys.argv[0]))
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
sys.path.append(os.path.join(addon_dir, 'resources', 'lib' ))
inicio = time.time()

base_url = 'https://btdigg.org/search'

PREFIX_LOG = 'ANIMESBR - '
HEADERS = { 'Referer' : base_url,
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
}

cache_prefix = xbmc.translatePath('special://temp') + __addon__.getAddonInfo('name').lower().replace(' ','_') + '_cache_'

def search(query):
    return []

def search_movie(imdb_id, name, year):
    return []

def search_episode(ep):
    name = ep['title']
    season = ep['season']
    episode = ep['episode']
    tvdb_id = ep['tvdb_id']
    print PREFIX_LOG + 'Seaching for: ' + name + ' (S' + str(season).zfill(2) + 'E' + str(episode).zfill(2) + ')'
    result = []
    if(tvdb_id == '79824'):
        result = search_naruto_shippuden(season, episode)
    elif(tvdb_id == '81797'):
        result = search_one_piece(season, episode)
    print PREFIX_LOG + 'Result:' + str(result)
    return result

def search_naruto_shippuden(season, episode):
    season_episode_fix = get_cached_func('get_shippuden_fix')
    episode_number = []
    for item in  season_episode_fix:
        if(item['season'] == season):
            episode_number = int(item['first_episode']) + (episode - 1)
            resp = provider.GET(base_url, params={"q": 'narutoPROJECT Shippuuden ' + str(episode_number),})
            return provider.extract_magnets(resp.data)
            break
    return []
    
def search_one_piece(season, episode):
    result = []
    season_episode_fix = get_cached_func('get_onepiece_fix')
    episode_number = []
    for item in  season_episode_fix:
        if(item['season'] == season):
            episode_number = int(item['first_episode']) + (episode - 1)
            resp = provider.GET(base_url, params={"q": 'piecePROJECT ' + str(episode_number) + 'HD',})
            return provider.extract_magnets(resp.data)
            break
    return []
    
def get_onepiece_fix():
    data = get_url('http://en.wikipedia.org/wiki/List_of_One_Piece_episodes')
    return [{"season": season, "first_episode": first_episode } for season, first_episode in re.findall(r'>(?:Season ([0-9][0-9]*))\ ?\(.*?\).*?(?:>([0-9][0-9]*)</th>)', data, re.DOTALL)]

def get_shippuden_fix():
    data = get_cached_func('get_url' ,('http://en.wikipedia.org/wiki/List_of_Naruto:_Shippuden_episodes',))
    return [{"season": season, "first_episode": first_episode } for season, first_episode in re.findall(r'>(?:Season ([0-9][0-9]*))?:.*?>([0-9]*)<\/th>', data, re.DOTALL)]

def get_url(url):
    print PREFIX_LOG + 'Downloading ' + url
    req = urllib2.Request(url, headers=HEADERS)
    data = urllib2.urlopen(req).read()
    return data

def get_cached_func(funcName,funcParm=(False,)):
    m = hashlib.md5()
    m.update(funcName + str(funcParm))
    key = m.hexdigest()
    cache_file = cache_prefix + key + '.db'
    f = globals()[funcName]
    d = shelve.open(cache_file)
    if (d.has_key(key)):
        value = d[key]
        d.close()
        thread.start_new_thread(update_cache, (key,funcName,funcParm, ))
        return value
    else:
        if(funcParm[0] == False):
            d[key] = f()
        else:
            d[key] = f(*funcParm)
        return d[key]

def update_cache(key,funcName,funcParm):
    m = hashlib.md5()
    m.update(funcName + str(funcParm))
    key = m.hexdigest()
    cache_file = cache_prefix + key + '.db'
    f = globals()[funcName]
    d = shelve.open(cache_file)
    if(funcParm[0] == False):
        d[key] = f()
    else:
        d[key] = f(*funcParm)
    print PREFIX_LOG + 'Cache key: ' + key + ' updated!'
    d.close()
    
print PREFIX_LOG + 'Time: ' + str((time.time() - inicio))
provider.register(search, search_movie, search_episode)