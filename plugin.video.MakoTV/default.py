import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os, sys, io, re, errno
import urllib, urllib2, json
import repoCheck

xbmc_version = xbmc.getInfoLabel( "System.BuildVersion" )
isXbmc = int(xbmc_version[:xbmc_version.find('.')]) < 14

AddonID = 'plugin.video.MakoTV'
Addon = xbmcaddon.Addon(AddonID)
userDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if isXbmc and not os.path.exists(userDir):
	os.makedirs(userDir)
libDir = os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'lib')
sys.path.insert(0, libDir)
from crypto.cipher.aes import AES
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
PLAYLIST_KEY = 'LTf7r/zM2VndHwP+4So6bw=='


def GetMakoTicket():
	makoTicket = urllib.urlopen('http://mass.mako.co.il/ClicksStatistics/entitlementsServices.jsp?et=gt&rv=akamai').read()
	result = json.loads(makoTicket)
	ticket = result['tickets'][0]['ticket']
	return ticket+'&hdcore=3.0.3'

def decrypt(encrypted, key):
	pes = AES(key.decode('base64'))
	decrypted = pes.decrypt(encrypted.decode('base64'))
	return decrypted

def GetSeriesList():
	repoCheck.UpdateRepo()
	prms = GetJson("http://www.mako.co.il/mako-vod-index?type=service")
	if prms is None or not prms.has_key("allPrograms"):
		print "Cannot get Series list"
		return
	seriesCount = len(prms["allPrograms"])
	for prm in prms["allPrograms"]:
		name = unicode(prm["title"]).encode("utf-8")
		url = "http://www.mako.co.il{0}".format(prm["url"])
		iconimage =  prm["pic"]
		description = prm["brief"]
		if prm.has_key("plot"):
			description = "{0} - {1}".format(description, prm["plot"])
		addDir(name, url, 1, iconimage, description, seriesCount)
		#print "{0} - {1}".format(name, url)
	  			
def GetSeasonsList(url, iconimage):
	prms = GetJson("{0}?type=service".format(url))
	if prms is None or not prms.has_key("programData") or not prms["programData"].has_key("seasons"):
		print "Cannot get Seasons list"
		return
	for prm in prms["programData"]["seasons"]:
		if not prm.has_key("vods"):
			continue
		name = unicode(prm["name"]).encode("utf-8")
		url = "http://www.mako.co.il{0}".format(prm["url"])
		description = unicode(prm["brief"]).encode("utf-8")
		addDir(name, url, 2, iconimage, description)
		#print "{0} - {1}".format(name, url)
	
def GetEpisodesList(url):
	prms = GetJson("{0}?type=service".format(url))
	if prms is None or not prms.has_key("channelId") or not prms.has_key("programData") or not prms["programData"].has_key("seasons"):
		print "Cannot get Seasons list"
		return
	urls = []
	videoChannelId=prms["channelId"]
	for prm in prms["programData"]["seasons"]:
		if prm is None or not prm.has_key("vods") or not prm.has_key("current") or prm["current"].lower() != "true":
			continue
		
		episodesCount = len(prm["vods"])
		for episode in prm["vods"]:
			try:
				vcmid = episode["guid"]
				name = "{0} - {1}".format(unicode(episode["title"]).encode("utf-8"), unicode(episode["shortSubtitle"]).encode("utf-8"))
				url = "http://www.mako.co.il/VodPlaylist?vcmid={0}&videoChannelId={1}".format(vcmid,videoChannelId)
				iconimage =  episode["picUrl"]
				description = unicode(episode["subtitle"]).encode("utf-8")
				if isXbmc:
					urls.append(url)
					url = str(len(urls)-1)
				addDir(name, url, 3, iconimage, description, episodesCount)
				#print "{0} - {1}".format(name, url)
			except Exception as ex:
				print ex
				#pass
			
	if isXbmc:
		WriteList(os.path.join(userDir, 'urls.txt'), urls)
				
def Play(url, name, iconimage):
	if isXbmc:
		urls = ReadList(os.path.join(userDir, 'urls.txt'))
		url = urls[int(url)]
	link = OpenURL(url)
	p = urllib.unquote_plus(decrypt(link, PLAYLIST_KEY))
	match = re.compile('provider="AKAMAI_HDS"/><Ref href="(.*?)"').findall(p)
	base = match[0].replace('/z/', '/i/').replace('manifest.f4m', 'master.m3u8')
	final = base+'?'+urllib.unquote_plus(GetMakoTicket())
	listItem = xbmcgui.ListItem(name, iconimage, iconimage, path=final)
	listItem.setInfo(type='Video', infoLabels={ "Title": name})
	listItem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
	
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
	
def OpenURL(url, headers={}, user_data={}, retries=3):
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	
	req.add_header('User-Agent', UA)
	for k, v in headers.items():
		req.add_header(k, v)

	link = None
	for i in range(retries):
		try:
			response = urllib2.urlopen(req, timeout=100)
			link = response.read()
			response.close()
			break
		except Exception as ex:
			print ex

	return link
		
def GetJson(url):
	html = OpenURL(url)
	if html is None:
		return None
	resultJSON = json.loads(html)
	if resultJSON is None or len(resultJSON) < 1 or not resultJSON.has_key("root"):
		return None
	return resultJSON["root"]
	
def addDir(name, url, mode, iconimage, description, totalItems=None):
	u = "{0}?url={1}&mode={2}&iconimage={3}".format(sys.argv[0], urllib.quote_plus(url), str(mode), iconimage)

	if (iconimage == None):
		iconimage = "DefaultFolder.png"
		
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	liz.setProperty("Fanart_Image", iconimage)
	isFolder=True
	if mode==3 :
		isFolder=False
		liz.setProperty("IsPlayable","true")
	if totalItems == None:
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	else:
		ok =xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=totalItems)
	
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
ChName = None
iconimage = None
background = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:        
	mode = int(params["mode"])
except:
	pass
try:      
	ChName = urllib.unquote_plus(params["chname"])
except:
	pass
try:        
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass
try:        
	background = urllib.unquote_plus(params["background"])
except:
	pass

if mode == None or url == None or len(url) < 1:
	#print "------------- Series: -----------------"
	GetSeriesList()
elif mode == 1:
	#print "------------- Seasons: -----------------"
	GetSeasonsList(url, iconimage)
elif mode == 2:
	#print "------------- Episodes: -----------------"
	GetEpisodesList(url)
elif mode == 3:
	#print "-------------playing episide  -----------------"
	Play(url,ChName,iconimage)

xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
xbmc.executebuiltin("Container.SetViewMode(504)")
xbmcplugin.endOfDirectory(int(sys.argv[1]))