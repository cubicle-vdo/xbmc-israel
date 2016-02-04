# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import sys, re, gzip
from StringIO import StringIO
import urllib, urllib2

handle = int(sys.argv[1])

def GetSeriesList():
	text = OpenURL('http://www.ch-20.tv/')
	matches = re.compile('<div class="show">\s+<h3><a href="(.*?)">(.*?)</a></h3>.*?<img src="(.*?)".*?</a></div>\s+</div>', re.S).findall(text)
	for link, name, iconimage in matches:
		name = UnEscapeXML(name)
		addDir(name, link, 1, iconimage, {"Title": name})

def GetEpisodesList(url, image):
	text = OpenURL(url)
	parts = text.split('<div id="catabpart"')
	name = "תכניות מלאות"
	addDir("[COLOR green]--- {0} ---[/COLOR]".format(name), '..', 99, image, {"Title": name, "Plot": name}, isFolder=False)
	episodes = re.compile('<div class="post-thumbnail">\s+<a href="(.*?)" rel="bookmark">.*?src="(.*?)".*?</a>.*?<div class="entry">.*?rel="bookmark">(.*?)</a></h2>\s+<p>(.*?)</p>.*?>.*?</a>', re.S).findall(parts[0])
	for link, iconimage, name, desc in episodes:
		name = UnEscapeXML(name)
		desc = UnEscapeXML(desc)
		addDir(name, link, 2, iconimage, {"Title": name, "Plot": desc}, isFolder=False)
	if len(parts) < 2:
		return
	name = "קטעים נבחרים"
	addDir("[COLOR green]--- {0} ---[/COLOR]".format(name), '..', 99, image, {"Title": name, "Plot": name}, isFolder=False)
	episodes = re.compile('<div class="post-thumbnail">\s+<a href="(.*?)" rel="bookmark">.*?src="(.*?)".*?</a>.*?<div class="entry">.*?rel="bookmark">(.*?)</a></h2>\s+<p>(.*?)</p>.*?>.*?</a>', re.S).findall(parts[1])
	for link, iconimage, name, desc in episodes:
		name = UnEscapeXML(name)
		desc = UnEscapeXML(desc)
		addDir(name, link, 2, iconimage, {"Title": name, "Plot": desc}, isFolder=False)

def Play(name, url, iconimage, desc):
	text = OpenURL(url)
	video = re.compile('<iframe class="tie_embed_code" src="(.*?)".*?<div class="entry">\s+<p.*?>(.*?)</p>', re.S).findall(text)
	desc = UnEscapeXML(video[0][1])
	text = OpenURL(video[0][0])
	link = re.compile('\("#content"\).html\(\'<source src="(.*?)"/>').findall(text)
	listItem = xbmcgui.ListItem(path=link[0])
	listItem.setInfo(type="Video", infoLabels={"title": name, "plot": desc})
	xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=listItem)

def UnEscapeXML(str):
	return str.replace('&amp;', '&').replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'").replace("&#8211;", "-").replace("&hellip;", "").replace("&nbsp;", " ").replace("<br />", "").replace("<strong>", "").replace("</strong>", "")
	
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
	desc = infos.get("Plot", "")
	u = "{0}?url={1}&mode={2}&name={3}&iconimage={4}&description={5}".format(sys.argv[0], urllib.quote_plus(url), str(mode), urllib.quote_plus(name), iconimage, urllib.quote_plus(desc))

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
description = None

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
try:      
	description = urllib.unquote_plus(params["description"])
except:
	pass
	

if mode == None or url == None or len(url) < 1:
	#print "------------- Categories: -----------------"
	GetSeriesList()
elif mode == 1:
	#print "------------- Episodes: -----------------"
	GetEpisodesList(url, iconimage)
elif mode == 2:
	#print "------------- Playing episode  -----------------"
	Play(name, url, iconimage, description)

xbmcplugin.setContent(handle, 'episodes')
xbmc.executebuiltin("Container.SetViewMode(504)")

xbmcplugin.endOfDirectory(handle)