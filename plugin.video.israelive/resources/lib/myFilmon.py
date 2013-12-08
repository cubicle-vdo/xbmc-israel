import urllib,re,datetime,sys
import requests

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
		pass
	try:      
		ChName = urllib.unquote_plus(params["chname"])
	except:
		ChName = None
		pass
		
	return GetChannelStream(chNum, referrerCh, ChName)

def GetChannelStream(chNum, referrerCh=None, ChName=None):
	if referrerCh == None:
		html = GetChannelHtml(chNum)
		match = re.compile('"title":"(.+?)"').findall(html)
		try:        
			name = match[0]
		except:
			print '--------- Playing Error: there is no channel with id="{0}" ---------'.format(chNum)
			return '',''
			
		fullName = "{0} ".format(name.replace('\\',''))
		match = re.compile('"streamName":"(.+?)"').findall(html)
		playPath = match[0]
		playPath = playPath.replace('\\','').replace('low','high')

		match = re.compile('"server_time":(.*?)}').findall(html)
		server_time = match[0]
	
		match = re.compile('"startdatetime":"(.*?)","enddatetime":"(.*?)"(.+?)"programme_name":"(.*?)"').findall(html)

		for startdatetime, enddatetime, ignore, programmename in match:
			if (int(server_time) > int(startdatetime) and int(server_time) < int(enddatetime)):
				startdatetime = datetime.datetime.fromtimestamp(int(startdatetime)).strftime('%H:%M')
				enddatetime = datetime.datetime.fromtimestamp(int(enddatetime)).strftime('%H:%M')
				programmename = '{0} [{1}-{2}]'.format(programmename, startdatetime, enddatetime)
				fullName = "[B]{0}[/B]- {1} ".format(fullName, programmename)
				break
				
	else:
		html = GetChannelHtml(referrerCh)
		fullName = name = "{0} ".format(ChName.replace('\\',''))
		playPath = '{0}.high.stream'.format(chNum)
	
	print '--------- Playing: ch="{0}", name="{1}" ----------'.format(chNum, name)
	
	match = re.compile('"serverURL":"(.+?)"').findall(html)
	url = match[0]
	url = url.replace('\\','')

	i = url.find('/', 7)
	app = url[i+1:]

	swfUrl = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'

	fullUrl = "{0} app={1} playpath={2} swfUrl={3} swfVfy=true live=true".format(url, app, playPath, swfUrl)
	
	return fullUrl, fullName

def GetChannelHtml(chNum):
	url1 = 'http://www.filmon.com/tv/htmlmain'
	url2 = 'http://www.filmon.com/ajax/getChannelInfo'
	user_data = {'channel_id': chNum}
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0', 'X-Requested-With': 'XMLHttpRequest', 'Connection': 'Keep-Alive'}

	with requests.session() as s:
		s.get(url1)
		response = s.post(url2, data = user_data, headers = headers)

	return response.text
	