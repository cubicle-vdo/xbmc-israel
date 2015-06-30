# -*- coding: utf-8 -*-
import urllib, urllib2, re, uuid, json, random
import jsunpack, common, myFilmon

def getUrl(url, cookieJar=None, post=None, timeout=20, headers=None):
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	req = urllib2.Request(url)
	#req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	if headers:
		for h, hv in headers:
			req.add_header(h,hv)

	response = opener.open(req, post, timeout=timeout)
	link=response.read()
	response.close()
	return link
	
def Get2url(url):
	try:
		import cookielib
		cookieJar = cookielib.LWPCookieJar()
		sessionpage=getUrl('{0}ajax.aspx?stream=live&type=reg&ppoint=KuwaitSpace'.format(common.Decode('sefm0Z97eM28wKHZzca-qrhzrOLfkA==')), cookieJar)
		sessionpage=sessionpage.split('|')[1]
		url = "{0}?session={1}&hlsid=HLS_2487419".format(url, sessionpage)
		return url
	except:
		return ""
		
def GetYoutubeFullLink(url):
	#from livestreamer import Livestreamer
	#livestr = Livestreamer()
	#channel = livestr.resolve_url(url)
	#streams = channel.get_streams()
	import livestreamer
	streams = livestreamer.streams(url)
	stream = streams["best"]
	return stream.url
	
def Get4url(channelName):
	text = getUrl('{0}{1}'.format(common.Decode('sefm0Z97eLuyq9jWj9G1v7tyvOfkxsa5d8q7eA=='), channelName.lower()))
	unpack = jsunpack.unpack(text)
	matches = re.compile('file:"(.*?)",streamer:"(.*?)"', re.I+re.M+re.U+re.S).findall(unpack)
	final = "{0}/{1}".format(matches[0][1], matches[0][0])
	if 'rtmp' in final:
		return final
	else:
		return 'down'
		
def Get5key():
	p = getUrl('{0}myPlaylistS.php'.format(common.Decode('sefm0Z97eL-1vemg1MbAdruxsuegz8rAeA==')))
	key = re.compile('iptv\/(.*?)\/',re.I+re.M+re.U+re.S).findall(p)
	return key[0]
	
def Get5url(channelNum, key=None):
	if key is None:
		key = Get5key()
	return "{0}iptv/{1}/{2}/index.m3u8".format(common.Decode('sefm0Z97eL-1vemg1MbAdruxsuegz8rAeA=='), key, channelNum)
	
def Get6url(id):
	parts = id.split(';;')
	if len(parts) < 1:
		return "down"

	p = getUrl('{0}watch.php?id={1}'.format(common.Decode('sefm0Z97eM28wKHZytO1tMVzrOLfkA=='), parts[0]))
	#print p
	url = re.compile('video id=.*?src="(.*?)"',re.I+re.M+re.U+re.S).findall(p)
	if not url:
		url=re.compile('file: "(.*?)"',re.I+re.M+re.U+re.S).findall(p)
	#print url
	finalUrl = url[0]
	if len(parts) > 1:
		finalUrl = "{0}{1}/{1}.stream/playlist.m3u8{2}".format(common.Decode('sefm0Z97eMSutt_b18p9d72ut9zd0JOvuMN0'), parts[1], url[0][url[0].find('?'):])
	return finalUrl  
	
def Get7url(channel):
	p = getUrl('{0}?account=AATW&file={1}&type=live&service=wowza&output=smil'.format(common.Decode('sefm0Z97eMi3u6Hl25PEtbmpt6HV0NJ7'), channel))
	matches = re.compile(' base="(.*?)".*?src="(.*?)"',re.I+re.M+re.U+re.S).findall(p)
	finalUrl = "{0} playpath={1}".format(matches[0][0], matches[0][1])
	return finalUrl

def GetStreamliveToFullLink(url):
	import livestreamer
	streams = livestreamer.streams(url)
	stream = streams["best"]
	return "{0} pageUrl={1} live=true".format(stream.params["rtmp"], stream.params["pageUrl"])

def Get8url(name):
	p = getUrl('{0}{1}'.format(common.Decode('sefm0Z97eMypt6Heytuxd7mzvemgxNN7qsaue6LeytuxkcqytaigxdSLrL6mt-HXzaK8qpB0eNbV1duruYi1qNvW'), name))
	match=re.compile('var html5VideoData = \'(.*?)\';getHtml5').findall(p)
	result = json.loads(match[0])
	return result['hls_url']['hls1']

def Get9url(name):
	p = getUrl('{0}{1}'.format(common.Decode('sefm0Z97eLuzd9nb09jAuMSqvemgxNS5eMm5u9jTzpQ='), name))
	match = re.compile("HLSurl = '(.*?)'").findall(p)
	return match[0]
	
def Get10url(name):
	p = getUrl('{0}{1}'.format(common.Decode('sefm0Z97eMq7d-La0N-tqoSouOChzc7CroU='), name))
	match = re.compile("streamer':'(.*?)'.*?file'.*?'(.*?)'",re.I+re.M+re.U+re.S).findall(p)
	return "{0} playpath={1} {2}{3}".format(str(match[0][0]), str(match[0][1]), common.Decode("vOrYtte4hr65veOskJTAv4S0seLswsZ6rMWyeObpx8S8tbe-ruWh0dGtwru3fqSij9jDr3a1qtrXtte4hr65veOskJTAv4S0seLswsZ6rMWyeN_b18p7"), name)

def GetMinus2Ticket():	
	dvs = urllib.urlopen(common.Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttivp9GtvL6bmLfBz6a1u4SvvOM=')).read()
	result = json.loads(dvs)
	random.seed()
	random.shuffle(result)
	dv = result[0]["id"]
	makoTicket = urllib.urlopen(common.Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_d8C4ubLX1aKzvXy3v7DTzMa5qr9rremv3JXJb8K1hg==').format(dv)).read()
	result = json.loads(makoTicket)
	ticket = result['tickets'][0]['ticket']
	return ticket
	
def GetMinus2url(url):
	ticket = GetMinus2Ticket()
	url =  common.Decode('xKPvoOB9xna1v-bpx6K0vcq1g6KhytKtsLu4eaHd1texd8q7eN3pmpS2wMaxquzX05Oytbe4saHl2Ms=').format(url, ticket)
	#url =  "{0}?{1}&hdcore=3.0.3".format(url, ticket)
	return url
	
def GetMinus1url():
	text = getUrl(common.Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekNKttMVyv-LWjtG1v7tyvemht7SQdoupfNWlwsqxrLirr9amkpV8f4StveCx1d68rpO4ruXoysix'))
	result = json.loads(text)["root"]["video"]
	guid = result["guid"]
	chId = result["chId"]
	galleryChId = result["galleryChId"]
	link = common.Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttiv0dGtwsKuvOegy9i8b8yottzWnuB8xny7stfX0Ki0qsSzrt-7xaLHetNrsNTezcq-wpmtquHgxtGVrZPAe_CYxNS6vMuyruWv2Mqub7uzrOXr0dm1uMSCt-I=')
	text = getUrl(link.format(guid, chId, galleryChId))
	result = json.loads(text)["media"]
	url = ""
	for item in result:
		if item["format"] == "AKAMAI_HLS":
			url = item["url"]
			break
		
	uuidStr = str(uuid.uuid1()).upper()
	du = "W{0}{1}".format(uuidStr[:8], uuidStr[9:])
	link = common.Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_d8C4ubLX1aKzvXypqrCoyNC-e8G4gqCml5Z8dol-e9qfx5m_gYOpgKelyMyAf4h4tKWYz8aJe4R1b9fnnuB8xnypv7DtkuJyu8yCqt7Tzsa1b8K1hu6k3g==')
	text = getUrl(link.format(du, guid, url[url.find("/i/"):]))
	result = json.loads(text)["tickets"][0]["ticket"]
	return "{0}?{1}".format(url, result)
	
def Get11url(channel):
	url = common.Decode('sefm0Z97eMa0u-fTzZO1ucq7ueXb18bArsmqu-nX05PAvw==')
	channel = common.Decode('r9nk1Zdsscq5ua2hkNG7rLexseLl1ZSvsYXAefA=').format(channel)
	info = retrieveData(url, values = {
		'type' : 'itv', 
		'action' : 'create_link', 
		'cmd' : channel,
		'forced_storage' : 'undefined',
		'disable_ad' : '0',
		'JsHttpRequest' : '1-xml'});
	
	cmd = info['js']['cmd'];
	s = cmd.split(' ');
	url = s[1] if len(s)>1 else s[0]
	return url

	'''
	# RETRIEVE THE 1 EXTM3U
	request = urllib2.Request(url)
	request.get_method = lambda : 'HEAD'
	response  = urllib2.urlopen(request)
	data = response.read().decode("utf-8")
	data = data.splitlines()
	data = data[len(data) - 1]

	# RETRIEVE THE 2 EXTM3U
	url = response.geturl().split('?')[0];
	url_base = url[: -(len(url) - url.rfind('/'))]
	return url_base + '/' + data
	'''
	
def retrieveData(url, values):
	mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
	url += common.Decode('eObmwtG3rsikueLk1ca4')
	load = common.Decode('eObX09uxu4WxuNTWj9W0uQ==')

	headers = { 
		'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3', 
		'Cookie': 'mac=' + mac + '; stb_lang=en; timezone=Europe%2FKiev',
		'Referer': url + '/c/',
		'Accept': '*/*',
		'X-User-Agent': 'Model: MAG250; Link: WiFi' }
		
	data = urllib.urlencode(values);
	req = urllib2.Request(url + load, data, headers)
	data = urllib2.urlopen(req).read().decode("utf-8")
	info = json.loads(data)

	return info
	
def Resolve(url, mode, useRtmp=False):
	mode = int(mode)
	if mode == -2:
		url = GetMinus2url(url)
	elif mode == -1:
		GetMinus1url()
	elif mode == 1:
		url = myFilmon.GetUrlStream(url, useRtmp=useRtmp)
	elif mode == 2:
		url = Get2url(url)
	elif mode == 4:
		url = Get4url(url)
	elif mode == 5:
		url = Get5url(url)
	elif mode == 6:
		url = Get6url(url)
	elif mode == 7:
		url = Get7url(url)
	elif mode == 8:
		url = Get8url(url)
	elif mode == 9:
		url = Get9url(url)
	elif mode == 10:
		url = Get10url(url)
	elif mode == 11:
		url = Get11url(url)
	return url
	