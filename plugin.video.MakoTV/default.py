import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os, sys, io, re, random, uuid, base64
import urllib, urllib2, json
import repoCheck

xbmc_version = xbmc.getInfoLabel( "System.BuildVersion" )
isXbmc = int(xbmc_version[:xbmc_version.find('.')]) < 14

AddonID = 'plugin.video.MakoTV'
Addon = xbmcaddon.Addon(AddonID)
AddonName = "MakoTV"

userDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if isXbmc and not os.path.exists(userDir):
	os.makedirs(userDir)

UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
PLAYLIST_KEY = 'LTf7r/zM2VndHwP+4So6bw=='

def GetSeriesList():
	repoCheck.UpdateRepo()
	prms = GetJson("http://www.mako.co.il/mako-vod-index?type=service")
	if prms is None or not prms.has_key("allPrograms"):
		print "Cannot get Series list"
		return
	seriesCount = len(prms["allPrograms"])
	for prm in prms["allPrograms"]:
		try:
			name = prm["title"]
			#name = "{0} - {1}".format(prm["title"].encode("utf-8"), prm["subtitle"].encode("utf-8")).decode("utf-8")
			url = "http://www.mako.co.il{0}".format(prm["url"])
			iconimage =  prm["pic"]
			description = prm["brief"]
			if prm.has_key("plot"):
				description = "{0} - {1}".format(description, prm["plot"])
			infos = {"Title": name, "Plot": description}
			addDir(name, url, 1, iconimage, infos, totalItems=seriesCount)
		except Exception as ex:
			print ex
	  			
def GetSeasonsList(url, iconimage):
	prms = GetJson("{0}?type=service".format(url))
	if prms is None or not prms.has_key("programData") or not prms["programData"].has_key("seasons"):
		print "Cannot get Seasons list"
		return
	for prm in prms["programData"]["seasons"]:
		try:
			if not prm.has_key("vods"):
				continue
			name = prm["name"]
			url = "http://www.mako.co.il{0}".format(prm["url"])
			description = prm["brief"]
			infos = {"Title": name, "Plot": description}
			addDir(name, url, 2, iconimage, infos)
		except Exception as ex:
			print ex
	
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
				name = "{0} - {1}".format(episode["title"].encode("utf-8"), episode["shortSubtitle"].encode("utf-8")).decode("utf-8")
				url = "http://www.mako.co.il/VodPlaylist?vcmid={0}&videoChannelId={1}".format(vcmid,videoChannelId)
				iconimage =  episode["picUrl"]
				description = episode["subtitle"]
				if isXbmc:
					urls.append(url)
					url = str(len(urls)-1)
				infos = {"Title": name, "Plot": description, "Aired": episode["date"][episode["date"].find(' ')+1:]}
				addDir(name, url, 3, iconimage, infos, totalItems=episodesCount)
			except Exception as ex:
				print ex
			
	if isXbmc:
		WriteList(os.path.join(userDir, 'urls.txt'), urls)
				
def Play(url, name, iconimage):
	if isXbmc:
		urls = ReadList(os.path.join(userDir, 'urls.txt'))
		url = urls[int(url)]
	
	guid = url[url.find('vcmid=')+6: url.find('&videoChannelId=')]
	link = Decode('tdXf346FfNji5oLDrszanbfFe8rXnpXArtm70Lu7jMve36K3usao38C3xs3U4siEt9Tblcq5usrPrM-Gyofh2Li7vKTT0MLEss2005HRft6R0sPEwNbY1MaTxMbNlbnEsNPk38i_vM-o3cM=')
	text = OpenURL(link.format(guid, url[url.find('&videoChannelId=')+16:]))
	result = json.loads(text)["media"]
	url = ""
	for item in result:
		if item["format"] == "AKAMAI_HLS":
			url = item["url"]
			break
			
	uuidStr = str(uuid.uuid1()).upper()
	du = "W{0}{1}".format(uuidStr[:8], uuidStr[9:])
	link = Decode('tdXf346FfM7M4seEusLW3oK5vI_U24OZucrO2sepwcLf2MfKtsTenrnEwcrf27nDss_f4qe7v9fU0rnJe8ve35O7wZ7S43rErp6dnYR8scKopbvBv5PW4o2DgZecn4GJhpPSnLqKwJmY04uKgMjSo4qIgMydlbjLityb7Hq6w57moNF8v9eo0L-3usLUlcDGityd7A==')
	text = OpenURL(link.format(du, guid, url[url.find("/i/"):]))
	result = json.loads(text)["tickets"][0]["ticket"]
	final = "{0}?{1}".format(url, result)
	listItem = xbmcgui.ListItem(path=final)
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
	
def addDir(name, url, mode, iconimage, infos={}, totalItems=None):
	u = "{0}?url={1}&mode={2}&iconimage={3}".format(sys.argv[0], urllib.quote_plus(url), str(mode), iconimage)

	if (iconimage == None):
		iconimage = "DefaultFolder.png"
		
	liz = xbmcgui.ListItem(name.encode("utf-8"), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels=infos)
	isFolder=True
	if mode==3 :
		isFolder=False
		liz.setProperty("IsPlayable","true")
	if totalItems == None:
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	else:
		ok =xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=totalItems)
	
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