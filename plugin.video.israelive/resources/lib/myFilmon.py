import sys, datetime
import urllib, urllib2
if sys.version_info >=  (2, 7):
	import json as _json
else:
	import simplejson as _json

UA = 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0'

def get_params(url):
	param = []
	params = url
	if len(params) >= 2:
		i = params.find('?')
		if i == -1:
			return param
		params = params[i:]
		cleanedparams = params.replace('?','')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0].lower()] = splitparams[1]
	return param

def GetUrlStream(url):
	params=get_params(url)
	chNum = None
	referrerCh = None
	ChName = None
	
	try:
		chNum = urllib.unquote_plus(params["url"])
	except:
		pass
	try:        
		referrerCh = int(params["referrerch"])
	except:
		referrerCh = None
	try:      
		ChName = urllib.unquote_plus(params["chname"])
	except:
		ChName = None
		
	return GetChannelStream(chNum, referrerCh, ChName)

def GetChannelStream(chNum, referrerCh=None, ChName=None):
	if referrerCh == None:
		prms = GetChannelJson(chNum)
	else:
		prms = GetChannelJson(referrerCh)
		
	if prms == None:
		print '--------- Playing Error: there is no channel with id="{0}" ---------'.format(chNum)
		return None,None,None
		
	channelName, programmename, description, iconimage, streamUrl, startdatetime, enddatetime = GetNowPlaying(prms, chNum, referrerCh, ChName)
	fullName = " [B]{0}[/B]".format(channelName)
	if programmename <> "":
		fullName = "{0} - {1}".format(fullName,  programmename)
	if startdatetime > 0 and enddatetime > 0:
		fullName = '{0} [{1}-{2}]'.format(fullName, datetime.datetime.fromtimestamp(startdatetime).strftime('%H:%M'), datetime.datetime.fromtimestamp(enddatetime).strftime('%H:%M'))
	print '--------- Playing: channel="{0}", name="{1}". ----------'.format(chNum, channelName)
	return streamUrl, fullName, iconimage

def OpenURL(url, headers={}, user_data={}, justCookie=False):
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	
	req.add_header('User-Agent', UA)
	for k, v in headers.items():
		req.add_header(k, v)
	
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	if justCookie == True:
		if response.info().has_key("Set-Cookie"):
			return response.info()['Set-Cookie']
		return None
	
	return link
	
def GetChannelHtml(chNum):
	url1 = 'http://www.filmon.com/tv/htmlmain'
	url2 = 'http://www.filmon.com/ajax/getChannelInfo'
	
	cookie = OpenURL(url1, justCookie=True)
	headers = {'X-Requested-With': 'XMLHttpRequest', 'Connection': 'Keep-Alive', 'Cookie': cookie}
	user_data = {'channel_id': chNum}

	return OpenURL(url2, headers, user_data)
	
def GetChannelJson(chNum):
	html = GetChannelHtml(chNum)
	resultJSON = _json.loads(html)
	if len(resultJSON) < 1 or not resultJSON[0].has_key("title"):
		return None
	return resultJSON[0]
	
def GetNowPlaying(prms, chNum, referrerCh=None, ChName=None):
	iconimage = 'http://static.filmon.com/couch/channels/{0}/extra_big_logo.png'.format(chNum)
	programmename = ""
	description = ""
	startdatetime = 0
	enddatetime = 0
	
	if referrerCh <> None:
		channelName = ChName
		playPath = '{0}.high.stream'.format(chNum)
	else:
		channelName = prms["title"]

		if not prms.has_key("now_playing") or len(prms["now_playing"]) < 1:
			if prms.has_key("description"):
				description = prms["description"]
		else:
			now_playing = prms["now_playing"]
			startdatetime = int(prms["now_playing"]["startdatetime"])
			enddatetime = int(prms["now_playing"]["enddatetime"])
			description = prms["now_playing"]["programme_description"]
			programmename = prms["now_playing"]["programme_name"]

		playPath = prms["streamName"].replace('low','high')
	
	url = prms["serverURL"]

	i = url.find('/', 7)
	app = url[i+1:]

	swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
	streamUrl = "{0} app={1} playpath={2} swfUrl={3} swfVfy=true live=true".format(url, app, playPath, swfUrl)
	
	return channelName, programmename, description, iconimage, streamUrl, startdatetime, enddatetime
