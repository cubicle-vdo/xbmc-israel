# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import sys, base64, re, gzip, io, json, os
from StringIO import StringIO
import urllib, urllib2
import repoCheck

AddonID = 'plugin.video.iltwenty'
Addon = xbmcaddon.Addon(AddonID)
AddonName = "Channel20"
icon = Addon.getAddonInfo('icon')
handle = int(sys.argv[1])

userDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(userDir):
	os.makedirs(userDir)
	
def GetSeriesList():
	url = Decode('q9zV3qiUm6mnupba3NPZmpWfcdHNndbU2Zdfc5SYoaKVmH5ddJmWo6aRnGJeq9zO2g==')
	text = OpenURL(url)
	matches = re.compile(Decode('f9TKnJmk06SfuNjA19Kik1pebqeKlY7b1ZaVstvA2tfY4G9Xa5aMrZeMqm6UrN6B0drG36VtatzX3s3M3qGls9vAz9zJy56ZsdPUzeLK5KZXgZCPma2OqGGUrN6fqp3Gqm5fr9Gf'), re.I+re.M+re.U).findall(text)
	for match in matches:
		name = UnEscapeXML(match[2])
		addDir(name, "{0};{1}".format(match[0], match[1]), 1, "", {"Title": name})

def GetEpisodesList(params):
	param = params.split(';')
	groupId = param[0]
	filename = os.path.join(userDir, "{0}.txt".format(groupId))
	cachedChannels = ReadList(filename)
	
	text = OpenURL(Decode('q9zV3qiUm6mnupba3NPZmpWfcdHNnbPd4GFzstXRncTO0JefctzQ3sTO0Jefk9TC59PXm3WUpLzQ3sTO0Jefk9TC59PXy4iZp7HV09vYm2JcdJuZpaGR52KtcKmTr7CnpV9gb5iRnNbZ2Z4=').format(param[1].replace(Decode('bw=='), Decode('nQ=='))))
	channels = re.compile(Decode('udHF19Kik1pebqeKlZyQq26ZsM-B4eDIqVlYcZOgl5WTl3FsttjC3I7I2JOjtqWI4uTVy6iZp83QzeLO4J6VotzG5uKMqlpebqeKqp3Y3JOegQ=='), re.I+re.M+re.U+re.S).findall(text)
	isListUpdate = True if len(cachedChannels) != len(channels) else False
	for i in range(len(channels)-1, -1, -1):
		channel = channels[i]
		vidId = channel[0]
		if vidId not in [item["id"] for item in cachedChannels]:
			cachedChannels.insert(0, {"id": str(vidId), "iconimage": Decode('q9zV3qiUm6mnupba3NPZmpWfcdHN6Z7i').format(channel[1]), "name": UnEscapeXML(channel[2]).decode("utf-8"), "desc": ""})
	if isListUpdate:
		WriteList(filename, cachedChannels)
	for channel in cachedChannels:
		vidId = channel["id"]
		iconimage = channel["iconimage"]
		name = channel["name"].encode("utf-8")
		desc = channel["desc"].encode("utf-8")
		addDir(name, "{0};{1}".format(groupId, vidId), 2, iconimage, {"Title": name, "Plot": desc}, isFolder=False, totalItems=len(cachedChannels))

def Play(name, params, iconimage):
	param = params.split(';')
	groupId = param[0]
	vidId = param[1]
	vidAjaxUrl = Decode('q9zV3qiUm6mnupba3NPZmpWfcdHNnbHS2mFxs9iQxNfJ0aFfhtXOr97VwpuUqNei3tfErZyRu7HV09vYm2JcdJuYpaSR52KtcJiOxNfJ0aFzq8nP3NPRmGJgcdDV29o=').format(vidId)
	text = OpenURL(vidAjaxUrl).replace(Decode('ZZO04uDO2pleqdrQ27HNzaRzsszGlqGZlV1S'), Decode('n4o='))
	params = json.loads(text)
	final = params["iphonePath"].replace(Decode('Yw=='), Decode('aJqR'))
	filename = os.path.join(userDir, "{0}.txt".format(groupId))
	cachedChannels = ReadList(filename)
	i = next(index for (index, d) in enumerate(cachedChannels) if d["id"] == vidId)
	if i > -1:
		iconimage = Decode('q9zV3qiUm6mnupba3NPZmpWfcdHN6Z7i').format(params["imgPath"])
		name =  params["title"].replace(Decode('ZZO04uDO2pleqdrQ27HNzaRzsszGlqGZlV1S'), Decode('ZQ=='))
		desc = "{0} - {1}".format(params["articleTitle"].encode("utf-8"), params["articleSubTitle"].encode("utf-8")).decode("utf-8") if params.has_key("articleTitle") else ""
		if cachedChannels[i]["iconimage"] != iconimage or cachedChannels[i]["name"] != name or cachedChannels[i]["desc"] != desc:
			cachedChannels[i]["iconimage"] = iconimage
			cachedChannels[i]["name"] = name
			cachedChannels[i]["desc"] = desc
			WriteList(filename, cachedChannels)
	listItem = xbmcgui.ListItem(path=final)
	listItem.setInfo(type="Video", infoLabels={"title": name, "plot": desc})
	xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=listItem)

def ReadList(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		print ex
		content=[]

	return content

def WriteList(filename, list):
	try:
		with io.open(filename, 'w', encoding='utf-8') as handle:
			handle.write(unicode(json.dumps(list, indent=2, ensure_ascii=False)))
		success = True
	except Exception as ex:
		print ex
		success = False
		
	return success
	
def UnEscapeXML(str):
	return str.replace('&amp;', '&').replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'")
	
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