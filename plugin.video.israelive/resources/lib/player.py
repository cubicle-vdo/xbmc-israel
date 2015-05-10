# -*- coding: utf-8 -*-
import urllib, json, xbmcaddon, random
import myFilmon, myResolver

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
	
def GetMakoUrl(url):
	dvs = urllib.urlopen('http://www.mako.co.il/AjaxPage?jspName=FlashVODOnAir.jsp').read()
	result = json.loads(dvs)
	random.seed()
	random.shuffle(result)
	dv = result[0]["id"]
	makoTicket = urllib.urlopen('http://mass.mako.co.il/ClicksStatistics/entitlementsServices.jsp?et=gt&rv=akamai&dv={0}&lp='.format(dv)).read()
	result = json.loads(makoTicket)
	ticket = result['tickets'][0]['ticket']
	url =  "{0}?{1} pvswf=http://images0.kure.tv/jw9/jwplayer.flash.swf".format(url, ticket)
	#url =  "{0}?{1}&hdcore=3.0.3".format(url, ticket)
	return url
	
def GetFilmonUrl(channelNum):
	url, chName, iconimage, programmes = myFilmon.GetUrlStream(channelNum, filmonOldStrerams=True, useRtmp=False)
	url = "hlsvariant://{0}".format(url)
	return url
	
def GetFullLink(url, mode):
	if mode == 2:
		url = "hlsvariant://{0}".format(myResolver.GetGLArabFullLink(url))
	elif mode == 5:
		url = "hls://{0}".format(myResolver.GetSatElitFullLink(url))
	elif mode == 6:
		url = "hlsvariant://{0}".format(myResolver.GetGinkoFullLink(url))
	elif mode == 8:
		url = "hlsvariant://{0}".format(myResolver.GetCctvLink(url))
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
	
	
	if mode == 1:
		streamUrl = GetFilmonUrl(url)
	elif mode == 2 or mode == 5 or mode == 6 or mode == 8:
		streamUrl = GetFullLink(streamUrl, mode)
	elif streamUrl.find('f4m') > 0:
		if streamUrl.find('keshet') > 0:
			streamUrl = GetMakoUrl(streamUrl)
		streamUrl = "hds://{0}".format(streamUrl)
	elif streamUrl == "BB":
		streamUrl = "hlsvariant://{0}".format(myResolver.GetBBLink())
	else:
		streamUrl = url[5:]

	return streamUrl, quality
	