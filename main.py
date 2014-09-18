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
cache_age = 24 * 60 * 60
URL_BASE = 'http://www.storetorrent.org/s/'

def search(query):
  return []

def search_movie(imdb_id, name, year):
    return []

def search_episode(imdb_id, tvdb_id, name, season, episode):
    print 'ANIMES-BR Provider Seaching for: ' + name + ' (' + str(season).zfill(2) + 'E' + str(episode).zfill(2) + ')'
    if(tvdb_id == '79824'):
        return search_naruto_shippuden(season, episode)
    elif(tvdb_id == '81797'):
        return search_one_piece(season, episode)
    else:
        return []

def search_naruto_shippuden(season, episode):
    cache_file = xbmc.translatePath('special://temp') + "naruto_shippuden_episode_list.html"
    #cache_file = "naruto_shippuden_episode_list.html"
    if(os.path.isfile(cache_file)):
        if ((time.time() - os.stat(cache_file).st_mtime)  > cache_age):
            print 'ANIMES-BR Provider: Invalid cache!'
            req = urllib2.Request('http://en.wikipedia.org/wiki/List_of_Naruto:_Shippuden_episodes')
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
        req = urllib2.Request('http://en.wikipedia.org/wiki/List_of_Naruto:_Shippuden_episodes')
        data = urllib2.urlopen(req).read()
        f = open(cache_file, "w")
        f.write(data)
        f.close()
    season_episode_fix = [{"season": season, "first_episode": first_episode } for season, first_episode in re.findall(r'>(?:Season ([0-9][0-9]*))?:.*?>([0-9]*)<\/th>', data,re.DOTALL)]
    episode_number = []
    for item in  season_episode_fix:
        if(item['season'] == season):
            episode_number = int(item['first_episode']) + (episode - 1)
            break
    episode_number = []
    for item in  season_episode_fix:
        if(item['season'] == season):
            episode_number = int(item['first_episode']) + (episode - 1)
            break
    result = [{"uri": storetorrent_get_magnet('narutoPROJECT Shippu' + str(episode_number))}]
    return result

def search_one_piece(season, episode):
    cache_file = xbmc.translatePath('special://temp') + "one_piece_episode_list.html"
    #cache_file = "one_piece_episode_list.html"
    if(os.path.isfile(cache_file)):
        if ((time.time() - os.stat(cache_file).st_mtime)  > cache_age):
            print 'ANIMES-BR Provider: Invalid cache!'
            req = urllib2.Request('http://en.wikipedia.org/wiki/List_of_One_Piece_episodes')
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
        req = urllib2.Request('http://en.wikipedia.org/wiki/List_of_One_Piece_episodes')
        data = urllib2.urlopen(req).read()
        f = open(cache_file, "w")
        f.write(data)
        f.close()
    season_episode_fix = [{"season": season, "first_episode": first_episode } for season, first_episode in re.findall(r'>(?:Season ([0-9][0-9]*))\ ?\(.*?\).*?(?:>([0-9][0-9]*)</th>)', data,re.DOTALL)]
    episode_number = []
    for item in  season_episode_fix:
        if(item['season'] == season):
            episode_number = int(item['first_episode']) + (episode - 1)
            break
    result = [{"uri": storetorrent_get_magnet('piecePROJECT ' + str(episode_number) + 'HD')}]
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

PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))
urllib2.urlopen(
PAYLOAD["callback_url"],
data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)
print 'ANIMES-BR Provider Time: ' + str(time.time() - inicio)