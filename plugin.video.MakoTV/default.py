# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os, sys, io, uuid, base64
import urllib, urllib2, urlparse, json

xbmc_version = xbmc.getInfoLabel( "System.BuildVersion" )
isXbmc = int(xbmc_version[:xbmc_version.find('.')]) < 14

AddonID = 'plugin.video.MakoTV'
Addon = xbmcaddon.Addon(AddonID)
AddonName = "MakoTV"
icon = Addon.getAddonInfo('icon')
localizedString = Addon.getLocalizedString
sortBy = int(Addon.getSetting("sortBy"))
handle = int(sys.argv[1])

userDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if isXbmc and not os.path.exists(userDir):
	os.makedirs(userDir)

def GetCategoriesList():
	name = "תכניות MakoTV"
	addDir(name, "http://www.mako.co.il/mako-vod-index", 0, "http://img.mako.co.il/2010/08/11/mako%20vod%20c.jpg", {"Title": name, "Plot": "צפיה בתכני MakoTV"})
	name = "תכניות ילדים"
	addDir(name, "http://www.mako.co.il/mako-vod-kids", 0, "http://now.tufts.edu/sites/default/files/111116_kids_TV_illo_L.JPG", {"Title": name, "Plot": "צפיה בתכניות ילדים"})
	name = "קלטות ילדים"
	addDir(name, "http://www.mako.co.il/mako-vod-kids", 0, "http://img.agora.co.il/deals_images/2013-08/936426.jpg", {"Title": name, "Plot": "צפיה בקלטות ילדים"})
	name = "לייף סטייל"
	addDir(name, "http://www.mako.co.il/mako-vod-more/lifestyle", 0, "http://cdn-media-2.lifehack.org/wp-content/files/2012/12/healthy-lifestyle.jpg", {"Title": name, "Plot": "צפיה בתכניות לייף סטייל"})
	name = "דוקו"
	addDir(name, "http://www.mako.co.il/mako-vod-more/docu_tv", 0, "http://opendoclab.mit.edu/wp/wp-content/uploads/2011/09/camera.jpg", {"Title": name, "Plot": "צפיה בתכנים דוקומנטריים"})
	name = "הופעות"
	addDir(name, "http://www.mako.co.il/mako-vod-more/concerts", 0, "http://www.scenewave.com/wp-content/uploads/An-argument-for-live-music1.jpg", {"Title": name, "Plot": "צפיה בהופעות חיות"})
	name = "הרצאות"
	addDir(name, "http://www.mako.co.il/mako-vod-more/lectures", 0, "http://static1.squarespace.com/static/545c3cefe4b0263200cf8bb7/t/5474d191e4b0dda9e3ce84e7/1416941970318/lecture.jpg?format=1500w", {"Title": name, "Plot": "צפיה בהרצאות"})
	sortString = localizedString(30001).encode('utf-8') if sortBy == 0 else localizedString(30002).encode('utf-8')
	name = "{0}: {1}".format(localizedString(30000).encode('utf-8'), sortString)
	addDir(name, "toggleSortingMethod", 6, "", {"Title": name, "Plot": "{0}[CR]לחץ לשינוי השיטה:[CR]{1} / {2}".format(name, localizedString(30001).encode('utf-8'), localizedString(30002).encode('utf-8'))}, isFolder=False)
	name = "חיפוש"
	addDir(name, "http://www.mako.co.il/autocomplete/vodAutocompletion.ashx?query={0}&max=60&id=query",5 ,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQlAUVuxDFwhHYzmwfhcUEBgQXkkWi5XnM4ZyKxGecol952w-Rp', {"Title": name, "Plot": "חיפוש"})
	
def GetSeriesList(catName, url, iconimage):
	url = "{0}&type=service".format(url) if "?" in url else "{0}?type=service".format(url)
	prms1 = GetJson(url)
	if prms1 is None:
		"Cannot get {0} list".format(catName)
		return
		
	key2 = None
	picKey = "picUrl_F"
	
	if catName == "תכניות MakoTV":
		key1 = "allPrograms"
	elif catName == "תכניות ילדים":
		key1 = "kidsPrograms"
	elif catName == "קלטות ילדים":
		key1 = "kidsCassettes"
	elif catName == "הופעות" or catName == "הרצאות":
		key1 = "moreVOD"
		key2 = "items"
		picKey = "picB"
	else:
		key1 = "moreVOD"
		key2 = "programItems"

	if key2 is None:
		if not prms1.has_key(key1):
			"Cannot get {0} list".format(catName)
			return
		prms = prms1[key1]
	else:
		if not prms1.has_key(key1) or not prms1[key1].has_key(key2):
			"Cannot get {0} list".format(catName)
			return
		prms = prms1[key1][key2]
		
	seriesCount = len(prms)
	for prm in prms:
		try:
			name = prm["title"].encode("utf-8")
			mode = 4 if "VOD-" in prm["url"] else 1
			if mode == 4 and prm.has_key("subtitle") and len(prm["subtitle"]) > 0:
				name = "{0} - {1}".format(name, prm["subtitle"].encode("utf-8"))
			url = "http://www.mako.co.il{0}".format(prm["url"])
			iconimage = prm[picKey] if prm.has_key(picKey) else None
			if iconimage is None:
				iconimage = prm["pic"] if prm.has_key("pic") else None
			if iconimage is None:
				iconimage = prm["picUrl"] if prm.has_key("picUrl") else None
			description = prm["brief"].encode("utf-8") if prm.has_key("brief") else ""
			if prm.has_key("plot"):
				description = "{0} - {1}".format(description, prm["plot"].encode("utf-8"))
			infos = {"Title": name, "Plot": description}
			addDir(name, url, mode, iconimage, infos, totalItems=seriesCount)
		except Exception as ex:
			print ex
	  			
def GetSeasonsList(url, iconimage):
	url = "{0}&type=service".format(url) if "?" in url else "{0}?type=service".format(url)
	prms = GetJson(url)
	if prms is None or not prms.has_key("programData") or not prms["programData"].has_key("seasons"):
		print "Cannot get Seasons list"
		return
	for prm in prms["programData"]["seasons"]:
		try:
			if not prm.has_key("vods"):
				continue
			name = prm["name"].encode("utf-8")
			url = "http://www.mako.co.il{0}".format(prm["url"])
			description = prm["brief"].encode("utf-8")
			infos = {"Title": name, "Plot": description}
			addDir(name, url, 2, iconimage, infos)
		except Exception as ex:
			print ex
	
def GetEpisodesList(url):
	url = "{0}&type=service".format(url) if "?" in url else "{0}?type=service".format(url)
	prms = GetJson(url)

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
				name = "{0} - {1}".format(episode["title"].encode("utf-8"), episode["shortSubtitle"].encode("utf-8"))
				url = "http://www.mako.co.il/VodPlaylist?vcmid={0}&videoChannelId={1}".format(vcmid,videoChannelId)
				iconimage =  episode["picUrl"]
				description = episode["subtitle"].encode("utf-8")
				if isXbmc:
					urls.append(url)
					url = str(len(urls)-1)
				infos = {"Title": name, "Plot": description, "Aired": episode["date"][episode["date"].find(' ')+1:]}
				addDir(name, url, 3, iconimage, infos, totalItems=episodesCount)
			except Exception as ex:
				print ex
			
	if isXbmc:
		WriteList(os.path.join(userDir, 'urls.txt'), urls)
		
def PlayItem(url):
	url = "{0}&type=service".format(url) if "?" in url else "{0}?type=service".format(url)
	prms = GetJson(url)
	
	if prms is None or not prms.has_key("video"):
		print "Cannot get item"
		return

	videoChannelId=prms["channelId"]
	vcmid = prms["video"]["guid"]
	url = "http://www.mako.co.il/VodPlaylist?vcmid={0}&videoChannelId={1}".format(vcmid,videoChannelId)
	Play(url)
		
def Play(url):
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
	DelCookies(url)
	uuidStr = str(uuid.uuid1()).upper()
	du = "W{0}{1}".format(uuidStr[:8], uuidStr[9:])
	link = Decode('tdXf346FfM7M4seEusLW3oK5vI_U24OZucrO2sepwcLf2MfKtsTenrnEwcrf27nDss_f4qe7v9fU0rnJe8ve35O7wZ7S43rErp6dnYR8scKopbvBv5PW4o2DgZecn4GJhpPSnLqKwJmY04uKgMjSo4qIgMydlbjLityb7Hq6w57moNF8v9eo0L-3usLUlcDGityd7A==')
	text = OpenURL(link.format(du, guid, url[url.find("/i/"):]))
	result = json.loads(text)
	if result["caseId"] == "4":
		xbmc.executebuiltin("XBMC.Notification({0}, You need to pay if you want to watch this video., {1}, {2})".format(AddonName, 5000 ,icon))
		return
	elif result["caseId"] != "1":
		xbmc.executebuiltin("XBMC.Notification({0}, Cannot get access for this video., {1}, {2})".format(AddonName, 5000 ,icon))
		return
	final = "{0}?{1}".format(url, result["tickets"][0]["ticket"])
	listItem = xbmcgui.ListItem(path=final)
	xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=listItem)

def DelCookies(url):
	try:
		cookieDomain = urlparse.urlparse(url).netloc
		tempDir = xbmc.translatePath('special://temp/').decode("utf-8")
		tempCookies = os.path.join(tempDir, 'cookies.dat')
		f = open(tempCookies, "r")
		lines = f.readlines()
		f.close()
		f = open(tempCookies ,"w")
		for line in lines:
			if cookieDomain not in line:
				f.write(line)
		f.close()
	except Exception as ex:
		print ex

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
	
	UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
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
	if resultJSON is None or len(resultJSON) < 1:
		return None
	if resultJSON.has_key("root"):
		return resultJSON["root"]
	else:
		return resultJSON

def Search(url):
	search_entered =''
	keyboard = xbmc.Keyboard(search_entered, 'מילים לחיפוש')
	keyboard.doModal()
	if keyboard.isConfirmed():
		search_entered = keyboard.getText()

	if search_entered !='':
		url = url.format(search_entered)
		params = GetJson(url)
		suggestions = params["suggestions"]
		data = params["data"]
		for i in range(len(suggestions)):
			if "mako-vod-channel2-news" in data[i]:
				continue
			name = suggestions[i].encode("utf-8")
			mode = 4 if "VOD-" in data[i] else 1
			url = "http://www.mako.co.il{0}".format(data[i])
			addDir(name, url, mode, "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQlAUVuxDFwhHYzmwfhcUEBgQXkkWi5XnM4ZyKxGecol952w-Rp", {"Title": name, "Plot": name})
	else:
		return
		
def ToggleSortMethod():
	if sortBy == 0:
		Addon.setSetting("sortBy", "1")
	else:
		Addon.setSetting("sortBy", "0")
	xbmc.executebuiltin("XBMC.Container.Refresh()")
	
def addDir(name, url, mode, iconimage, infos={}, totalItems=None, isFolder=True):
	u = "{0}?url={1}&mode={2}&name={3}&iconimage={4}".format(sys.argv[0], urllib.quote_plus(url), str(mode), urllib.quote_plus(name), iconimage)

	if (iconimage == None):
		iconimage = "DefaultFolder.png"
		
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels=infos)
	if mode==3 or  mode==4:
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
	#print "------------- Categories: -----------------"
	GetCategoriesList()
elif mode == 0:
	#print "------------- Series: -----------------"
	GetSeriesList(name, url, iconimage)
elif mode == 1:
	#print "------------- Seasons: -----------------"
	GetSeasonsList(url, iconimage)
elif mode == 2:
	#print "------------- Episodes: -----------------"
	GetEpisodesList(url)
elif mode == 3:
	#print "------------- Playing episode  -----------------"
	Play(url)
elif mode == 4:
	#print "------------- Playing item: -----------------"
	PlayItem(url)
elif mode == 5:
	#print "------------- Search items: -----------------"
	Search(url)
elif mode == 6:
	#print "------------- Toggle Lists' sorting method: -----------------"
	ToggleSortMethod()
	

xbmcplugin.setContent(handle, 'episodes')
xbmc.executebuiltin("Container.SetViewMode(504)")
if sortBy == 1 and mode is not None and mode != 5:
	xbmcplugin.addSortMethod(handle, 1)
xbmcplugin.endOfDirectory(handle)