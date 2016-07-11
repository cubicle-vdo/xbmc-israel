# -*- coding: utf-8 -*-
import myResolver, xbmc

def get_params(url):
	param=[]
	params = url
	if len(params) >= 2:
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
							
	return param
		
def GetFullLink(url, mode):
	#xbmc.log('player   ======>> url: {0},  mode: {1}'.format(url, mode), 2)
	if mode != 0 and mode != 3:
		url = myResolver.Resolve(url, mode)
	if '.f4m' in url:
		url = "hds://{0}".format(url)
	elif mode == 1 or mode == 4 or mode == 5 or mode == 12 or mode == 15 or mode == 19 or mode == 20 or mode == 22 or mode == 25 or mode == 27 or mode == 34:
		url = "hls://{0}".format(url)
	elif mode != 0 and mode != 3:
		url = "hlsvariant://{0}".format(url)
	return url

def GetStreamUrl(url):
	try:
		params = get_params(url)
	except:
		pass
	try:
		streamUrl = params["url"]
	except:
		streamUrl = url[5:]
	try:
		quality = params["q"]
	except:
		quality = "best"
	try:
		mode = int(params["mode"])
	except:
		mode = 0
		streamUrl = url[5:]
	
	if mode == 1 or mode == 3:
		streamUrl = url[5:url.find('&mode')]
	if '.f4m' in streamUrl and 'keshet' in streamUrl:
		mode = -2
		
	streamUrl = GetFullLink(streamUrl.replace('&', '?', 1), mode)
	xbmc.log('Sending "{0}" to Livestreamer.'.format(streamUrl), 2)
	return streamUrl, quality
	