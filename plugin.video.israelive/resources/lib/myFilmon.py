import re, time
import urllib, urllib2, json

def GetUrlStream(url, filmonOldStrerams=True, useRtmp=False):
	chNum, referrerCh, filmonMethod = GetUrlParams(url)
	if filmonMethod is not None:
		filmonOldStrerams = (filmonMethod == 0)
	return GetChannelStream(chNum, referrerCh, filmonOldStrerams, useRtmp)

def GetChannelStream(chNum, referrerCh=None, filmonOldStrerams=True, useRtmp=False):
	if referrerCh == None:
		prms = GetChannelJson(chNum, filmonOldStrerams)
	else:
		prms = GetChannelJson(referrerCh, filmonOldStrerams)
		
	if prms == None:
		print '--------- Playing Error: there is no channel with id="{0}" ---------'.format(chNum)
		return None
		
	selectedStream = None
	for stream in prms['streams']:
		if stream ['quality'].lower() == "low":
			selectedStream = stream
			break
			
	url = GetFilmonStream(selectedStream, useRtmp=useRtmp)
	
	if url is None:
		return None
		
	url = url.replace('low','high')
		
	if referrerCh != None:
		url = url.replace("{0}.".format(referrerCh), "{0}.".format(chNum))
		
	return url

def GetUrlGuide(url, days):
	chNum, referrerCh, filmonMethod = GetUrlParams(url)
	if referrerCh is not None:
		return None
	return MakeChannelGuide(chNum, days)

def MakeChannelGuide(chNum, days):
	now = int(time.time())
	days = now + 86400*days
	html = OpenURL("http://www.filmon.com/api-v2/tvguide/{0}".format(chNum))
	if html is None:
		return []
		
	prms = json.loads(html.decode("utf-8"))
	programmes = prms["data"]
	
	programmename = ""
	description = ""
	startdatetime = 0
	enddatetime = 0
	tvGuide = []
	
	for programme in programmes:
		startdatetime = int(programme["startdatetime"])
		enddatetime = int(programme["enddatetime"])
		if now > enddatetime:
			continue
		if startdatetime > days:
			break
		description = programme["programme_description"]
		programmename = programme["programme_name"]
		image = None if not programme.has_key("images") or programme["images"] is None or len(programme["images"]) == 0 else programme["images"][0]["url"]
		tvGuide.append({"start": startdatetime, "end": enddatetime, "name": programmename.encode('utf-8'), "description": description.encode('utf-8'), "image": image})
		
	return tvGuide

def OpenURL(url, headers={}, justCookie=False):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
	for k, v in headers.items():
		req.add_header(k, v)
	
	try:
		response = urllib2.urlopen(req)
	except:
		return None
	
	if justCookie == True:
		if response.info().has_key("Set-Cookie"):
			data = response.info()['Set-Cookie']
		else:
			data = None
	else:
		try:
			data = response.read()
		except:
			return None
	
	response.close()
	return data

def GetChannelParams(html):
	resultJSON = None
	try:
		resultJSON = json.loads(html)
		if len(resultJSON) < 1 or (not resultJSON.has_key("streams") and not resultJSON.has_key("serverURL")):
			return None
	except:
		pass
		
	return resultJSON

def GetChannelJson(chNum, filmonOldStrerams=True):
	html = None
	if filmonOldStrerams:
		html = OpenURL("http://www.filmon.com/api/init/")
		if html is not None:
			resultJSON = json.loads(html)
			session_key = resultJSON["session_key"]
			html = OpenURL("http://www.filmon.com/api/channel/{0}?session_key={1}".format(chNum , session_key))
		
	if html is None:
		if filmonOldStrerams:
			print "---------------------------- Trying filmonNewStrerams method for chNum {0} ----------".format(chNum)
		cookie = OpenURL('http://www.filmon.com/tv/htmlmain', justCookie=True)
		if cookie is not None:
			headers = {'X-Requested-With': 'XMLHttpRequest', 'Connection': 'Keep-Alive', 'Cookie': cookie}
			html = OpenURL('http://www.filmon.com/ajax/getChannelInfo?channel_id={0}'.format(chNum), headers)
		if html is None:
			return None
	
	return GetChannelParams(html)

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
	filmonMethod = None
	
	try:
		chNum = int(params["url"])
	except:
		pass
	try:
		referrerCh = int(params["referrerch"])
	except:
		pass
	try:
		filmonMethod = int(params["filmonmethod"])
	except:
		pass
		
	return chNum, referrerCh, filmonMethod

def GetFilmonStream(selectedStream, useRtmp=True):
	url = selectedStream['url']
	if url is None:
		return None
		
	if "rtmp" in url:
		streamUrl = selectedStream['url'] + '<'
		streamName = selectedStream['name'].replace("low", "high")

		if not useRtmp and not re.search('mp4', streamName, re.IGNORECASE):
			regx = re.compile('rtmp://(.+?)\?id=(.+?)<')
			match = regx.search(streamUrl)
			url = "http://{0}{1}/playlist.m3u8?id={2}".format(match.group(1), streamName, match.group(2))
		else:
			if re.search('mp4', streamName, re.IGNORECASE):
				regx = re.compile('rtmp://(.+?)/(.+?)/(.+?)/<')
				match = regx.search(streamUrl)
				app = '{0}/{1}/'.format(match.group(2), match.group(3))
				swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
				url = "{0}{1}".format(selectedStream['url'], streamName)
				
			if re.search('m4v', streamName, re.IGNORECASE):
				app = 'vodlast'
				swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
				url = "{0}/{1}".format(selectedStream['url'], streamName)
			else:
				try:
					regx = re.compile('rtmp://(.+?)/live/(.+?)id=(.+?)<')
					match = regx.search(streamUrl)
					app = 'live/{0}id={1}'.format(match.group(2), match.group(3))
					url = selectedStream['url']
					swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
				except:
					pass
				try:
					regx = re.compile('rtmp://(.+?)/(.+?)id=(.+?)"')
					match = regx.search(streamUrl)
					app = '{0}id={1}'.format(match.group(2), match.group(3))
					swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=28'
				except:
					pass
				try:
					regx = re.compile('rtmp://(.+?)/(.+?)/<')
					match = regx.search(streamUrl)
					app = '{0}/'.format(match.group(2))
					url = "{0}/{1}".format(selectedStream['url'], streamName)
					swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
				except:
					pass
					
			tcUrl = selectedStream['url']
			url = "{0} playpath={1} app={2} swfUrl={3} tcUrl={4} pageurl=http://www.filmon.com/ live=true timeout=45 swfVfy=true".format(url, streamName, app, swfUrl, tcUrl)
	elif useRtmp:
		url2 = url.split('/')
		urlrtmp = "rtmp://%s/live/%s" % (url2[2],url2[5].replace('playlist.m3u8',''))
		playpath = url2[4].replace('.l.stream', '.low.stream').replace('.lo.stream', '.low.stream')
		swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
		url = "{0}/{1} playpath={1} swfUrl={2} pageUrl=http://www.filmon.com/ live=true timeout=45 swfVfy=true".format(urlrtmp, playpath, swfUrl)
		
	return url
	