import re, random, time
import urllib, urllib2, json
import common

AddonID = "plugin.video.israelive"

def GetUrlStream(url, filmonOldStrerams=False, useRtmp=False):
	chNum, referrerCh, ChName, filmonMethod = GetUrlParams(url)
	if filmonMethod is not None:
		filmonOldStrerams = (filmonMethod == 0)
	return GetChannelStream(chNum, referrerCh, ChName, filmonOldStrerams, useRtmp)

def GetChannelStream(chNum, referrerCh=None, ChName=None, filmonOldStrerams=False, useRtmp=False):
	if referrerCh == None:
		prms = GetChannelJson(chNum, filmonOldStrerams)
	else:
		prms = GetChannelJson(referrerCh, filmonOldStrerams)
		
	if prms == None:
		print '--------- Playing Error: there is no channel with id="{0}" ---------'.format(chNum)
		return None,None,None,None
		
	channelName, channelDescription, iconimage, streamUrl, tvGuide = GetChannelDetails(prms, chNum, referrerCh, ChName, filmonOldStrerams, useRtmp)
	
	#print '--------- Playing: ch="{0}", name="{1}" ----------'.format(chNum, channelName)
	#return streamUrl, channelName, programmeName, iconimage #, image
	return streamUrl, channelName, iconimage, tvGuide

def GetChannelGuide(chNum, filmonOldStrerams=False):
	prms = GetChannelJson(chNum, filmonOldStrerams)
	if prms == None:
		return None,None,None,None
		
	channelName, channelDescription, iconimage, streamUrl, tvGuide = GetChannelDetails(prms, chNum, filmonOldStrerams=filmonOldStrerams)
	return channelName, channelDescription, iconimage, tvGuide

def MakeChannelGuide(prms):
	tvGuide = []

	server_time = int(prms["server_time"]) if prms.has_key("server_time") else int(time.time())
		
	programmename = ""
	description = ""
	startdatetime = 0
	enddatetime = 0

	if prms.has_key("tvguide") and len(prms["tvguide"]) > 1:
		tvguide = prms["tvguide"]
		for prm in tvguide:
			startdatetime = int(prm["startdatetime"])
			enddatetime = int(prm["enddatetime"])
			if server_time > enddatetime:
				continue
			description = prm["programme_description"]
			programmename = prm["programme_name"]
			image = None if not prm.has_key("images") or len(prm["images"]) == 0 or not prm["images"][0].has_key("url") else prm["images"][0]["url"]
			tvGuide.append({"start": startdatetime, "end": enddatetime, "name": programmename.encode('utf-8'), "description": description.encode('utf-8'), "image": image})
	elif prms.has_key("now_playing") and len(prms["now_playing"]) > 0:
		now_playing = prms["now_playing"]
		startdatetime = int(now_playing["startdatetime"])
		enddatetime = int(now_playing["enddatetime"])
		
		if startdatetime < server_time and server_time < enddatetime:
			description = now_playing["programme_description"]
			programmename = now_playing["programme_name"]
			image = None if not now_playing.has_key("images") or len(now_playing["images"]) == 0 or not now_playing["images"][0].has_key("url") else now_playing["images"][0]["url"]
			tvGuide.append({"start": startdatetime, "end": enddatetime, "name": programmename.encode('utf-8'), "description": description.encode('utf-8'), "image": image})
			if prms.has_key("next_playing") and len(prms["next_playing"]) > 0:
				next_playing = prms["next_playing"]
				startdatetime = int(next_playing["startdatetime"])
				enddatetime = int(next_playing["enddatetime"])
				description = next_playing["programme_description"]
				programmename = next_playing["programme_name"]
				image = None if not next_playing.has_key("images") or len(next_playing["images"]) == 0 or not next_playing["images"][0].has_key("url") else next_playing["images"][0]["url"]
				tvGuide.append({"start": startdatetime, "end": enddatetime, "name": programmename.encode('utf-8'), "description": description.encode('utf-8'), "image": image})
			
	return tvGuide
			
def GetChannelDetails(prms, chNum, referrerCh=None, ChName=None, filmonOldStrerams=False, useRtmp=False):
	channelName = ""
	channelDescription = ""
	iconimage = 'http://static.filmon.com/couch/channels/{0}/extra_big_logo.png'.format(chNum)
	url = None
	tvGuide = []
	
	if filmonOldStrerams:
		url = GetFilmonOldStreram(prms['streams'], useHls=not useRtmp)
	else:
		url = prms["serverURL"]
		if useRtmp:
			url = hls2rtmp(url)
		
	streamUrl = None if url is None else url.replace('low','high')
		
	if referrerCh == None:
		tvGuide = MakeChannelGuide(prms)
		channelName = prms["title"].encode("utf-8")
	else:
		streamUrl = streamUrl.replace("{0}.".format(referrerCh), "{0}.".format(chNum))
		channelName = ChName
		
	return channelName, channelDescription, iconimage, streamUrl, tvGuide

def OpenURL(url, headers={}, user_data={}, justCookie=False):
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
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
		data = response.read()
	
	response.close()
	return data
	
def getCookie():
	return OpenURL('http://www.filmon.com/tv/htmlmain', justCookie=True)
	
def getChannelHtml(cookie, chNum):
	headers = {'X-Requested-With': 'XMLHttpRequest', 'Connection': 'Keep-Alive', 'Cookie': cookie}
	user_data = {'channel_id': chNum}
	return OpenURL('http://www.filmon.com/ajax/getChannelInfo', headers, user_data)
	
def GetChannelParams(html):
	resultJSON = None
	try:
		resultJSON = json.loads(html)
		if len(resultJSON) < 1 or not resultJSON.has_key("title"):
			return None
	except:
		pass
		
	return resultJSON
	
def GetChannelJson(chNum, filmonOldStrerams=False):
	if filmonOldStrerams:
		html = OpenURL("http://www.filmon.com/api/init/")
		if html is None:
			return None
		resultJSON = json.loads(html)
		session_key = resultJSON["session_key"]
		html = OpenURL("http://www.filmon.com/api/channel/{0}?session_key={1}".format(chNum , session_key))
	else:
		cookie = getCookie()
		if cookie == None:
			return None
		html =  getChannelHtml(cookie, chNum)

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
	ChName = None
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
		ChName = str(params["chname"])
	except:
		pass
	try:
		filmonMethod = int(params["filmonmethod"])
	except:
		pass
		
	return chNum, referrerCh, ChName, filmonMethod
	
def GetFilmonOldStreram(streams, useHls=False):
	selectedStream = None
	for stream in streams:
		if stream ['quality'].lower() == "low":
			selectedStream = stream
			break

	if selectedStream is not None:
		streamUrl = selectedStream['url'] + '<'
		streamName = selectedStream['name'].replace("low", "high")
		
		if useHls:
			regx = re.compile('rtmp://(.+?)\?id=(.+?)<')
			match = regx.search(streamUrl)
			return "http://{0}{1}/playlist.m3u8?id={2}".format(match.group(1), streamName, match.group(2))

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
	return url
	
def hls2rtmp(urlhls):
	url2 = urlhls.split('/')
	urlrtmp = "rtmp://%s/live/%s" % (url2[2],url2[5].replace('playlist.m3u8',''))
	playpath = url2[4].replace('.l.stream', '.low.stream').replace('.lo.stream', '.low.stream')
	swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
	urlrtmp = "{0}/{1} playpath={1} swfUrl={2} pageUrl=http://www.filmon.com/ live=true timeout=45 swfVfy=true".format(urlrtmp, playpath, swfUrl)
	return urlrtmp
	
def GetFilmonChannelsList():
	list = []
	
	try:
		list1 = common.GetListFromPlx(includeCatNames=False, fullScan=True)
		for item in list1:
			if item["type"] == 'video':
				url = item['url']
				if url.find(AddonID) > 0:
					channel = re.compile('url=([0-9]*).*?mode=1(.*?)$',re.I+re.M+re.U+re.S).findall(url)
					if len(channel) > 0 and channel[0][0] != "" and channel[0][1].find("&ignorefilmonguide=1") < 0:
						list.append({"channel": int(channel[0][0]), "name": item["name"]})
	except:
		pass
		
	return list

def MakePLXguide(filmonGuideFile):
	filmonlist = GetFilmonChannelsList()
	if filmonlist == []:
		return False

	randList =  [{ "index": filmonlist.index(item), "channel": item["channel"]} for item in filmonlist]
	random.seed()
	random.shuffle(randList)

	#cookie = OpenURL('http://www.filmon.com/tv/htmlmain', justCookie=True)
	#if cookie == None:
	#	return
	html = OpenURL("http://www.filmon.com/api/init/")
	if html is None:
		return False
	resultJSON = json.loads(html)
	session_key = resultJSON["session_key"]

	for item in randList:
		prms = None
		#html =  getChannelHtml(cookie, item["channel"])
		html = OpenURL("http://www.filmon.com/api/channel/{0}?session_key={1}".format(item["channel"] , session_key))
		if html is not None:
			prms = GetChannelParams(html)

		tvGuide = [] if prms is None else MakeChannelGuide(prms)
		filmonlist[item["index"]] = {"channel": filmonlist[item["index"]]["name"], "tvGuide": tvGuide}
			
	with open(filmonGuideFile, 'w') as outfile:
		json.dump(filmonlist, outfile) 
	outfile.close()
	
	return True
	