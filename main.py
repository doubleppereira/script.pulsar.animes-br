import urllib2
import urllib
import time
import re
from pulsar import provider

inicio = time.time()

base_url = 'http://api.btdigg.org/api/public-8e9a50f8335b964f/s01'

PREFIX_LOG = 'ANIMESBR - '

def search(query):
    return []

def search_movie(movie):
    return []

def search_episode(ep):
    title = ep['title']
    absolute_number = ep['absolute_number']
    tvdb_id = ep['tvdb_id']
    provider.log.info(PREFIX_LOG + 'Seaching for: ' + title + ' ' + str(absolute_number))
    result = []
    string_search = re.sub(' ', '+', title + ' ' + str(absolute_number))
    if(tvdb_id == 79824):
        string_search = 'narutoPROJECT+Shippuuden+' + str(absolute_number)
        provider.log.info(PREFIX_LOG + 'Replaced with: ' + string_search)
    elif(tvdb_id == 81797):
        string_search = 'piecePROJECT+' + str(absolute_number)
        provider.log.info(PREFIX_LOG + 'Replaced with: ' + string_search)
    result = search_anime(string_search)
    provider.log.info(PREFIX_LOG + 'Result:' + str(result))
    return result

def search_anime(string_search):
    result = []
    u = urllib2.urlopen(base_url + '?q=' + string_search)
    try:
       for line in u:
        if line.startswith('#'):
            continue
        info_hash, name, files, size, dl, seen = line.strip().split('\t')[:6]
        res = dict(uri = 'magnet:?xt=urn:btih:%s' % (info_hash,) + '&amp;dn=' + '%s' % name.translate(None, '|') ) 
        if(files == '1'):
            result.append(res)
    except urllib2.HTTPError as error_code:
        provider.log.error(PREFIX_LOG + ' error %s' % error_code, xbmc.LOGDEBUG)
    finally:
        u.close()
    return result

provider.log.info(PREFIX_LOG + 'Time: ' + str((time.time() - inicio)))
provider.register(search, search_movie, search_episode)
