# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import sys, base64, re, gzip, json, os, math
from StringIO import StringIO
import urllib, urllib2, urlparse

AddonID = 'plugin.video.tenil'
Addon = xbmcaddon.Addon(AddonID)
icon = Addon.getAddonInfo('icon')
handle = int(sys.argv[1])
baseUrl = 'http://10tv.nana10.co.il'
userDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")

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
	matches = re.compile('UserID=(.+?);GroupId=(.+?);').findall(text)
	url = 'http://vod.ch10.cloudvideoplatform.com/api/getlink/GetFlash?showID={0}&userID={1}'.format(matches[0][1], matches[0][0])
	text = OpenURL(url)
	matches = re.compile('<Bitrates>(.*?)</Bitrates>.*?<MediaFile>(.*?)</MediaFile>.*?<MediaRoot>(.*?)</MediaRoot><ProtocolType>(.*?)</ProtocolType>.*?<ServerAddress>(.*?)</ServerAddress>.*?<StreamingType>(.*?)</StreamingType>').findall(text)
	Bitrates, MediaFile, MediaRoot, ProtocolType, ServerAddress, StreamingType = matches[0]
	mf = MediaFile.split('.')
	link = '{0}{1}{2}{3}{4}.{5}{6}'.format(ProtocolType, ServerAddress, MediaRoot, mf[0], Bitrates, mf[1], StreamingType)
	listItem = xbmcgui.ListItem(path=link)
	listItem.setInfo(type="Video", infoLabels={"title": name})
	xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=listItem)

def OpenURL(url, headers={}, user_data={}, referer=None, Host=None):
	link = ""
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')
	req.add_header('Accept-encoding', 'gzip')
	for k, v in headers.items():
		req.add_header(k, v)
	if referer:
		req.add_header('Referer' ,referer)
	if Host:
		req.add_header('Host' ,Host)
	try:
		response = urllib2.urlopen(req,timeout=100)
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