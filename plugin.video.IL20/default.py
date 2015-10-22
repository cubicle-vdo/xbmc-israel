# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import sys, base64, re, gzip
from StringIO import StringIO
import urllib, urllib2
import repoCheck

AddonID = 'plugin.video.IL20'
Addon = xbmcaddon.Addon(AddonID)
AddonName = "Channel20"
icon = Addon.getAddonInfo('icon')
handle = int(sys.argv[1])

def GetSeriesList():
	url = Decode('q9zV3qiUm6mnupba3NPZmpWfcdHNndbU2Zdfc5SYoaKVmH5ddJmWo6aRnGJeq9zO2g==')
	text = OpenURL(url)
	matches = re.compile(Decode('f9TKnJmk4puUqNfUzdrO36ZtapCPma2Ok3Bsp9HXjtHRzaWjgI_V5N7E06SfuNjUzc_T0JGcrNbM4c3Z0aqkaqaJnJmklW5fp9HXrKqUzXBsctTKrA=='), re.I+re.M+re.U+re.S).findall(text)
	for match in matches:
		name = UnEscapeXML(match[1])
		addDir(name, Decode('q9zV3qiUm6mnupba3NPZmpWfcdHNnbPd4GFzstXRncTO0JefctzQ3sTO0Jefk9TC59PXm3WUpLzQ3sTO0Jefk9TC59PXy4iZp7HV09vYm2JcdJuZpaGR52KtcKmTr7CnpV9gb5iRnNbZ2Z4=').format(match[0].replace(Decode('bw=='), Decode('nQ=='))), 1, "", {"Title": name})

def GetEpisodesList(url):
	text = OpenURL(url)
	matches = re.compile(Decode('udHF19Kik1pebqeKlZyQq26ZsM-B4eDIqVlYcZOgl5WTl3FsttjC3I7I2JOjtqWI4uTVy6iZp83QzeLO4J6VotzG5uKMqlpebqeKqp3Y3JOegQ=='), re.I+re.M+re.U+re.S).findall(text)
	for match in matches:
		vidid = match[0]
		iconimage = Decode('q9zV3qiUm6mnupba3NPZmpWfcdHN6Z7i').format(match[1])
		name = UnEscapeXML(match[2])
		addDir(name, vidid, 2, iconimage, {"Title": name}, isFolder=False)

def Play(name, url, iconimage):
	vidAjaxUrl = Decode('q9zV3qiUm6mnupba3NPZmpWfcdHNnbHS2mFxs9iQxNfJ0aFfhtXOr97VwpuUqNei3tfErZyRu7HV09vYm2JcdJuYpaSR52KtcJiOxNfJ0aFzq8nP3NPRmGJgcdDV29o=').format(url)
	text = OpenURL(vidAjaxUrl)
	matches = re.compile(Decode('ZdHR1t3T0YKRt9CDqJCNml1vbIo=')).findall(text)
	final = matches[0]
	print final
	listItem = xbmcgui.ListItem(path=final)
	xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=listItem)
	
def UnEscapeXML(str):
	return str.replace('&amp;', '&').replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "'")
	
def OpenURL(url, headers={}, user_data={}, referer=None, Host=None):
	link = ""
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
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
		print ex
		return None
	return link
		
def addDir(name, url, mode, iconimage, infos={}, totalItems=None, isFolder=True):
	u = "{0}?url={1}&mode={2}&name={3}&iconimage={4}".format(sys.argv[0], urllib.quote_plus(url), str(mode), urllib.quote_plus(name), iconimage)

	if (iconimage == None):
		iconimage = "DefaultFolder.png"
		
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels=infos)
	if mode==2:
		isFolder=False
		liz.setProperty("IsPlayable","true")
	if totalItems == None:
		ok = xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=liz,isFolder=isFolder)
	else:
		ok =xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=liz,isFolder=isFolder,totalItems=totalItems)
	
	return ok
	
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
	repoCheck.UpdateRepo()
	#print "------------- Categories: -----------------"
	GetSeriesList()
elif mode == 1:
	#print "------------- Episodes: -----------------"
	GetEpisodesList(url)
elif mode == 2:
	#print "------------- Playing episode  -----------------"
	Play(name, url, iconimage)

xbmcplugin.setContent(handle, 'episodes')
xbmc.executebuiltin("Container.SetViewMode(504)")

xbmcplugin.endOfDirectory(handle)