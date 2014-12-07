# -*- coding: utf-8 -*-
import urllib2
import urllib
import time
import re
from pulsar import provider

# Só vai funcionar com trackers abertos.
#
# Sintaxe: [TVBD_ID,'STRING DE BUSCA','TRACKER_ENGINE','URL_DE_BUSCA']
#
# TVBD_ID: Código do anime (vide http://thetvdb.com/).
# STRING DE BUSCA: String usada para busca, onde %EPISODE% será substituído pelo número do episódio.
# TRACKER_ENGINE: Valores aceitos: 'generic' e 'btdigg_api'.
# URL_DE_BUSCA: Parte da URL que fica antes da "String de Busca".\
#
# Atenção não se esqueça da virgula no final.
# A engine "generic" só funciona com pesquisas que retornem o link magnético direto.

animes_array = [
            [79824,'narutoPROJECT Shippuuden %EPISODE%','btdigg_api','http://api.btdigg.org/api/public-8e9a50f8335b964f/s01?q='],
            [81797,'piecePROJECT %EPISODE%','btdigg_api','http://api.btdigg.org/api/public-8e9a50f8335b964f/s01?q='],
            [252322,'HXP-E_%EPISODE%','btdigg_api','http://api.btdigg.org/api/public-8e9a50f8335b964f/s01?q='],
]


PREFIX_LOG = 'ANIMESBR - '
inicio = time.time()
def search(query):
    return []

def search_movie(movie):
    return []

def search_episode(ep):
    title = ep['title']
    absolute_number = ep['absolute_number']
    tvdb_id = ep['tvdb_id']
    provider.log.info(PREFIX_LOG + 'Procurando por: ' + title + ' ' + str(absolute_number))
    result = []
    tracker = ''
    base_url = ''
    string_search = ''    
    for anime in animes_array:
        if anime[0] == tvdb_id:
            string_search = re.sub(' ', '+',re.sub('%EPISODE%', str(absolute_number),anime[1]))
            tracker = anime[2]
            base_url = anime[3]
            provider.log.info(PREFIX_LOG + 'String de busca: ' + string_search)
            break
    if ((tracker != '') and (base_url != '') and (string_search != '')):
        result = search_anime(tracker, base_url, string_search)
    provider.log.info(PREFIX_LOG + 'Result:' + str(result))
    return result
    
def search_anime(tracker, base_url, string_search):
    if tracker == 'btdigg_api':
        return search_btdigg(base_url, string_search)
    else:
        return search_generic(base_url, string_search)
        
def search_btdigg(base_url, string_search):
    result = []
    u = urllib2.urlopen(base_url + string_search)
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
    
def search_generic(base_url, string_search):
    data = urllib2.urlopen(base_url + string_search)
    return provider.extract_magnets(data.read())

provider.log.info(PREFIX_LOG + 'Time: ' + str((time.time() - inicio)))
provider.register(search, search_movie, search_episode)
