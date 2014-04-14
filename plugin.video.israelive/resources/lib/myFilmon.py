import sys, datetime, xbmcgui, random
import urllib, urllib2
isNewPython = True if sys.version_info >=  (2, 7) else False
if isNewPython:
	import json as _json
else:
	import simplejson as _json

filmonMainUrl = 'http://www.filmon.com/tv/htmlmain'
filmonChannelUrl = 'http://www.filmon.com/ajax/getChannelInfo'
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
	
def GetChannelDetails(prms, chNum, referrerCh=None, ChName=None, forM3U=False):
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
	
	if (forM3U):
		streamUrl = "{0} app={1} playpath={2} swfUrl={3} swfVfy=true pageUrl={4} live=true".format(url, app, playPath, swfUrl, pageUrl)
	else:
		streamUrl = "{0} tcUrl={0} app={1} playpath={2} swfUrl={3} swfVfy=true pageUrl={4} live=true".format(url, app, playPath, swfUrl, pageUrl)
	
	return channelName, channelDescription, iconimage, streamUrl, tvGuide

def MakeM3ULinks(scanChList, dp, isIptvAddonGotham):
	M3Ulist = '#EXTM3U\n'
	errorLog = ''

	try:
		cookie = OpenURL(filmonMainUrl, justCookie=True)
		if cookie == None:
			raise
		headers = {'X-Requested-With': 'XMLHttpRequest', 'Connection': 'Keep-Alive', 'Cookie': cookie}
	except:
		return None, "Cannot connect to server. :-("
			
	channelsCount = len(scanChList)
	
	random.seed()
	random.shuffle(scanChList)
	
	i = 0
	for channel in scanChList: 
		i = i + 1
		user_data = {'channel_id': channel['chNum']}
		
		if dp.iscanceled(): 
			return None, "Canceled by user."
			
		percent = i * 100 // channelsCount 
		progress = "{0} of {1}".format(i, channelsCount)

		try:
			response = OpenURL(filmonChannelUrl, headers, user_data)
			resultJSON = _json.loads(response)
			if len(resultJSON) < 1 or not resultJSON[0].has_key("title"):
				raise
			dp.update(percent, line2=progress, line3="{0}... Done.".format(channel['chName']))
			print "{0} of {1} [{2}. {3}]... Done. :-)".format(i, channelsCount, channel['chNum'], channel['chName'])
		except:
			dp.update(percent, line2=progress, line3="{0}... Faild.".format(channel['chName']))
			print "{0} of {1} [{2}. {3}]... Faild. :-(".format(i, channelsCount, channel['chNum'], channel['chName'])
			errorLog += "{0}. {1}\n".format(channel['chNum'], channel['chName'])
			continue

		channelName, channelDescription, iconimage, streamUrl, tvGuide = GetChannelDetails(resultJSON[0], channel['chNum'], forM3U=True)
		
		chID = "fil-{0}".format(channel['chNum'])
		#M3Ulist += '#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" tvg-logo="{2}" group-title="{3}",{4}\n{5}\n'.format(chID, channelName.replace(' ','_'), iconimage.replace('.png',''), "Filmon", channelName, streamUrl)
		#M3Ulist += '\n#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" group-title="{2}",{3}\n{4}\n'.format(chID, channelName.replace(' ','_'), channel['group'], channelName, streamUrl)
		if isIptvAddonGotham:
			M3Ulist += '\n#{5}#\n#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" group-title="{2}" tvg-logo="{3}.png",{3}\n{4}\n'.format(chID, channel['chName'].replace(' ','_'), channel['group'], channel['chName'], streamUrl, channel['index'])
		else:
			M3Ulist += '\n#{5}#\n#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" group-title="{2}",{3}\n{4}\n'.format(chID, channel['chName'].replace(' ','_'), channel['group'], channel['chName'], streamUrl, channel['index'])
		
	return "{0}\n".format(M3Ulist), errorLog
	
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
	cookie = OpenURL(filmonMainUrl, justCookie=True)
	if cookie == None:
		return None
	headers = {'X-Requested-With': 'XMLHttpRequest', 'Connection': 'Keep-Alive', 'Cookie': cookie}
	user_data = {'channel_id': chNum}
	return OpenURL(filmonChannelUrl, headers, user_data)
	
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