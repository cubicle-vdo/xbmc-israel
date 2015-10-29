# -*- coding: utf-8 -*-
import myResolver

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
	if mode != 0 and mode != -3:
		url = myResolver.Resolve(url, mode)
		
	if mode == -2 or mode == -3:
		url = "hds://{0}".format(url)
	elif mode == 4 or mode == 5 or mode == 12 or mode == 15:
		url = "hls://{0}".format(url)
	elif mode != 0:
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
		if mode == 1:
			streamUrl = url
	except:
		mode = 0
		streamUrl = url[5:]
	
	if streamUrl == "BB":
		mode = -1
	elif '.f4m' in streamUrl:
		mode = -2 if 'keshet' in streamUrl else -3

	streamUrl = GetFullLink(streamUrl, mode)
	print 'Sending "{0}" to Livestreamer.'.format(streamUrl)
	return streamUrl, quality
	