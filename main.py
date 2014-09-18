import sys
import json
import base64
import re
import urllib
import urllib2
import time
import os
import bencode
import hashlib
inicio = time.time()
cache_age = 48 * 60 * 60

URL_BASE = 'http://www.storetorrent.org/s/'

def search(query):
    return []

def search_movie(imdb_id, name, year):
    return []

def search_episode(imdb_id, tvdb_id, name, season, episode):
    print 'ANIMES-BR Provider Seaching for: ' + name + ' (' + str(season).zfill(2) + 'E' + str(episode).zfill(2) + ')'
    result = []
    if(tvdb_id == '79824'):
        result = search_naruto_shippuden(season, episode)
    elif(tvdb_id == '81797'):
        result = search_one_piece(season, episode)
    print 'ANIMES-BR Provider Result:' + str(result)
    return result

def search_naruto_shippuden(season, episode):
    result = []
    data = get_cached_url('http://en.wikipedia.org/wiki/List_of_Naruto:_Shippuden_episodes')
    season_episode_fix = [{"season": season, "first_episode": first_episode } for season, first_episode in re.findall(r'>(?:Season ([0-9][0-9]*))?:.*?>([0-9]*)<\/th>', data, re.DOTALL)]
    episode_number = []
    for item in  season_episode_fix:
        if(item['season'] == season):
            episode_number = int(item['first_episode']) + (episode - 1)
            result.append({"uri": storetorrent_get_magnet('narutoPROJECT Shippu' + str(episode_number))})
            break
    return result

def search_one_piece(season, episode):
    result = []
    data = get_cached_url('http://en.wikipedia.org/wiki/List_of_One_Piece_episodes')
    season_episode_fix = [{"season": season, "first_episode": first_episode } for season, first_episode in re.findall(r'>(?:Season ([0-9][0-9]*))\ ?\(.*?\).*?(?:>([0-9][0-9]*)</th>)', data, re.DOTALL)]
    episode_number = []
    for item in  season_episode_fix:
        if(item['season'] == season):
            episode_number = int(item['first_episode']) + (episode - 1)
            result.append({"uri": storetorrent_get_magnet('piecePROJECT ' + str(episode_number) + 'HD')})
            break
    return result

def storetorrent_get_magnet(query):
    req = urllib2.Request(URL_BASE + urllib.quote_plus(query))
    data = urllib2.urlopen(req).read()
    for magnet in re.findall(r'(magnet:.*)" class', data):
        return magnet

def torrent2mag(torrent_url):
    response = urllib2.urlopen(torrent_url)
    torrent = response.read()
    metadata = bencode.bdecode(torrent)
    hashcontents = bencode.bencode(metadata['info'])
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest)
    magneturl = 'magnet:?xt=urn:btih:' + b32hash  + '&dn=' + metadata['info']['name']
    return magneturl

def get_cached_url(url):
    data = ''
    m = hashlib.md5()
    m.update(url)
    url_hash = m.hexdigest()
    cache_file = xbmc.translatePath('special://temp') + url_hash
    print 'ANIMES-BR Provider:  cache -> ' + cache_file
    if(os.path.isfile(cache_file)):
        if ((time.time() - os.stat(cache_file).st_mtime)  > cache_age):
            print 'ANIMES-BR Provider: Invalid cache!'
            req = urllib2.Request(url)
            data = urllib2.urlopen(req).read()
            f = open(cache_file, "w")
            f.write(data)
            f.close()
        else:
            f = open(cache_file, "r")
            data = f.read()
            f.close()
    else:
        print 'ANIMES-BR Provider: No cache!'
        req = urllib2.Request(url)
        data = urllib2.urlopen(req).read()
        f = open(cache_file, "w")
        f.write(data)
        f.close()
    return data

PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))
urllib2.urlopen(
PAYLOAD["callback_url"],
data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)
print 'ANIMES-BR Provider Time: ' + str(time.time() - inicio)