# -*- coding: utf-8 -*-
import myResolver, xbmc, urlparse, re

def GetFullLink(url, mode):
	#xbmc.log('player   ======>> url: {0},  mode: {1}'.format(url, mode), 2)
	if mode != '0' and mode != '3':
		url = myResolver.Resolve(url, mode, isLiveTV=True)
	if '.f4m' in url:
		url = "hds://{0}".format(url)
	return url

def GetStreamUrl(url):
	try:
		params = dict(urlparse.parse_qsl(url.replace('?','')))
	except:
		params = {}
	try:
		regex = re.compile('[\?|&]mode=(\-?[0-9]+)', re.I+re.M+re.U+re.S)
		streamUrl = regex.sub('', url[5:]).strip()
	except:
		streamUrl = url[5:]
	quality = params.get('q', 'best')
	mode = params.get('mode', '0')
	
	streamUrl = GetFullLink(streamUrl.replace('&', '?', 1), mode)
	#xbmc.log('Sending "{0}" to Livestreamer.'.format(streamUrl), 2)
	return streamUrl, quality
	