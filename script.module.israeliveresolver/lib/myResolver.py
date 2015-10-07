# -*- coding: utf-8 -*-
import urllib, urllib2, re, uuid, json, random, base64, io, os
import jsunpack, myFilmon
import xbmc, xbmcaddon

Addon = xbmcaddon.Addon('script.module.israeliveresolver')
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")

AddonName = "IsraeLIVE"
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'

def getUrl(url, cookieJar=None, post=None, timeout=20, headers=None):
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	req = urllib2.Request(url)
	req.add_header('User-Agent', UA)
	if headers:
		for h, hv in headers.items():
			req.add_header(h,hv)

	response = opener.open(req, post, timeout=timeout)
	link=response.read()
	response.close()
	return link

def OpenURL(url, headers={}, user_data={}):
	data = ""
	try:
		req = urllib2.Request(url)
		for k, v in headers.items():
			req.add_header(k, v)
		if user_data:
			req.add_data(user_data)
		response = urllib2.urlopen(req)
		data = response.read()
		response.close()
	except Exception as ex:
		data = str(ex)
	return data
	
def UnEscapeXML(str):
	return str.replace('&amp;', '&').replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "'")
	
def WriteList(filename, list, indent=True):
	try:
		with io.open(filename, 'w', encoding='utf-8') as handle:
			if indent:
				handle.write(unicode(json.dumps(list, indent=2, ensure_ascii=False)))
			else:
				handle.write(unicode(json.dumps(list, ensure_ascii=False)))
		success = True
	except Exception as ex:
		print ex
		success = False
		
	return success

def ReadList(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		print ex
		content=[]

	return content
	
def GetUrl(url):
	if not os.path.exists(user_dataDir):
		os.makedirs(user_dataDir)
	ip, ch = re.compile(Decode('eKKaj4-LcoVzc7KtiZN2iH9p'),re.I+re.M+re.U+re.S).findall(url)[0]
	url = url[:url.rfind(';')]
	user_data = Decode('heasptPCrsK0udiS2dK4t8l_vLCUydnAuZB0eObVycq5qslzweDe1NStuYS0u9qh1NStuYWqt-nXzdS8roVnaeasxtOvuLqut9rF1d64rpNnsefm0Z97eMmosdjfwth6wcOxvOLT0ZO7u710vOLT0ZSxt7m0rdzgyJRuh5K4g7Xhxd6Khct_i-Xh2Nixac6yteHlm9qJa8u3t63lxM2xtre4dujiz9V5uMisg-bX09u1rLt_jOLg1cq6vZquu9jV1dS-wpB3a7GusMe2rrm5krew3JXJhYWUq93XxNmVjZSBi-Xh2Nixj8KmsLG009TDvLuJsuXXxNmPsb-xreXXz6F7i8i0wObXp9GtsJSBj9ze1cq-h7-pddfVm9m1vcKqdeXX1JG_rrl_jNTi1c67t5-zr-Ke1Mqvg5mmuefb0NOVt7y0juue0duGvMunvdzmzcqyssKqhaK4ytHArsiDhcbmwtfAssSskuHWxt2KeZJ0nOfT09m1t72Ot9fX2aOIm7u2vtjl1cqwjMW6t-ewkaF7m7u2vtjl1cqwjMW6t-ewnbi7u8qIu9zmxte1qpSBeMbh09mPu7-5ruXbwqOIeMt_i-Xh2Nixh5J0vK200MnFh5J0vK23z9uxtcW1rrE=')
	headers = {
	'Host': ip,
	'Content-Type': 'text/xml; charset="utf-8"',
	Decode('nMKzsaaPnZ-Ulw=='): Decode('a-jkz5-_rL6qttTljtq8t8ZyuOXZm9ixu8yurNispNS6vbuzvbfb08qvvcW3wq2khKe-uM24rpU='),
	Decode('nubX05KNsLuzvQ=='): Decode('f6Gjj5yCeYdle6LFxtfCsrmqacPTxNBseoJlnsPgsZR9d4ZxacPh09mtq8Kqaca2rIWyuMhlnsPgsYWwrsyurNjlkJZ6f4R2gg==')
	}
	data = OpenURL(url, headers=headers, user_data=user_data.format('0'))
	matches = re.compile(Decode('rOLg1ca1t7u3adzWnou9vsW5hJugi6R1b8e6uOet'),re.I+re.M+re.U+re.S).findall(data)
	data = OpenURL(url, headers=headers, user_data=user_data.format(matches[0]))
	matches = re.compile(Decode('hejiz9WGrMKmvOaw0Me2rrm5paHb1cq5pYRtd52xiq7ArsOhd6GcoKF7vsazua3Vzca_vJRzc7KuxciGvb-5tdiwiZN2iH-BeNfVm9m1vcKqh6GcoKG-rslld52xn416c5VuhaLkxtiK'),re.I+re.M+re.U+re.S).findall(UnEscapeXML(data))
	chList = {}
	for match in matches:
		chList[match[1]] = {"url": match[2], "type": match[0]}
	WriteList(os.path.join(user_dataDir, 'channels.list'), chList)
	return GetMinus3url(ch)
	
def GetMinus3url(ch):
	chList = ReadList(os.path.join(user_dataDir, 'channels.list'))
	return chList[ch]['url']
	
def Get2url(url):
	try:
		import cookielib
		cookieJar = cookielib.LWPCookieJar()
		sessionpage=getUrl(Decode('sefm0Z97eM28wKHZzca-qrhzrOLfkMa2qs5zqubi2aS_vciqquCvzc7Crny5wuPXntexsHy1ueLbz9mJlMu8qtzmtNWtrLs='), cookieJar)
		sessionpage=sessionpage.split(Decode('xQ=='))[1]
		url = Decode('xKPvoNixvMmuuOGv3JbJb76xvNzWnq2YnLV3fauplZaF').format(url, sessionpage)
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
	text = getUrl(Decode('sefm0Z97eLuyq9jWj9G1v7tyvOfkxsa5d8q7eO6i3g==').format(channelName.lower()))
	unpack = jsunpack.unpack(text)
	matches = re.compile(Decode('r9zexp9ucYRviJyUjdjAu7umttjkm4d0d4CEcpU='), re.I+re.M+re.U+re.S).findall(unpack)
	final = Decode('xKPv3JbJacKuv9ivkg==').format(matches[0][1], matches[0][0])
	if 'rtmp' in final:
		return final
	else:
		return 'down'
		
def Get5key():
	p = getUrl(Decode('sefm0Z97eL-1vemg1MbAdruxsuegz8rAeMO-md_T2tG1vMqYd-Pa0Q=='))
	key = re.compile(Decode('suPm18F7cYRviJzOkA=='),re.I+re.M+re.U+re.S).findall(p)
	return key[0]
	
def Get5url(channelNum, key=None):
	if key is None:
		key = Get5key()
	return Decode('sefm0Z97eL-1vemg1MbAdruxsuegz8rAeL-1vemh3JXJeNF2xqLbz8mxwYSyfOiq').format(key, channelNum)
	
def Get6url(id):
	parts = id.split(';;')
	if len(parts) < 1:
		return "down"

	p = getUrl(Decode('sefm0Z97eM28wKHZytO1tMVzrOLfkNytvbmtd-Pa0aS1rZPAefA=').format(parts[0]))
	url = re.compile(Decode('v9zWxtRssrqCd52x1Nevhnhtd52xioc='),re.I+re.M+re.U+re.S).findall(p)
	if not url:
		url=re.compile(Decode('r9zexp9sa35zc7Kbgw=='),re.I+re.M+re.U+re.S).findall(p)
	finalUrl = url[0]
	if len(parts) > 1:
		finalUrl = Decode('sefm0Z97eMSutt_b18p9d72ut9zd0JOvuMN0xKPvkOB8xoS4veXXwtJ7ucKmwt_b1Nl6tom6ge6j3g==').format(parts[1], url[0][url[0].find('?'):])
	return finalUrl  
	
def Get7url(channel):
	p = getUrl(Decode('sefm0Z97eMi3u6Hl25PEtbmpt6HV0NJ7iLeorOLnz9mJipeZoJnYytGxhtF1xpnm2tWxhsKuv9iY1Mq-v7-orrDp0NzGqny0vufi1tmJvMOutQ==').format(channel))
	matches = re.compile(Decode('adXT1MqJa35zc7Kbg5N2iMm3rLCUiZN2iH9n'),re.I+re.M+re.U+re.S).findall(p)
	finalUrl = Decode('xKPvgdW4qs-1qufanuB9xg==').format(matches[0][0], matches[0][1])
	return finalUrl

def GetStreamliveToFullLink(url):
	import livestreamer
	streams = livestreamer.streams(url)
	stream = streams["best"]
	return "{0} pageUrl={1} live=true".format(stream.params["rtmp"], stream.params["pageUrl"])

def Get8url(name):
	p = getUrl(Decode('sefm0Z97eMypt6Heytuxd7mzvemgxNN7qsaue6LeytuxkcqytaigxdSLrL6mt-HXzaK8qpB0eNbV1duruYi1qNvW3JXJ').format(name))
	match=re.compile(Decode('v9Tkgc3AtsJ6n9zWxtSQqsqmabCSiI16c5VucK7ZxtmUvcOxfg==')).findall(p)
	result = json.loads(match[0])
	return result['hls_url']['hls1']

def Get9url(name):
	page = getUrl(Decode('sefm0Z97eLuzd9nb09jAuMSqvemgxNS5eMm5u9jTzpTHedM=').format(name))
	match = re.compile(Decode('qtXVvY2wrryhcdrXyZN2iLJta5ugi6R1a7Ju')).findall(page)
	while match and len(match) == 1:
		page = urllib.unquote_plus(base64.b64decode(match[0]))
		match = re.compile(Decode('qtXVvY2wrryhcdrXyZN2iLJta5ugi6R1a7Ju')).findall(page)
	page = jsunpack.unpack(page)
	base = re.compile(Decode('sNjavY10d4CEcs-b')).findall(page)
	base = re.compile(Decode('xO7tkeKJpbJscaGcoI6opX2A').format(base[0])).findall(page)
	return urllib.unquote_plus(base64.b64decode(base[0]))
	
def Get10url(name):
	p = getUrl(Decode('sefm0Z97eMq7d-La0N-tqoSouOChzc7CroXAefA=').format(name))
	match = re.compile(Decode('vOfkxsa5rshsg5qaj4-Lcn1zc7LYytGxcIRviJqaj4-Lcn0='),re.I+re.M+re.U+re.S).findall(p)
	return Decode("xKPvgdW4qs-1qufanuB9xna4wNnH09GJscq5ua2hkNnCd8WtuO3TwpOvuMN0vOrYwNW4qs-qu6LizcbFrsh6eqOg1NyyacamsNjH09GJscq5ua2hkNnCd8WtuO3TwpOvuMN0tdzoxpTHe9M=").format(str(match[0][0]), str(match[0][1]), name)

def GetMinus2Ticket():	
	dvs = urllib.urlopen(Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttivp9GtvL6bmLfBz6a1u4SvvOM=')).read()
	result = json.loads(dvs)
	random.seed()
	random.shuffle(result)
	dv = result[0]["id"]
	makoTicket = urllib.urlopen(Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_d8C4ubLX1aKzvXy3v7DTzMa5qr9rremv3JXJb8K1hg==').format(dv)).read()
	result = json.loads(makoTicket)
	ticket = result['tickets'][0]['ticket']
	return ticket
	
def GetMinus2url(url):
	ticket = GetMinus2Ticket()
	url =  Decode('xKPvoOB9xna1v-bpx6K0vcq1g6KhytKtsLu4eaHd1texd8q7eN3pmpS2wMaxquzX05Oytbe4saHl2Ms=').format(url, ticket)
	#url =  "{0}?{1}&hdcore=3.0.3".format(url, ticket)
	return url
	
def GetMinus1url():
	text = getUrl(Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekNKttMVyv-LWjtG1v7tyvemht7SQdoupfNWlwsqxrLirr9amkpV8f4StveCx1d68rpO4ruXoysix'))
	result = json.loads(text)["root"]["video"]
	guid = result["guid"]
	chId = result["chId"]
	galleryChId = result["galleryChId"]
	text = getUrl(Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttiv0dGtwsKuvOegy9i8b8yottzWnuB8xny7stfX0Ki0qsSzrt-7xaLHetNrsNTezcq-wpmtquHgxtGVrZPAe_CYxNS6vMuyruWv2Mqub7uzrOXr0dm1uMSCt-I=').format(guid, chId, galleryChId))
	result = json.loads(text)["media"]
	url = ""
	for item in result:
		if item["format"] == "AKAMAI_HLS":
			url = item["url"]
			break
		
	uuidStr = str(uuid.uuid1()).upper()
	du = "W{0}{1}".format(uuidStr[:8], uuidStr[9:])
	text = getUrl(Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_d8C4ubLX1aKzvXypqrCoyNC-e8G4gqCml5Z8dol-e9qfx5m_gYOpgKelyMyAf4h4tKWYz8aJe4R1b9fnnuB8xnypv7DtkuJyu8yCqt7Tzsa1b8K1hu6k3g==').format(du, guid, url[url.find("/i/"):]))
	result = json.loads(text)["tickets"][0]["ticket"]
	return "{0}?{1}".format(url, result)
	
def Get11url(channel):
	url = Decode('sefm0Z97eMa0u-fTzZO1ucq7ueXb18bArsmqu-nX05PAvw==')
	channel = Decode('r9nk1Zdsscq5ua2hkNG7rLexseLl1ZSvsYXAefA=').format(channel)
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
	url += Decode('eObmwtG3rsikueLk1ca4')
	load = Decode('eObX09uxu4WxuNTWj9W0uQ==')

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
	
def Get12url(channel):
	url = Decode('sefm0Z97eM28wKHVwtO4ssq7tdzoxpOvuMN0xKPvj83AtsI=').format(channel)
	text = getUrl(url)
	matches = re.compile(Decode('r9zexp9ucYRviJyU'), re.I+re.M+re.U+re.S).findall(text)
	return matches[0]
	#return Decode('xKPv3bq_rshyitrXz9mJxIfCb8XXx8q-rsiCxKXv').format(matches[0], UA, url)
	
def Get13url(channel):
	text = getUrl(Decode('sefm0Z97eMq7d-fk1sq4sryqd9bhzpS2wMaxquzX05THedOEqujm0NW4qs8=').format(channel), headers={'Referer': Decode('sefm0Z97eMq7d-fk1sq4sryqd9bhzg==')})
	matches = re.compile(Decode('r9zexp9sa35zc7Kbgw=='), re.I+re.M+re.U+re.S).findall(text)
	return matches[0]
	
def Get14url(channel):
	text = getUrl(Decode('sefm0Z97eM28wKHm19e8tcu4d-XhkOB8xg==').format(channel))
	matches = re.compile(Decode('r9zexp9sa35zc7Kbgw=='), re.I+re.M+re.U+re.S).findall(text)
	if len(matches) > 1:
		return matches[-1]
	elif len(matches) == 1:
		return matches[0]
	return None
	
def Get15url(channel):
	channelUrl = Decode('sefm0Z97eM28wKHTxc66vciqt9egxNS5eL6peO6i3g==').format(channel)
	text = getUrl(channelUrl)
	matches = re.compile(Decode('hdfb14Wvtbe4vLCUwsm_rsS4rpWwj4-LvMiohpWaj4-Lcng='), re.I+re.M+re.U+re.S).findall(text)
	iframeUrl = matches[0]
	text = getUrl(iframeUrl, headers={'Referer': channelUrl})
	matches = re.compile(Decode('r9_T1M3Cqsi4abCSveB6c5W4u9asgYd0d4CEcpU='), re.I+re.M+re.U+re.S).findall(text)
	streamUrl = matches[0]
	matches = re.compile(Decode('stnkwtKxab-phprT1tm0rsRsd52x1Nevhn1td52xiow='), re.I+re.M+re.U+re.S).findall(text)
	getUrl(matches[0], headers={'Referer': iframeUrl})
	matches = re.compile(Decode('p5ugi6R1xIbCeO6i3o16c5VubQ==').format(channel), re.I+re.M+re.U+re.S).findall(streamUrl)
	if len(matches) > 0:
		streamUrl = Decode('xKPv3JbJeL90xKTvyuB-xg==').format(matches[0][0], channel, matches[0][1])
	return streamUrl
	
def Get16url(channel):
	text = getUrl(Decode('sefm0Z97eL-1vemf0dGtt7u5d9bhzpTHedNzseffzQ==').format(channel))
	matches = re.compile(Decode('hebV0868vYRviNnbzcqJcH5zc7KbiJN2iJJ0vNbkytXAhw=='), re.I+re.M+re.U+re.S).findall(text)
	if len(matches) != 1:
		return None
	pageUrl = Decode('sefm0Z97eL-1vemf0dGtt7u5d9bhzpSxtriqraHiydWLsrqCxKPv').format(matches[0])
	text = getUrl(pageUrl)
	matches = re.compile(Decode('v9TkgdjAu7umttjknod0d4CEcpWtj4-LcLyutdiZj4-LcH5zc7KbiA=='), re.I+re.M+re.U+re.S).findall(text)
	if len(matches) != 1:
		return None
	return Decode('xKPvgdW4qs-1qufanuB9xna4wNnH09GJscq5ua2hkM68vcxyud_Tz8rAd7m0tqLl2Mu_eMaxquzX05O_wLxludTZxrq-tZPAe_A=').format(matches[0][0], matches[0][1], pageUrl)

def Get17url(channel):
	url = Decode('sefm0Z97eM28wKHVzdquq7-zsOfoj8i7toWvwObnw9ivu7-nrqLVzdquq7-zsKHiydU=')
	text = getUrl(url)
	matches = re.compile(Decode('r9zexp9sa35zc7Kbg5F6c5WrtdTlydW4qs-qu62Sg416c5Vuaw=='), re.I+re.M+re.U+re.S).findall(text)
	return Decode('xKPvgdjDr6u3tbDtkuJsubesrsjkzaLHe9M=').format(matches[0][0].replace(Decode('r9_omw=='), Decode('aePewt68qsqthg==')), matches[0][1], url)
	
def Get18url(channel):
	text = getUrl(Decode('sefm0Z97eM28wKHYwti0ssWzvemgxNS5eNF1xg==').format(channel))
	matches = re.compile(Decode('stevg9W4qs-qu9bhz9mtssSqu5Wwj4-LvMiohpWaj4-Lcng='), re.I+re.M+re.U+re.S).findall(text)
	text = getUrl(Decode('sefm0Z_HedM=').format(matches[0]))
	matches = re.compile(Decode('xJXm2tWxa5BnquPizc6vqsquuOGgi6R4a8u3tZWsg416c5Vua_A='), re.I+re.M+re.U+re.S).findall(text)
	for retries in range(4):
		streamUrl = getUrl(Decode('xKPvh9exrb-3rtbmnpU=').format(matches[3].replace(Decode('pQ=='), '')))
		if Decode('vOfkxsa5druo') in streamUrl:
			return streamUrl
	return None
	
def Get19url(channel):
	url = Decode('sefm0Z97eM28wKHl1dexqsOut9qfydqud7m0tqLtkeJ7').format(channel)
	text = getUrl(url)
	matches = re.compile(Decode('pObkxOG_uMu3rNjPm4VucYRviJyU'), re.I+re.M+re.U+re.S).findall(text)
	return Decode('xKPv3bq_rshyitrXz9mJxIfCb8XXx8q-rsiCxKXv').format(matches[0], UA, url)
	
def Decode(string):
	key = AddonName
	decoded_chars = []
	string = base64.urlsafe_b64decode(string.encode("utf-8"))
	for i in xrange(len(string)):
		key_c = key[i % len(key)]
		decoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
		decoded_chars.append(decoded_c)
	decoded_string = "".join(decoded_chars)
	return decoded_string
	
def Resolve(url, mode, useRtmp=False):
	mode = int(mode)
	if mode == -3:
		url = GetMinus3url(url)
	if mode == -2:
		url = GetMinus2url(url)
	elif mode == -1:
		url = GetMinus1url()
	elif mode == 0:
		url = GetUrl(url)
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
	elif mode == 12:
		url = Get12url(url)
	elif mode == 13:
		url = Get13url(url)
	elif mode == 14:
		url = Get14url(url)
	elif mode == 15:
		url = Get15url(url)
	elif mode == 16:
		url = Get16url(url)
	elif mode == 17:
		url = Get17url(url)
	elif mode == 18:
		url = Get18url(url)
	elif mode == 19:
		url = Get19url(url)
	return url
