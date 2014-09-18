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

def search_naruto_shippuden(season, episode):
    cache_file = xbmc.translatePath('special://temp') + "naruto_shippuden_episode_list.html"
    #cache_file = "naruto_shippuden_episode_list.html"
    if(os.path.isfile(cache_file)):
        if ((time.time() - os.stat(cache_file).st_mtime)  > cache_age):
            print 'Invalid cache!'
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
        print 'No cache!'
        req = urllib2.Request('http://en.wikipedia.org/wiki/List_of_Naruto:_Shippuden_episodes')
        data = urllib2.urlopen(req).read()
        f = open(cache_file, "w")
        f.write(data)
        f.close()
    season_episode_fix = [{"season": season, "first_episode": first_episode } for season, first_episode in re.findall(r'>(?:Season ([0-9][0-9]*)):.*?>([0-9]*)<\/th>', data,re.DOTALL)]
    episode_number = []
    for item in  season_episode_fix:
        if(item['season'] == season):
            episode_number = int(item['first_episode']) + (episode - 1)
            break
    torrent = "http://naruto.com.br/torrent/narutoPROJECT_-_Shippuuden_%s.mkv.torrent" % str(episode_number)
    print "Naruto Project - Downloading: " + torrent
    return [{"uri": torrent2mag(torrent)}]
    
def search(query):
  return []

def search_episode(imdb_id, tvdb_id, name, season, episode):
    if(tvdb_id == 79824):
        print 'Seaching for: ' + name + ' (' + str(season).zfill(2) + 'E' + str(episode).zfill(2) + ')'
        return search_naruto_shippuden(season, episode)
    else:
        return []

def search_movie(imdb_id, name, year):
    return []

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