import sys, datetime
import urllib, urllib2
if sys.version_info >=  (2, 7):
	import json as _json
else:
	import simplejson as _json

UA = 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0'

def GetUrlStream(url):
	chNum, referrerCh, ChName = GetUrlParams(url)
	return GetChannelStream(chNum, referrerCh, ChName)

def GetChannelStream(chNum, referrerCh=None, ChName=None):
	if referrerCh == None:
		prms = GetChannelJson(chNum)
	else:
		prms = GetChannelJson(referrerCh)
		
	if prms == None:
		print '--------- Playing Error: there is no channel with id="{0}" ---------'.format(chNum)
		return None,None,None,None
		
	channelName, channelDescription, iconimage, streamUrl, tvGuide = GetChannelDetails(prms, chNum, referrerCh, ChName)

	channelName = "[B]{0}[/B]".format(channelName)
	
	if len(tvGuide) > 0:
		programme = tvGuide[0]
		programmeName = '[B]{0}[/B] [{1}-{2}]'.format(programme[2], datetime.datetime.fromtimestamp(programme[0]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programme[1]).strftime('%H:%M'))
		#image = programme[4]
		if len(tvGuide) > 1:
			nextProgramme = tvGuide[1]
			channelName = "[COLOR yellow]{0}[/COLOR] - [COLOR white]Next: [B]{1}[/B] [{2}-{3}][/COLOR]".format(channelName, nextProgramme[2], datetime.datetime.fromtimestamp(nextProgramme[0]).strftime('%H:%M'), datetime.datetime.fromtimestamp(nextProgramme[1]).strftime('%H:%M'))
	else:
		programmeName = channelName
		channelName = "[COLOR yellow]{0}[/COLOR]".format(channelName)
		#image = iconimage

	print '--------- Playing: ch="{0}", name="{1}" ----------'.format(chNum, channelName)
	return streamUrl, channelName, programmeName, iconimage #, image

def GetChannelGuide(chNum):
	prms = GetChannelJson(chNum)
	if prms == None:
		return None,None,None,None
		
	channelName, channelDescription, iconimage, streamUrl, tvGuide = GetChannelDetails(prms, chNum)
	return channelName, channelDescription, iconimage, tvGuide
	
def GetChannelDetails(prms, chNum, referrerCh=None, ChName=None):
	iconimage = 'http://static.filmon.com/couch/channels/{0}/extra_big_logo.png'.format(chNum)
	pageUrl = "http://www.filmon.com/"
	swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
	url = prms["serverURL"]
	i = url.find('/', 7)
	app = url[i+1:]
	
	channelName = ""
	channelDescription = ""
	tvGuide = []
	
	if referrerCh <> None:
		channelName = ChName
		playPath = '{0}.high.stream'.format(chNum)
	else:
		channelName = prms["title"].encode('utf-8')
		if prms.has_key("description"):
			channelDescription = prms["description"].encode('utf-8')
		playPath = prms["streamName"].replace('low','high')
		
		programmename = ""
		description = ""
		startdatetime = 0
		enddatetime = 0
	
		server_time = int(prms["server_time"])
		if prms.has_key("tvguide") and len(prms["tvguide"]) > 1:
			tvguide = prms["tvguide"]
			for prm in tvguide:
				startdatetime = int(prm["startdatetime"])
				enddatetime = int(prm["enddatetime"])
				if server_time > enddatetime:
					continue
				description = prm["programme_description"]
				programmename = prm["programme_name"]
				image = None if not prm.has_key("images") or len(prm["images"]) == 0 else prm["images"][0]["url"]
				tvGuide.append((startdatetime, enddatetime, programmename.encode('utf-8'), description.encode('utf-8'), image))
		elif prms.has_key("now_playing") and len(prms["now_playing"]) > 0:
			now_playing = prms["now_playing"]
			startdatetime = int(now_playing["startdatetime"])
			enddatetime = int(now_playing["enddatetime"])
			
			if startdatetime < server_time and server_time < enddatetime:
				description = now_playing["programme_description"]
				programmename = now_playing["programme_name"]
				image = None if not prms.has_key("images") or len(prms["images"]) == 0 else prms["images"][0]["url"]
				tvGuide.append((startdatetime, enddatetime, programmename.encode('utf-8'), description.encode('utf-8'), image))
	
	streamUrl = "{0} tcUrl={0} app={1} playpath={2} swfUrl={3} swfVfy=true pageUrl={4} live=true".format(url, app, playPath, swfUrl, pageUrl)
	return channelName, channelDescription, iconimage, streamUrl, tvGuide

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
	
	if justCookie == True:
		if response.info().has_key("Set-Cookie"):
			data = response.info()['Set-Cookie']
		else:
			data = None
	else:
		data = response.read()
	
	response.close()
	return data
	
def GetChannelHtml(chNum):
	url1 = 'http://www.filmon.com/tv/htmlmain'
	url2 = 'http://www.filmon.com/ajax/getChannelInfo'
	
	cookie = OpenURL(url1, justCookie=True)
	if cookie == None:
		return None
	headers = {'X-Requested-With': 'XMLHttpRequest', 'Connection': 'Keep-Alive', 'Cookie': cookie}
	user_data = {'channel_id': chNum}

	return OpenURL(url2, headers, user_data)
	
def GetChannelJson(chNum):
	html = GetChannelHtml(chNum)
	resultJSON = _json.loads(html)
	if len(resultJSON) < 1 or not resultJSON[0].has_key("title"):
		return None
	return resultJSON[0]

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
	
def GetUrlParams(url):
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
	return 	chNum, referrerCh, ChName