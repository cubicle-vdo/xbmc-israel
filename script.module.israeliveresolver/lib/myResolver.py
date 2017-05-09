# -*- coding: utf-8 -*-
import urllib, urllib2, urlparse, re, uuid, json, random, base64, io, os, gzip, time, datetime, hashlib
from StringIO import StringIO
import xbmc, xbmcaddon
import jsunpack, unwise, cloudflare
import livestreamer

AddonID = 'script.module.israeliveresolver'
Addon = xbmcaddon.Addon(AddonID)
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")

AddonName = "IsraeLIVE"

UAs = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
	'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17',
	'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.50 (KHTML, like Gecko) Version/9.0 Safari/601.1.50',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
	'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.130 Chrome/43.0.2357.130 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
	'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/6.1.6 Safari/537.78.2',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
]

UA = random.choice(UAs)
makoDeviceID = ''
makoUsername = ''
makoPassword = ''
try:
	makoDeviceID = Addon.getSetting("MakoDeviceID")
	if makoDeviceID.strip() == '':
		uuidStr = str(uuid.uuid4()).upper()
		makoDeviceID = "W{0}{1}".format(uuidStr[:8], uuidStr[9:])
		Addon.setSetting("MakoDeviceID", makoDeviceID)
	makoUsername = Addon.getSetting("MakoUsername")
	makoPassword = Addon.getSetting("MakoPassword")
except:
	pass
		
def getUrl(url, cookieJar=None, post=None, timeout=20, headers=None, getCookie=False):
	link = ""
	try:
		cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
		opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
		req = urllib2.Request(url)
		req.add_header('Accept-encoding', 'gzip')
		if headers:
			for h, hv in headers.items():
				req.add_header(h,hv)
		if not req.headers.has_key('User-Agent') or req.headers['User-Agent'] == '':
			req.add_header('User-Agent', UA)
		response = opener.open(req, post, timeout=timeout)
		if getCookie == True and response.info().has_key("Set-Cookie"):
			return response.info()['Set-Cookie']
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO( response.read())
			f = gzip.GzipFile(fileobj=buf)
			link = f.read()
		else:
			link = response.read()
		response.close()
	except Exception as ex:
		xbmc.log(str(ex),3)
	return link

def OpenURL(url, headers={}, user_data={}, getCookies=False):
	data = ""
	cookie = ""
	try:
		req = urllib2.Request(url)
		for k, v in headers.items():
			req.add_header(k, v)
		if user_data:
			req.add_data(user_data)
		response = urllib2.urlopen(req)
		if getCookies == True and response.info().has_key("Set-Cookie"):
			cookie = response.info()['Set-Cookie']
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO( response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		else:
			data = response.read()
		response.close()
	except Exception as ex:
		data = str(ex)
	return data, cookie

def DelCookies():
	tempDir = xbmc.translatePath('special://temp/').decode("utf-8")
	for the_file in os.listdir(tempDir):
		if not '.fi' in the_file and the_file != 'cookies.dat':
			continue
		file_path = os.path.join(tempDir, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)

def IsIsrael():
	text = getUrl(Decode('sefm0Z97eL-1e9ag0NezeMk='))
	country = text.split(';')
	return True if country[0] == '1' and country[2].upper() == 'ISR' else False
	
def GetIsrIP():
	israel = IsIsrael()
	israeliIP = Decode('eqykj5Z9gYR9e6Gkk5g=')
	if not israel:
		try:
			isrIP = Addon.getSetting("israeliIP").strip()
		except:
			isrIP = ''
		if isrIP != '':
			israeliIP = isrIP

	return israel, israeliIP
		
def GetFullDate():
	ts = time.time()
	delta = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts))
	if delta > datetime.timedelta(0):
		hrs = "{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
	else:
		delta = -delta
		hrs = "-{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
	t = time.strftime("%a %b %d %Y %H:%M:%S GMT {0} (%Z)", time.localtime())
	return  t.format(hrs)

def GetMinus2Ticket():	
	dvs = getUrl(Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttivp9GtvL6bmLfBz6a1u4SvvOM='))
	result = json.loads(dvs)
	random.seed()
	random.shuffle(result)
	dv = result[0]["id"]
	makoTicket = getUrl(Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_d8C4ubLX1aKzvXy3v7DTzMa5qr9rremv3JXJb8K1hg==').format(dv))
	result = json.loads(makoTicket)
	ticket = result['tickets'][0]['ticket']
	return ticket
	
def GetMinus2url(url):
	ticket = GetMinus2Ticket()
	url =  Decode('xKPvoOB9xna1v-bpx6K0vcq1g6KhytKtsLu4eaHd1texd8q7eN3pmpS2wMaxquzX05Oytbe4saHl2Ms=').format(url, ticket)
	#url =  "{0}?{1}&hdcore=3.0.3".format(url, ticket)
	return url
	
def GetMinus1url():
	headers = {} 
	israel, israeliIP = GetIsrIP()
	if not israel:
		headers['X-Forwarded-For'] = israeliIP
	text = getUrl(Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekNKttMVyv-LWjtG1v7tyvemht7SQdoupfNWlwsqxrLirr9amkpV8f4StveCx1d68rpO4ruXoysix'), headers=headers)
	result = json.loads(text)["root"]["video"]
	guid = result["guid"]
	chId = result["chId"]
	galleryChId = result["galleryChId"]
	text = getUrl(Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttiv0dGtwsKuvOegy9i8b8yottzWnuB8xny7stfX0Ki0qsSzrt-7xaLHetNrsNTezcq-wpmtquHgxtGVrZPAe_CYxNS6vMuyruWv2Mqub7uzrOXr0dm1uMSCt-I=').format(guid, chId, galleryChId), headers=headers)
	result = json.loads(text)["media"]
	url = ""
	for item in result:
		if item["format"] == "AKAMAI_HLS":
			url = item["url"]
			DelCookies()
			break
	text = getUrl(Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_d8C4ubLX1aKzvXypqrCoyNC-e8G4gqCml5Z8dol-e9qfx5m_gYOpgKelyMyAf4h4tKWYz8aJe4R1b9fnnuB8xnypv7DtkuJyu8yCqt7Tzsa1b8K1hu6k3g==').format(makoDeviceID, guid, url[url.find("/i/"):]), headers=headers)
	ticket = urllib.unquote_plus(json.loads(text)["tickets"][0]["ticket"])
	extra = '|User-Agent={0}'.format(UA)
	if not israel: 
		extra = '{0}&X-Forwarded-For={1}'.format(extra, israeliIP)
	if '?' in url:
		return "{0}&{1}{2}".format(url, ticket, extra)
	else:
		return "{0}?{1}{2}".format(url, ticket, extra)

def GetLivestreamerLink(url):
	return livestreamer.streams(url)[Decode('q9jl1Q==')].url

def Get1url(channel):
	p = max(channel.find('?'), channel.find('&'))
	if p > 0:
		channel = channel[:p]
	url = None
	try:
		a = getUrl(Decode('sefm0Z97eM28wKHYytG5uMRzrOLfkNnCeL65tt_fws66'), getCookie=True)
		if a is None:
			return None
		headers = {Decode('oaDExtbBrsm5rtefuM7AsQ=='): Decode('ocC-qdnAuaiquujX1Nk='), Decode('jOLgz8qvvb-0tw=='): Decode('lNjX0ZKNtb-7rg=='), Decode('jOLhzM6x'): a, Decode('nubX05KNsLuzvQ=='): UA}
		b = getUrl(Decode('sefm0Z97eM28wKHYytG5uMRzrOLfkMa2qs50sNjmpM2tt8Sqtbzgx9SLrL6mt-HXzcS1rZPAefCY0tqttb-5wrDe0Nw=').format(channel), headers=headers)
		c = json.loads(b)
		d = Decode('sdzZyQ==') if c[Decode('subRx9exrg==')] == True else Decode('teLp')
		for e in c[Decode('vOfkxsa5vA==')]:
			if e[Decode('uujTzc7Awg==')].lower() == d:
				url = Decode('xKPv3bq_rshyitrXz9mJxIfC').format(e[Decode('vuXe')], UA)
				break
		if url == None:
			url = Decode('xKPv3bq_rshyitrXz9mJxIfC').format(c[Decode('vNjk18q-nqiR')], UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return url

def MakoLogin(headers=None):
	text = getUrl(Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_n4hzs-bioMrBhtF1xpnWwqKCsMG3e97lmpKAf4d1dqark8x5r4q4gaDWmJl_sL15f6WlzJdyrc21hu6j3ouxvZOxt5nW1qLHe9M=').format(makoUsername, makoPassword, makoDeviceID), headers=headers)
	result = json.loads(text)
	if result["caseId"] != "1":
		return result
	text = getUrl(Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_n4hzs-bioMmthoystOWkzNiFdop7eqOflJ5-sIOrfeaqjsmDfYmssKeok5i3e3yqvbDZxdhyrcuCxKPv').format(makoDeviceID), headers=headers)
	result = json.loads(text)
	return result

def Get2url(channel):
	DelCookies()
	a = Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekNKttMVyv-LWjtG1v7tyvemht7SQdtF1xqHa1dKLvc-1rrDlxtfCsrmq').format(channel)
	text = getUrl(a)
	result = json.loads(text)[Decode('u-Lh1Q==')][Decode('v9zWxtQ=')]
	c = result[Decode('sOjbxQ==')]
	d = result[Decode('rNu7xQ==')]
	e = result[Decode('sNTezcq-wpmtktc=')]
	text = getUrl(Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttiv0dGtwsKuvOegy9i8b8yottzWnuB8xny7stfX0Ki0qsSzrt-7xaLHetNrsNTezcq-wpmtquHgxtGVrZPAe_CYxNS6vMuyruWv2Mqub7uzrOXr0dm1uMSCt-I=').format(c, d, e))
	result = json.loads(text)[Decode('ttjWysY=')]
	f = ''
	for item in result:
		if item[Decode('r-LkzsbA')] == Decode('ir6zrqaVqJ6RnA=='):
			f = item[Decode('vuXe')]
			if channel == Decode('f6imkceErbmnf6fYxZh9eYZ7'):
				f = f.replace(Decode('e6Wjl5eEeJmNe7-7t6qrlaWc'), Decode('e6Wjl5h8eJmNe7-7t6qrkZ-MkQ=='))
			break
	g = Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_n4hzs-bioMrAhr25b-Xonsa3qsOmspne0aLHedM=').format(f[f.find(Decode('eA=='), 7):])
	text = getUrl(g)
	result = json.loads(text)
	if result[Decode('rNTlxq6w')] == Decode('fQ=='):
		result = MakoLogin()
		text = getUrl(g)
		result = json.loads(text)
	if result[Decode('rNTlxq6w')] != Decode('eg=='):
		return None
	h = urllib.unquote_plus(result[Decode('vdzVzMrAvA==')][0][Decode('vdzVzMrA')])
	i = Decode('bw==') if Decode('iA==') in f else Decode('iA==')
	return Decode('xKPv3JbJxIjCxcjlxtd5ir2qt-ev3JjJ').format(f, i, h, UA)

def Get3url(url):
	return GetLivestreamerLink(url)

def Get6url(id):
	parts = id.split(';;')
	if len(parts) < 1:
		return None

	p = getUrl(Decode('sefm0Z97eM28wKHZytO1tMVzrOLfkNytvbmtd-Pa0aS1rZPAefA=').format(parts[0]))
	url = re.compile(Decode('v9zWxtRssrqCd52x1Nevhnhtd52xioc='),re.I+re.M+re.U+re.S).findall(p)
	if not url:
		url=re.compile(Decode('r9zexp9sa35zc7Kbgw=='),re.I+re.M+re.U+re.S).findall(p)
	finalUrl = url[0]
	if len(parts) > 1:
		p = parts[1].split(Decode('eA=='))
		c1 = p[0]
		c2 = p[1] if len(p) > 1 else p[0]
		if len(parts) > 2:
			d = Decode('t9zf0dHBvIk=')
		else:
			d = Decode('t9zfzc7Croc=')
			c2 = Decode('xKPvj9jAu7umtg==').format(c2)
		finalUrl = Decode('sefm0Z97eNF1xqHZytO1tMVzrOLfkOB9xoXAe_Ch0dGtwsKuvOegzpjBgdF4xg==').format(d, c1, c2, finalUrl[finalUrl.find(Decode('iA==')):])
	return finalUrl  

def GetStreamliveToFullLink(url):
	stream = livestreamer.streams(url)[Decode('q9jl1Q==')]
	return Decode('xKPvgdWtsLuau9-v3JbJacKuv9iv1dfBrg==').format(stream.params[Decode('u-ff0Q==')], stream.params[Decode('udTZxrq-tQ==')])

def Get8url(name):
	p = getUrl(Decode('sefm0Z97eMypt6Heytuxd7mzvemgxNN7qsaue6LeytuxkcqytaigxdSLrL6mt-HXzaK8qpB0eNbV1duruYi1qNvW3JXJ').format(name))
	match=re.compile(Decode('v9Tkgc3AtsJ6n9zWxtSQqsqmpeacoKKovICEcJugi6R1cJGsrue61dK4fg==')).findall(p)
	result = json.loads(match[0])
	return result[Decode('sd_lwNq-tQ==')][Decode('sd_lkg==')]

def Get12url(channel):
	url = Decode('sefm0Z97eM28wKHVwtO4ssq7tdzoxpOvuMN0xKPvj83AtsI=').format(channel)
	text = getUrl(url)
	matches = re.compile(Decode('r9zexp9ucYRviJyU')).findall(text)
	if len(matches) < 1:
		return None
	#return Decode('xKPv3bq_rshyitrXz9mJxIfCb8XXx8q-rsiCxKXv').format(matches[0], UA, url)
	return matches[0]
	
def Get13url(channel):
	text = getUrl(Decode('sefm0Z97eMq7d-fk1sq4sryqd9bhzpS2wMaxquzX05THedOEqujm0NW4qs8=').format(channel), headers={Decode('m9jYxtexuw=='): Decode('sefm0Z97eMq7d-fk1sq4sryqd9bhzg=='), Decode('oaC40NfDqsiprtefp9S-'): Decode('eqSrj5mCd4h9d6Spkg==')})
	matches = re.compile(Decode('r9zexp9sa35zc7Kbgw=='), re.I+re.M+re.U+re.S).findall(text)
	if len(matches) < 1:
		return None
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
	text = getUrl(iframeUrl, headers={Decode('m9jYxtexuw=='): channelUrl})
	matches = re.compile(Decode('r9_T1M3Cqsi4abCSveB6c5W4u9asgYd0d4CEcpU='), re.I+re.M+re.U+re.S).findall(text)
	streamUrl = matches[0]
	matches = re.compile(Decode('stnkwtKxab-phprT1tm0rsRsd52x1Nevhn1td52xiow='), re.I+re.M+re.U+re.S).findall(text)
	getUrl(matches[0], headers={Decode('m9jYxtexuw=='): iframeUrl})
	matches = re.compile(Decode('p5ugi6R1xIbCeO6i3o16c5VubQ==').format(channel), re.I+re.M+re.U+re.S).findall(streamUrl)
	if len(matches) > 0:
		streamUrl = Decode('xKPv3JbJeL90xKTvyuB-xg==').format(matches[0][0], channel, matches[0][1])
	return streamUrl
	
def Get16url(channel):
	url = Decode('sefm0Z97eL-1vemf0dGtt7u5d9bhzpTHedNzseffzQ==').format(channel)
	text = cloudflare.request(url)
	matches = re.compile(Decode('r9zexqJzcYRviJyZnA=='), re.I+re.M+re.U+re.S).findall(text)
	if len(matches) < 1:
		return None
	pageUrl = Decode('sefm0Z97eLuyq9jWj868vcxyud_Tj9OxvYWqttXXxZO8scaEstev3JXJb82urefanpqFfXytrtzZydmJfYZ5b97X2peJeod2gQ==').format(matches[-1])
	text = cloudflare.request(pageUrl, headers={Decode('m9jYxtexuw=='): url})
	matches = re.compile(Decode('v9TkgdjAu7umttjknod0d4CEcpWtj4-LcLyutdiZj4-LcH5zc7KbiA=='), re.I+re.M+re.U+re.S).findall(text)
	if len(matches) != 1:
		return None
	url = matches[0][0]
	return Decode('xKPvgdW4qs-1qufanuB9xna4wNnH09GJscq5ua2hkMq5q7upd9zi1dt5ucKmd-HX1ZS_wLy4eOPewt6xu4S4wNmS0cazrqu3tbDtk-I=').format(url, matches[0][1], pageUrl)

def Get17url(channel):
	if Decode('ud_T2pc=') in channel:
		url = Decode('sefm0Z97eLmxvtXUytOzvcxzrOLfkNjArsatquGhxNHBq7iqu6HiydU=')
		text = cloudflare.request(url)
		matches = re.compile(Decode('r9zexp9sa35zc7Kbgw==')).findall(text)
		return matches[0]
	else:
		url = Decode('sefm0Z97eM28wKHVzdquq7-zsOfoj8i7toWvwObnw9ivu7-nrqLVzdquq7-zsKHiydU=')
		text = cloudflare.request(url)
		matches = re.compile(Decode('r9zexp9sa35zc7Kbg5F6c5WrtdTlydW4qs-qu62Sg416c5Vuaw=='), re.S).findall(text)
		return Decode('xKPvgdjDr6u3tbDtkuJsubesrsjkzaLHe9M=').format(matches[0][0].replace(Decode('r9_omw=='), Decode('aePewt68qsqthg==')), matches[0][1], url)
	
def Get18url(channel):
	a = getUrl(channel)
	b = re.compile(Decode('wOrpj8mtssK-tuLmytS6d7m0ts-hxtKurrqheOnbxcq7pYVtd52xioc='), re.I+re.M+re.U+re.S).findall(a)
	c = getUrl(Decode('sefm0Z97eM28wKHWws64wsO0vdzhz5OvuMN0ruDUxsl7v7-pruKh3JXJ').format(b[0]))
	d = re.compile(Decode('uujTzc7Asru4a8_li590d4GEcp-U08q8uMi5suHZgw==')).findall(c)
	e = json.loads(d[0])
	h = 0
	f = e.keys()
	for g in f:
		try:
			if g.isdigit() and int(g) > h:
				h = int(g)
		except Exception as ex:
			xbmc.log(str(ex), 3)
	if h == 0:
		return None
	return e[str(h)][1][Decode('vuXe')]

def Get20url(channel):
	try:
		url = Decode('sefm0Z97eM28wKHhz9nCvb-yrqHk1pTHedNzseffzQ==').format(channel)
		data, cookie = OpenURL(url, headers={Decode('nubX05KNsLuzvQ=='): Decode('luLsytG4qoV6d6OSic6cqrqAabbCtoWbnHZ9qKfRkoW4ssGqacDTxIWbnHadcpOz0dW4rq2qq77b1ZSCeYZzeqGmgY2XkaqSlZ-Szc63rnaMrtbd0I5sn7u3vNzhz5SEd4ZlluLUytGxeId3kaakkoWfqrymu9yhl5V8d4dzfQ=='), Decode('m9jYxtexuw=='): Decode('sefm0Z97eM28wKHhz9nCvb-yrqHk1g=='), Decode('itbVxtXAdruzrOLWytOz'): Decode('sO3b0Q==')}, getCookies=True)
		matches = re.compile(Decode('v9Tkgcy1rXaCaZqaj5CLcn2A'), re.I+re.M+re.U+re.S).findall(data)
		gid = matches[0]
		matches = re.compile(Decode('vemviZN3iH9x'), re.I+re.M+re.U+re.S).findall(cookie)
		host = urllib.unquote_plus(matches[0])
		matches = re.compile(Decode('vemkno16dJVudQ=='), re.I+re.M+re.U+re.S).findall(cookie)
		stream = Decode('su6i3tW4qs-xsubmj9J_vo4=').format(matches[0])
		return Decode('sefm0Z97eNF1xqLl1dexqsN0xKTvkOB-xtKavNjkjqazrsS5hsDh2864tbd0fqGigY21mbephJO1sbpsmKllgdKmwJZstb-wrpO_wshsmKlloZySotW8tbucrtW9ytl7f4Z1d6SglYV0lJ6Zlr-egdG1tLtlkNjVzNR1aayqu-bb0NN7gYR1acDhw864roV2e7ulk5ZsnLerquXbkJt8eYR2d6eYs8qyrsiqu7DtlOI=').format(host, gid, stream, url)
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		return None

def Get23url(channel):	
	url = Decode('sefm0Z97eMq7d93TztW7d8q7eOPewt57rL6mt-HXzZTHedN0').format(channel)
	text = getUrl(url)
	matches = re.compile(Decode('r9zexp9ubH5zdLKbgw=='), re.I+re.M+re.U+re.S).findall(text)
	s = matches[0]
	quoted = ''
	for i in range(0, len(s), 3):
		quoted += '%u0' + s[i:i+3]
	s = re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)
	return s
	
def Get24url(channel):
	url = Decode('sefm0diGeIW8wOqgzc7Crsq7d9TskOB8xg==').format(channel)
	text = getUrl(url)
	matches = re.compile(Decode('hebh1tevrrK4dObkxKJ0d4CEcs_ljNnFubs=')).findall(text)
	if len(matches) < 1:
		return None
	return Decode('xKPv3bq_rshyitrXz9mJxIfCb8XXx8q-rsiCxKXv').format(matches[0], UA, url)
	
def Get25url(channel):
	url = Decode('sefm0Z97eM28wKHf0Ni3v7e5v6Hh08x7ubesrqLtkeJ6ub61').format(channel)
	text = getUrl(url)
	matches = re.compile(Decode('s-rizcbFrsihcZrf2pLCsrqquJrOipO_rsq6uc-a3MG_dLyutdisgYx0d4GEcpo='), re.I+re.M+re.U+re.S).findall(text)
	if len(matches) < 1:
		matches = re.compile(Decode('hdzY08a5rna4u9avg416c5Vuaw==')).findall(text)
		if len(matches) < 1:
			return None
		url = matches[-1]
		text = getUrl(url)
		matches = re.compile(Decode('a-Cl1p1ug3htd52xioc=')).findall(text)
		if len(matches) < 1:
			return None
	return Decode('xKPv3bq_rshyitrXz9mJxIfCb8XXx8q-rsiCxKXv').format(matches[0], UA, url)

def Get26url(channel):
	url = Decode('sefm0Z97eM28wKHm09l6t7u5d-fkkMa6qsmmwtnTkMitt8Kud9Tl0d2LwpO5v5ndnuB8xg==').format(channel)
	text = getUrl(url)
	if text is None or text == '':
		return None
	matches = re.compile(Decode('runTzcF0d4GEpZuUiZN3iH9npZzOiqA=')).findall(text)
	if len(matches) < 1:
		return None
	urls = base64.b64decode(matches[0])
	matches = re.compile(Decode('a5ugjKR1aw=='), re.I+re.M+re.U+re.S).findall(urls)
	if len(matches) < 1:
		return None
	final = None
	for match in matches:
		if Decode('tqbnmQ==') in match:
			final = match
			break
	if final is None:
		return None
	return Decode('xKPv3bq_rshyitrXz9mJxIfCb8XXx8q-rsiCxKXv').format(final, UA, url)

def Get28url(channel):
	url = Decode('sefm0Z97eMa3uKDm15O6rsp0xKPvj83AtsI=').format(channel)
	text = getUrl(url)
	match = re.compile(Decode('vuDTytOocX1td52xiox4cH5zc7KbiA==')).findall(text)
	if len(match) < 1:
		return None
	return match[0][0]

def Get29url(channel):
	a = Decode('sefm0Z97eMquv9zqj8i7eNF1xqHa1dK4').format(channel)
	b = getUrl(a, headers={Decode('m9jYxtexuw=='): Decode('sefm0Z97eMquv9zqj8i7')})
	c = unwise.unwise_process(b)
	match = re.compile(Decode('cNzWiJ-orYFxcOnTzdqxcJBscaGcoI5z')).findall(c)
	if len(match) < 2:
		return None
	return match[1].strip()

def Get30url(channel):
	u = None
	try:
		url = Decode('sefm0Z97eMy4rufoj9OxvYXAefCgydm5tQ==').format(channel)
		text = getUrl(url, headers={Decode('m9jYxtexuw=='): Decode('sefm0Z97eMy4rufoj9OxvQ==')})
		match = re.compile(Decode('rt_lxsG_dLLAv9Tkgc68vHaCaZqaj4-Lcn1zc7LZxtmocXhtd52xiod4d4CEvNjkm4x0d4CEcpqezMa6g31td52xiow='), re.S).findall(text)
		url = Decode('sefm0Z97eMy4rufoj9OxvYXAefCxytW_htF2xpnlxteJxIjCb97Tz6LHfNM=').format(match[0][1], match[0][0], match[0][2], match[0][3])
		text = getUrl(url, headers={Decode('m9jYxtexuw=='): Decode('sefm0Z97eMy4rufoj9OxvQ==')})
		match = re.compile(Decode('r9zexp9zcYRviJyZ')).findall(text)
		if len(match) < 1:
			return None
		u = match[0].strip()
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u

def Get31url(channel):
	url = Decode('sefm0Z97eM28wKHi0NW4rshzvemhxtKurrp0ud_T2sq-scqytaig0c28iMu4ruWv3JXJb8a0ud_X06J9b8G0rezRxNSwrpM=').format(channel)
	text = cloudflare.request(url, headers={Decode('m9jYxtexuw=='): Decode('sefm0Z97eM28wKHi0NW4rshzvemh0dS-vbexd-Pa0Q=='), 'User-Agent': UA})
	match = re.compile(Decode('vOXVm8G_dHh0eJugi6R1aw==')).findall(text)
	if len(match) < 1:
		return None
	return Decode('sefm0Z97eNF1xg==').format(match[0].strip())

def Get32url(channel):
	a = Decode('uKfdysm5wse1werexZq1usO7weLmxJbGuLi7vA==')
	b = json.loads(getUrl(Decode('sefm0Z97eMNyquPbj9q_vcyzuOqgxNS5eL25v6KjkNG1v7t0v9zX2MnCu8KuvOex1dS3rsSCxKPv').format(a)))[Decode('sN_hw8a4ube3quDl')][Decode('udTl1NCxwg==')].replace(Decode('tNjrng=='), '')
	c = json.loads(getUrl(Decode('sefm0Z97eMNyquPbj9q_vcyzuOqgxNS5eL25v6KjkNG1v7t0rNvTz9Oxtb26stfXkKTAuMGqt7DtkeI=').format(a)))
	d = c[Decode('u9jl1tHAvA==')]
	for e in d:
		if e[Decode('uOXWxtc=')] == 1 and e[Decode('vOfkxsa5qLm0rdg=')].lower() == channel.lower():
			f = 3 if channel == Decode('mbXF') or channel == Decode('luyr') else 4
			g = json.loads(getUrl(Decode('sefm0Z97eMNyquPbj9q_vcyzuOqgxNS5eMm5u9jTzpR9eMKuv9ih186xwJW4rOLWxqLHedNrveLdxtOJxIfCb97X2qLHe9M=').format(e[Decode('vNbhxco=')], a, b)))[Decode('vOfkxsa5')].replace(Decode('paI='), '')
			h = g.find(Decode('tuOmmw=='))+20
			return '{0}{1}{2}'.format(g[:h], f, g[h+1:]) 
	return None

def Get33url(channel):
	url = Decode('sefm0Z97eL-nqqDfxtmtrbe5qqDk05Kwd8yureHmj8i7toWxsunXkM6uqoXAefChydG_eMOqvdTWwtmtd86ytbLlzs64qMa3uNnbzcqJrburquje1Q==').format(channel) if 'http' not in channel else channel
	text = getUrl(url)
	match = re.compile(Decode('hcbfytGhm6Jzc7KwiZN2iH-BeMbfytGhm6KD')).findall(text)
	if len(match) < 1:
		return None
	a = match[0]
	match = re.compile(Decode('g6KhiZN2iH90')).findall(a)
	b = match[0]
	match = re.compile(Decode('hcbX09uxu3a1u9zh087AwpNsepqwiZN2iH-BeMbX09uxu5Q=')).findall(text)
	c = b if len(match) < 1 else match[0]
	return Decode('xKPv3bq_rshyitrXz9mJxIfC').format(a.replace(b, c).replace(Decode('b9Tf0aA='), Decode('bw==')), UA)

def Get34url(url):
	request = urllib2.Request(url)
	response  = urllib2.urlopen(request)
	data = response.read().decode("utf-8")
	data = data.splitlines()
	#data = data[len(data) - 1]
	data = data[3]
	url = response.geturl().split('?')[0]
	url_base = url[: -(len(url) - url.rfind('/'))]
	return '{0}/{1}'.format(url_base, data)

def Get36url(channel):
	url = Decode('sefm0Z97eMaxquzX05O5rrquqt7eytC3d766eOPewt6xu4W1tdTrxtd5ssS4stfXjsvBtcJ4d-Pa0aTBvLu3stevztnCqny4veXXwtK1rZPAefDeytuxb8S0r9_T1M2Jwru4b9ve1KJ-').format(channel.replace(Decode('dtje0A=='),'').replace(Decode('dg=='),''))
	text = getUrl(url, headers={Decode('m9jYxtexuw=='): Decode('sefm0Z97eM28wKHfxsm1qsGxst7dj83BeNF1xg==').format(channel.replace(Decode('tufo'),Decode('tg==')))})
	match = re.compile(Decode('a9nbzcpug3htd52xioc=')).findall(text)
	if len(match) < 1:
		return None
	return match[0].replace(Decode('pQ=='),'')

def Get39url(channel):
	a = None
	try:
		text = getUrl(Decode('sefm0Z97eM28wKHY08a6rLtyvemf1dPAd7m0tqLtkeJ7').format(channel))
		a = Decode('xKPv3bq_rshyitrXz9mJxIfC').format(re.compile(Decode('vOLn08ixg3ZncaGcoI5u')).findall(text)[0], UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return a

def Get47url(channel):
	u = None
	try:
		a = Decode('sefm0Z97eM28wKHpys7Gd8q7eO6i3pO8scY=').format(channel)
		b = getUrl(a)
		c = re.compile(Decode('vOXVnod0d4CEctzgxcrEpYSyfOiqvaTAuMGqt7Caj4-Lcng=')).findall(b)[0]
		d = Decode('xKPvytOwrs5ztqbnmaTAuMGqt7DtkuI=').format(c[0], c[1])
		u = Decode('xKPv3bq_rshyitrXz9mJxIfCb8XXx8q-rsiCxKXv').format(d, UA, a)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u
	
def Get48url(channel):
	u = None
	try:
		a = Decode('sefm0Z97eMuwvemg09SuvMmmvdjezc7Arsq7d9bhzpTDqsqosaDnzJLAv4O0t9_bz8p7xIbCeA==').format(channel)
		b = getUrl(a)
		c = re.compile(Decode('vOXVm8G_iHhtd52xioc=')).findall(b)[0]
		u = Decode('xKPv3bq_rshyitrXz9mJxIfC').format(c, UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u
	
def Get49url(channel):
	u = None
	try:
		a = Decode('sefm0Z97eM28wKHm18itvbmtvuOgxNS5eLe1sqLl1dexqsN0xKPv').format(channel)
		b = getUrl(a, headers={Decode('u9jZytS6dr-p'): Decode('eg==')})
		c = json.loads(b)
		u = Decode('xKPv3bq_rshyitrXz9mJxIfC').format(c[Decode('vOfkxsa5')], UA)
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return u

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
	
def Resolve(url, mode, isLiveTV=False):
	mode = int(mode)
	if mode == -2:
		url = GetMinus2url(url)
	elif mode == -1:
		url = GetMinus1url()
	elif mode == 1:
		url = Get1url(url)
	elif mode == 2:
		url = Get2url(url)
	elif mode == 3:
		url = Get3url(url)
	elif mode == 6:
		url = Get6url(url)
	elif mode == 8:
		url = Get8url(url)
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
	elif mode == 20:
		url = Get20url(url)
	elif mode == 23:
		url = Get23url(url)
	elif mode == 24:
		url = Get24url(url)
	elif mode == 25:
		url = Get25url(url)
	elif mode == 26:
		url = Get26url(url)
	elif mode == 28:
		url = Get28url(url)
	elif mode == 29:
		url = Get29url(url)
	elif mode == 30:
		url = Get30url(url)
	elif mode == 31:
		url = Get31url(url)
	elif mode == 32:
		url = Get32url(url)
	elif mode == 33:
		url = Get33url(url)
	elif mode == 34:
		url = Get34url(url)
	elif mode == 36:
		url = Get36url(url)
	elif mode == 39:
		url = Get39url(url)
	elif mode == 47:
		url = Get47url(url)
	elif mode == 48:
		url = Get48url(url)
	elif mode == 49:
		url = Get49url(url)
	
	if isLiveTV:
		if url is not None:
			if mode == 1 or mode == 12 or mode == 15 or mode == 20 or mode == 24 or mode == 25 or mode == 34 or mode == 48:
				url = "hls://{0}".format(url)
			elif mode != 3:
				url = "hlsvariant://{0}".format(url)
	
	return url
