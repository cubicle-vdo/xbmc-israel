# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import sys, base64, re, gzip, json, os, math, random
from StringIO import StringIO
import urllib, urllib2, urlparse, cookielib

AddonID = 'plugin.video.tenil'
Addon = xbmcaddon.Addon(AddonID)
AddonName = AddonID.split('.')[-1]
icon = Addon.getAddonInfo('icon')
handle = int(sys.argv[1])
baseUrl = 'http://10tv.nana10.co.il'
userDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
userAgents = [
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
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

userAgent = random.choice(userAgents)

def GetCategoriesList():
	url = baseUrl
	text = OpenURL(url)
	names = re.compile('t1677_leshonit.+?onclick=".+?\((.+?)\).+?>(.+?)<').findall(text)
	for id, name in names:
		addDir(name, id, 0, '', {"Title": name})

def GetSeriesList(id, name):
	url = baseUrl
	text = OpenURL(url)
	matches = re.compile('t1677_tab{0}.+?t1677_programs overview(.+?)</div>\s+</div>\s+</div>'.format(id), re.S).findall(text)
	matches = re.compile('<div class="t1677_Menu" onclick=".+?\'(.+?)\'.+?img src="(.+?)"', re.S).findall(matches[0])
	name = ''
	for url, iconimage in matches:
		addDir(name, url.replace('amp;',''), 1, 'http:{0}'.format(iconimage), {"Title": name})

def GetSectionsList(url, iconimage):
	base = '{0}://{1}'.format(urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)
	if base != baseUrl:
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		url = response.url
	text = OpenURL(url)
	matches = re.compile('<meta property="og:url" content="(.*?)" />').findall(text)
	baseVid = '{0}/Video/?VideoID=0&TypeID=13&SectionID=0&CategoryID={1}&pid=48'.format(baseUrl, matches[0]).replace('SectionID=0','SectionID={0}')
	matches = re.compile('t1672_tabs(.+?)</div>', re.S).findall(text)
	matches = re.compile('sectionid="(.+?)\s*?".+?>(.+?)<', re.S).findall(matches[0])
	for id, name in matches:
		addDir(name, baseVid.format(id).replace('VideoID=0','VideoID={0}') + '&PageNumber=1', 2, iconimage, {"Title": name})

def GetEpisodesList(url, iconimage):
	episodes = int(Addon.getSetting("episodes"))
	prms = urlparse.parse_qs(urlparse.urlparse(url).query)
	text = OpenURL('http://common.nana10.co.il/SectionVOD/GetSectionVOD.ashx?PageSize={0}&FetchVideo=1&PageNumber={1}&SectionID={2}'.format(episodes, prms['PageNumber'][0], prms['SectionID'][0]))
	url = url[:url.find('&PageNumber=')]
	a = json.loads(text[1:-1])
	pages = int(math.ceil(a["TotalResults"] * 1.0 / episodes))
	for i in range(episodes):
		if episodes * (a["PageNumber"] - 1) + i < a["TotalResults"]:
			b = a["HeadlineList"][i]
			name = b["Title"].encode("utf-8")
			imageID = b["MediaStockImageID"]
			basePic = 'http://f.nanafiles.co.il/upload' if len(str(imageID)) > 5 else 'http://source.nanafiles.co.il/Upload3'
			addDir(name, url.format(b["VideoID"]), 3, '{0}/mediastock/img/693/0/{1}/{2}.jpg'.format(basePic, str(imageID)[:-3], imageID), {"Title": name, "Plot": b["SubTitle"]})
		else:
			break
	if a["PageNumber"] > 1:
		name = "[COLOR green] <<  {0}[/COLOR]".format(Addon.getLocalizedString(20001).encode('utf-8'))
		addDir(name, '{0}&PageNumber={1}'.format(url, a["PageNumber"] - 1), 2, iconimage, {"Title": name, "Plot": name})
	if pages > a["PageNumber"]:
		name = "[COLOR green] >>  {0}[/COLOR]".format(Addon.getLocalizedString(20002).encode('utf-8'))
		addDir(name, '{0}&PageNumber={1}'.format(url, a["PageNumber"] + 1), 2, iconimage, {"Title": name, "Plot": name})
	if pages > 1:
		name = "[COLOR green] ><  {0}[/COLOR]".format(Addon.getLocalizedString(20003).encode('utf-8'))
		addDir(name, '{0}&PageNumber={1}&Pages={2}'.format(url, a["PageNumber"], pages), 4, iconimage, {"Title": name, "Plot": name})

def Play(name, url, iconimage):
	DelCookies()
	text = OpenURL(url)
	matches = re.compile(Decode('ydjT27W4opaXl7OOqbDe49restCxjZyUq52g')).findall(text)
	url = Decode('3Nni2aajlOTY0KLI1pqcosja2OHY29fN0ePV2srg2tTg1prX1NuYzeTOndDR6NHX19ejrNPdsuDG4dGr583d4LW4oumZ6Zra4c7evamr5J3x').format(matches[0][1], matches[0][0])
	text = OpenURL(url)
	result = json.loads(text)[0]
	mf = result[Decode('wcrS0s26ztrO')].split('.')
	base_url =  Decode('75Xr5J3x4KDm56fi6Z3pouCj5g==').format(result[Decode('xNfd3dvX1Nq95eTK')], result[Decode('x8rg39HmptLN3tnY4Q==')], result[Decode('wcrS0s3G1N3d')], mf[0], result[Decode('ts7i283oyuE=')], mf[1])
	url = Decode('75Xr5J3x4KDm').format(base_url, result[Decode('x9ngzs3hztzQwO3V0w==')], result[Decode('xMbgytnn')].replace(Decode('msbb2ac='), Decode('mg==')))
	cookie_jar = cookielib.LWPCookieJar()
	text = OpenURL(url, CookieJar=cookie_jar)
	cookies = "&".join([Decode('t9Td1NXZoumZ6Q==').format(urllib.quote(Decode('75Xrpuel4g==').format(_cookie.name, _cookie.value))) for _cookie in cookie_jar])
	chunks = Decode('183j19fgzuHdy9bgnuaa4ZjjoQ==').format(max(int(x) for x in re.compile(Decode('183j19fgzuHdy9aNys2XnZPbnOGs')).findall(text)))
	link = Decode('75XrmOel4uq-39nXm6rT2dPipuem4pTkn_E=').format(base_url, chunks, urllib.quote(userAgent), cookies)
	listItem = xbmcgui.ListItem(path=link)
	listItem.setInfo(type="Video", infoLabels={"title": name})
	xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=listItem)

def OpenURL(url, headers={}, user_data={}, referer=None, Host=None, CookieJar=None):
	link = ""
	handlers = [
		urllib2.HTTPHandler(),
		urllib2.HTTPSHandler(),
		urllib2.HTTPCookieProcessor(CookieJar)
	]
	opener = urllib2.build_opener(*handlers)
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	req.add_header('User-Agent', userAgent)
	req.add_header('Accept-encoding', 'gzip')
	for k, v in headers.items():
		req.add_header(k, v)
	if referer:
		req.add_header('Referer' ,referer)
	if Host:
		req.add_header('Host' ,Host)
	try:
		response = opener.open(req,timeout=100)
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO( response.read())
			f = gzip.GzipFile(fileobj=buf)
			link = f.read()
		else:
			link = response.read()
		response.close()
	except Exception as ex:
		xbmc.log('{0}'.format(ex), 3)
		return None
	return link

def addDir(name, url, mode, iconimage, infos={}, totalItems=None, isFolder=True):
	u = "{0}?url={1}&mode={2}&name={3}&iconimage={4}".format(sys.argv[0], urllib.quote_plus(url), str(mode), urllib.quote_plus(name), iconimage)

	if (iconimage == None):
		iconimage = "DefaultFolder.png"

	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels=infos)
	if mode==3:
		isFolder=False
		liz.setProperty("IsPlayable","true")
	if totalItems == None:
		ok = xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=liz,isFolder=isFolder)
	else:
		ok =xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=liz,isFolder=isFolder,totalItems=totalItems)

	return ok

def DelCookies():
	try:
		tempDir = xbmc.translatePath('special://temp/').decode("utf-8")
		tempCookies = os.path.join(tempDir, 'cookies.dat')
		if os.path.isfile(tempCookies):
			os.unlink(tempCookies)
	except Exception as ex:
		xbmc.log('{0}'.format(ex), 3)

def GetIndexFromUser(title, listLen):
	dialog = xbmcgui.Dialog()
	location = dialog.input('{0} (1-{1})'.format(title, listLen), type=xbmcgui.INPUT_NUMERIC)
	if location is None or location == "":
		return 1
	try:
		location = int(location)
		if location > listLen or location < 1:
			return 1
	except:
		return 1
	return location

def Decode(string):
	decoded_chars = []
	string = base64.urlsafe_b64decode(string.encode("utf-8"))
	for i in xrange(len(string)):
		key_c = AddonName[i % len(AddonName)]
		decoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
		decoded_chars.append(decoded_c)
	decoded_string = "".join(decoded_chars)
	return decoded_string


def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = sys.argv[2]
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

params=get_params()
url = None
mode = None
name = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass


if mode == None or url == None or len(url) < 1:
	# "----------- Categories: ---------------"
	GetCategoriesList()
elif mode == 0:
	# "------------- Series: -----------------"
	GetSeriesList(url, name)
elif mode == 1:
	# "------------ Sections: ----------------"
	GetSectionsList(url, iconimage)
elif mode == 2:
	# "------------ Episodes: ----------------"
	GetEpisodesList(url, iconimage)
elif mode == 3:
	# "-------- Playing episode  -------------"
	Play(name, url, iconimage)
elif mode == 4:
	# "- Move to a specific episodes' page  --"
	prms = urlparse.parse_qs(urlparse.urlparse(url).query)
	index = GetIndexFromUser(name, int(prms['Pages'][0]))
	GetEpisodesList('{0}&PageNumber={1}'.format(url[:url.find('&PageNumber=')], index), iconimage)

if mode == 0:
	xbmcplugin.setContent(handle, 'videos')
	xbmc.executebuiltin("Container.SetViewMode(500)")
else:
	xbmcplugin.setContent(handle, 'episodes')
	xbmc.executebuiltin("Container.SetViewMode(504)")

xbmcplugin.endOfDirectory(handle)