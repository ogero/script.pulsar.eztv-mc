from pulsar import provider

url_address = provider.ADDON.getSetting('url_address')
icon = provider.ADDON.getAddonInfo('icon') # gets icon
values3 = {'ALL': 0, 'HDTV': 1,'480p': 1,'DVD': 1,'720p': 2 ,'1080p': 3, '3D': 3, "1440p": 4 ,"2K": 5,"4K": 5} #code_resolution steeve
#quality_TV
TV_q1 = provider.ADDON.getSetting('TV_q1') #480p
TV_q2 = provider.ADDON.getSetting('TV_q2') #720p
TV_allow = []
TV_deny = [] 
TV_allow.append('480p') if TV_q1 == 'true' else TV_deny.append('480p')
TV_allow.append('720p') if TV_q2 == 'true' else TV_deny.append('720p')

# function to validate
def included(value, keys):
    res = False
    for item in keys:
        if item in value:
            res = True 
            break
    return res

def search(info):
	return []

def search_episode(info):
	title= ' S%02dE%02d' % (info['episode'],info['season'])
	provider.notify(message='Searching: ' + info['title'].title()  + title +'...', header=None, time=1500, image=icon)
	url = str(url_address) + "/show/" + info['imdb_id']
	provider.log.info(url)
	response = provider.GET(url)
	results=[]
	if  str(response.data)!='':
		provider.log.info('Keywords allowed: ' + str(TV_allow))
		provider.log.info('Keywords denied: ' + str(TV_deny))
		items = provider.parse_json(response.data)
		for episode in items['episodes']:
			if (episode['episode']==info['episode'] and episode['season']==info['season']):
				for resolution in episode['torrents']:
					resASCII =resolution.encode('utf-8')
					name = resASCII + ' - ' + items['title'] + ' - ' + episode['title']
					if included(resASCII, TV_allow) and not included(resASCII, TV_deny):
						res_val=values3[resASCII]
						results.append({'name': name + ' - EZTVapi Provider', 'uri': episode['torrents'][resolution]['url'],'resolution' : res_val})
					else:
						provider.log.warning(name + '   ***Not Included for keyword filtering or size***')
	return results
	
def search_movie(info):
	# not info
	return []

# This registers your module for use
provider.register(search, search_movie, search_episode)
