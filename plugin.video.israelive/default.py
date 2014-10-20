# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import sys, os, time, datetime, re
import urllib ,urllib2, json

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
xbmcLang = xbmc.getLanguage(0)
if xbmcLang != "he":
	xbmcLang = "en"

libDir = os.path.join(Addon.getAddonInfo("path"), 'resources', 'lib')
sys.path.insert(0, libDir)
import myFilmon, common, chardet

StreramsMethod = Addon.getSetting("StreramsMethod")
filmonOldStrerams = StreramsMethod == "0"
useRtmp = StreramsMethod == "2"
__icon__='http://static2.wikia.nocookie.net/__cb20121121053458/spongebob/images/f/f4/Check-icon.png'
__icon2__='https://svn.apache.org/repos/asf/openoffice/symphony/trunk/main/extras/source/gallery/symbols/Sign-QuestionMark02-Red.png'
icon = Addon.getAddonInfo('icon')
AddonName = Addon.getAddonInfo("name")

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)

tmpList = os.path.join(user_dataDir, 'tempList.txt')
FAV = os.path.join(user_dataDir, 'favorites.txt')
if not (os.path.isfile(FAV)):
	f = open(FAV, 'w') 
	f.write('[]') 
	f.close() 

remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")
remoteSettingsUrl = "https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/remoteSettings.txt"
remoteSettings = common.GetUpdatedList(remoteSettingsFile, remoteSettingsUrl)
if remoteSettings == []:
	xbmc.executebuiltin('Notification({0}, Cannot load settings, {1}, {2})'.format(AddonName, 5000, icon))
	sys.exit()

plxType = int(Addon.getSetting("PlxPlaylist"))
if plxType == 0:
	package = remoteSettings["packages"]["zip"]
	filmonGuideFile = os.path.join(user_dataDir, 'filmonZipGuide.txt')
elif plxType == 1:
	package = remoteSettings["packages"]["light"]
	filmonGuideFile = os.path.join(user_dataDir, 'filmonLightGuide.txt')
else:
	package = remoteSettings["packages"]["full"]
	filmonGuideFile = os.path.join(user_dataDir, 'filmonFullGuide.txt')

useFilmonEPG = Addon.getSetting("saveFilmonEPG") == "true"
if useFilmonEPG:
	if not (os.path.isfile(filmonGuideFile)):
		useFilmonEPG = False

globalGuideFile = os.path.join(user_dataDir, "guide.txt")
#useEPG = True if os.path.isfile(globalGuideFile) else False

	
def CATEGORIES():
	SaveGuide(showNotification=False)
	addDir("[COLOR green][B][{0}][/B][/COLOR]".format(localizedString(20102).encode('utf-8')),'favorits',15,'http://cdn3.tnwcdn.com/files/2010/07/bright_yellow_star.png','')
	
	if plxType == 0 or plxType == 1:
		ListLive(package["url"])
	else:
		for sub in package["sub"]:
			addDir("[COLOR blue][B][{0}][/B][/COLOR]".format(sub[xbmcLang].encode('utf-8')), sub["url"], 2, sub["icon"], '', background=sub["icon"])

		if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
			addDir('[COLOR blue][B][iLive.to][/B][/COLOR]','plugin://plugin.video.movie25/?iconimage=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashupArtwork%2fmaster%2fart%2filive.png&mode=119&name=iLive%20Streams&url=ilive',7,'https://raw.github.com/mash2k3/MashupArtwork/master/art/ilive.png','')
			addDir('[COLOR blue][B][Mash Sports][/B][/COLOR]','plugin://plugin.video.movie25/?fanart&genre&iconimage=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashupArtwork%2fmaster%2fskins%2fvector%2fk1m05.png&mode=182&name=K1m05%20Sports&plot&url=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashUpK1m05%2fmaster%2fPlaylists%2fSports%2fSports.xml',7,'http://3.bp.blogspot.com/-gJtkhvtY1EY/UVWwH2iCGfI/AAAAAAAAA-o/b-_qJk5UMiU/s1600/Live-Sports+-+Copie.jpg','')
		else:
			addDir('[COLOR green][B]לחץ כאן להתקנת תוסף חסר[/B][/COLOR]' ,'https://github.com/o2ri/xbmc-israel/blob/master/mash.zip?raw=true',8,'http://blog.missionmode.com/storage/post-images/critical-factor-missing.jpg','Mash23 addon')
	
	SetViewMode()
		
def update_view(url):
	ok=True		
	xbmc.executebuiltin('XBMC.Container.Update(%s)' % url )
	return ok

def SetViewMode():
	if useFilmonEPG:
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmc.executebuiltin("Container.SetViewMode(504)")

def ListLive(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
	page = urllib2.urlopen(req)
	response=page.read().replace("\r", "")
	page.close()
	matches = re.compile('^type(.*?)#$',re.I+re.M+re.U+re.S).findall(response)
	
	epgFilmon = None
	epgGlobal = None
	list = []
	for match in matches:
		item=re.compile('^(.*?)=(.*?)$',re.I+re.M+re.U+re.S).findall("type{0}".format(match))
		item_data = {}
		for field, value in item:
			item_data[field.strip().lower()] = value.strip()
		if not item_data.has_key("type") or (item_data["type"]=='playlist' and item_data['name'].find('Scripts section') >= 0):
			continue
		
		url = item_data['url']
		thumb = "" if not item_data.has_key("thumb") else item_data['thumb']
		description = ""
		channelName = item_data['name'].decode(chardet.detect(item_data['name'])["encoding"]).encode("utf-8")
		background = None
		isTvGuide = False
		if item_data["type"] == 'video' or item_data["type"] == 'audio':
			channelName = "[COLOR yellow][B]{0}[/B][/COLOR]".format(channelName)
			displayName = channelName
			if url.find('plugin.video.israelive') > 0:
				itemMode = re.compile('url=([0-9]*).*?mode=([0-9]*).*?',re.I+re.M+re.U+re.S).findall(url)
				if len(itemMode) > 0 and itemMode[0] != '':
					mode = int(itemMode[0][1])
				if mode == 1:
					mode = 3
					epgFilmon, displayName, description, background, isTvGuide = GetProgrammeDetails(epgFilmon, itemMode[0][0], channelName, filmon=True)
			elif url.find('plugin.video.f4mTester') > 0:
				mode= 12
				epgGlobal, displayName, description, background, isTvGuide = GetProgrammeDetails(epgGlobal, channelName, channelName)
			else:
				mode = 10
				epgGlobal, displayName, description, background, isTvGuide = GetProgrammeDetails(epgGlobal, channelName, channelName)
		elif item_data["type"] == 'playlist':
			mode = 2
			channelName = "[COLOR blue][B][{0}][/B][/COLOR]".format(channelName)
			displayName = channelName
		else:
			continue
					
		addDir(displayName, url, mode, thumb, description, channelName = channelName, background=background, isTvGuide=isTvGuide)
		list.append({"url": url, "image": thumb, "name": channelName, "type": item_data["type"]})
		
	with open(tmpList, 'w') as outfile:
		json.dump(list, outfile) 
	outfile.close()
	
	SetViewMode()

def Playf4m(url, name=None, iconimage=None):
	i = url.find('http://')
	if url.find('keshet') > 0:
		makoTicket = common.OPEN_URL('http://mass.mako.co.il/ClicksStatistics/entitlementsServices.jsp?et=gt&rv=akamai')
		result = json.loads(makoTicket)
		ticket = result['tickets'][0]['ticket']
		url = "{0}%3F{1}%26hdcore%3D3.0.3".format(url[i:], ticket)
	else:
		url = url[i:]
	
	if name is not None:
		name = urllib.unquote_plus(name)
		
	from F4mProxy import f4mProxyHelper
	player = f4mProxyHelper()
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
	#player.playF4mLink(urllib.unquote_plus(url), name, use_proxy_for_chunks=True)
	player.playF4mLink(urllib.unquote_plus(url), name, use_proxy_for_chunks=True, iconimage=iconimage)
	
def play_Filmon(url):
	direct, channelName, programmeName, iconimage = myFilmon.GetUrlStream(url, filmonOldStrerams, useRtmp)
	if direct == None:
		return

	listItem = xbmcgui.ListItem(path=direct)
	listItem.setInfo(type="Video", infoLabels={"Title": programmeName})
	#listItem.setInfo(type="Video", infoLabels={ "studio": channelName})
	listItem.setInfo(type="Video", infoLabels={"tvshowtitle": channelName, "episode": "0", "season": "0"})
	listItem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

def FilmonChannelGuide(url):
	chNum, referrerCh, ChName = myFilmon.GetUrlParams(url)
	if referrerCh != None:
		addDir('[COLOR red][B]No TV-Guide for this channel.[/B][/COLOR]', '.', 99, '', '')
		return
		
	channelName, channelDescription, iconimage, tvGuide = myFilmon.GetChannelGuide(chNum, filmonOldStrerams)
	ShowGuide(tvGuide, "[COLOR yellow][B]{0}[/B][/COLOR]".format(channelName), iconimage, channelDescription, filmon=True)

def ChannelGuide(channelName, iconimage):
	epg = common.ReadList(globalGuideFile)
	programmes = GetProgrammes(epg, channelName, full=True)
	ShowGuide(programmes, channelName, iconimage, "")
	
def ShowGuide(programmes, channelName, iconimage, channelDescription, filmon=False):
	if programmes is None or len(programmes) == 0:
		addDir('[COLOR red][B]No TV-Guide for[/B] "{0}".[/COLOR]'.format(channelName), '.', 99, iconimage, channelDescription)
	else:
		addDir('------- {0} [B][COLOR orange]- TV-Guide[/COLOR][/B] -------'.format(channelName), '.', 99, iconimage, channelDescription)
		day = ""
		for programme in programmes:
			startdate = datetime.datetime.fromtimestamp(programme["start"]).strftime('%d/%m/%y')
			if startdate != day:
				day = startdate
				addDir('[COLOR white][B]{0}:[/B][/COLOR]'.format(day), '.', 99, iconimage, channelDescription)
			startdatetime = datetime.datetime.fromtimestamp(programme["start"]).strftime('%H:%M')
			enddatetime = datetime.datetime.fromtimestamp(programme["end"]).strftime('%H:%M')
			if filmon == False:
				programme["name"] = programme["name"].encode('utf-8')
				programme["description"] = programme["description"].encode('utf-8')
			programmeName = "[COLOR orange][{0}-{1}][/COLOR] [COLOR yellow][B]{2}[/B][/COLOR]".format(startdatetime, enddatetime, programme["name"])
			description = programme["description"]
			image = programme["image"] if programme["image"] else iconimage
			addDir(programmeName, channelName, 99, image, description)
		
	SetViewMode()

def GetProgrammeDetails(epg, channelNum, channelName, filmon=False):
	displayName = channelName
	description = ""
	background = None
	isTvGuide = False
	if useFilmonEPG:
		if epg is None:
			guideFile = filmonGuideFile if filmon else globalGuideFile
			epg = common.ReadList(guideFile)
		programmes = GetProgrammes(epg, channelNum, filmon=filmon)
		if programmes is not None and len(programmes) > 0:
			isTvGuide = True
			programmeName = "[COLOR orange][B]{0}[/B][/COLOR] [COLOR grey][{1}-{2}][/COLOR]".format(programmes[0]["name"].encode('utf-8'), datetime.datetime.fromtimestamp(programmes[0]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[0]["end"]).strftime('%H:%M'))
			displayName = "{0} - {1}".format(channelName, programmeName)
			description = programmes[0]["description"].encode('utf-8')
			#background = thumb
			if programmes[0]["image"] is not None:
				background = programmes[0]["image"]
			if len(programmes) > 1:
				displayName = "{0} - [COLOR white]Next: [B]{1}[/B] [{2}-{3}][/COLOR]".format(displayName, programmes[1]["name"].encode('utf-8'), datetime.datetime.fromtimestamp(programmes[1]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[1]["end"]).strftime('%H:%M'))
				
	return epg, displayName, description, background, isTvGuide
		
def GetProgrammes(epg, channelName ,full=False, filmon=False):
	programmes = []
	try:
		matches = [x["tvGuide"] for x in epg if (filmon and str(x["channel"]) == channelName) or (filmon == False and x["channel"].encode('utf-8') == channelName)]
		programmes = matches[0]
	except:
		pass

	now = int(time.time())
	programmesCount = len(programmes)

	for i in range(programmesCount):
		programme = programmes[i]
		start = programmes[i]["start"]
		stop = programmes[i]["end"]
		if (start < now and now < stop):
			if (full):
				return programmes[i:]
			elif i+1 < programmesCount: 
				return programmes[i:i+2]
			else:
				return programmes[i:i+1]
	return []
	
def listFavorites():
	data=common.ReadList(FAV)
	if data==[]:
		addDir('[COLOR red]No channels in your favorits[/COLOR]','',99,'','')
		addDir('[COLOR red]ADD with right click on any channel[/COLOR]','',99,'','')
		
	epgFilmon = None
	epgGlobal = None
	for item in data:
		channelName = item["name"].encode("utf-8")
		displayName = channelName
		url = item["url"]
		image = item["image"].encode("utf-8")
		description = ""
		background = None
		isTvGuide = False

		if url.lower().find('israelive') > 0:
			itemMode = re.compile('url=([0-9]*).*?mode=([0-9]*).*?',re.I+re.M+re.U+re.S).findall(url)
			if len(itemMode) > 0 and itemMode[0] != '':
				mode = int(itemMode[0][1])
			if mode == 1:
				mode = 4
				epgFilmon, displayName, description, background, isTvGuide = GetProgrammeDetails(epgFilmon, itemMode[0][0], channelName, filmon=True)
		elif url.lower().find('f4mtester') > 0:
			mode = 13
			epgGlobal, displayName, description, background, isTvGuide = GetProgrammeDetails(epgGlobal, channelName, channelName)
		else:
			mode = 11
			epgGlobal, displayName, description, background, isTvGuide = GetProgrammeDetails(epgGlobal, channelName, channelName)
			
		addDir(displayName, url, mode, image, description, channelName = channelName, background=background, isTvGuide=isTvGuide)
		
	SetViewMode()
	
def addFavorites(url, iconimage, name):
	dirs=common.ReadList(FAV)
	for item in dirs:
		if item["url"].lower() == url.lower():
			xbmc.executebuiltin('Notification({0}, {1} Already in  favorites, {2}, {3})'.format(AddonName, name, 5000, __icon2__))
			return
	
	list=common.ReadList(tmpList)	
	for item in list:
		#if urllib.unquote_plus(item["name"].lower()) == name.lower():
		if item["name"].encode("utf-8").lower() == name.lower():
			url = item["url"]
			iconimage = item["image"]
			type = item["type"]
	if not iconimage:
		iconimage = ""
	data = {"url": url, "image": iconimage, "name": name, "type": type}
	dirs.append(data)
	with open(FAV, 'w') as outfile:
		json.dump(dirs, outfile) 
	outfile.close()
	xbmc.executebuiltin('Notification({0}, {1} added to favorites, {2}, {3})'.format(AddonName, name, 5000, __icon__))
		
def removeFavorties(url):
	dirs=common.ReadList(FAV)
	for item in dirs:
		if item["url"].lower() == url.lower():
		  dirs.remove(item)
		  with open(FAV, 'w') as outfile:
			json.dump(dirs, outfile) 
			outfile.close()
			xbmc.executebuiltin("XBMC.Container.Update('{0}/?description&iconimage=http%3a%2f%2fcdn3.tnwcdn.com%2ffiles%2f2010%2f07%2fbright_yellow_star.png&mode=15&name=%d7%94%d7%a2%d7%a8%d7%95%d7%a6%d7%99%d7%9d%20%d7%a9%d7%9c%d7%99&url=favorits')".format(AddonID))

def SaveGuide(forceManual=False, showNotification=True):
	try:
		if showNotification:
			xbmc.executebuiltin("XBMC.Notification({0}, Saving Guide..., {1}, {2})".format(AddonName, 300000 ,icon))
		common.UpdateZipedFile(globalGuideFile, remoteSettings["globalGuide"]["url"])
		if forceManual == False:
			isNewGuideFile = common.UpdateZipedFile(filmonGuideFile, package["guide"])
			isGuideFileOld = common.isFileOld(filmonGuideFile, package["refresh"] * 3600) # 24 hours
			if isNewGuideFile or not isGuideFileOld:
				if showNotification:
					xbmc.executebuiltin("XBMC.Notification({0}, Guide saved., {1}, {2})".format(AddonName, 5000 ,icon))
				return
			
		myFilmon.MakePLXguide(package["url"], filmonGuideFile)
		if showNotification:
			xbmc.executebuiltin("XBMC.Notification({0}, Guide saved., {1}, {2})".format(AddonName, 5000 ,icon))
	except:
		if showNotification:
			xbmc.executebuiltin("XBMC.Notification({0}, Guide NOT saved!, {1}, {2})".format(AddonName, 5000 ,icon))

def addDir(name, url, mode, iconimage, description, isFolder=True, channelName=None, background=None, isTvGuide=False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	
	if mode==3 or mode==6 or mode==7 or mode==8 or mode==10 or mode==12 or mode==11 or mode==4 or mode==99 or mode == 13:
		isFolder=False
	
	if mode==3 or mode==4 or mode==10 or mode==11 or mode==12 or mode == 13:
		liz.setProperty("IsPlayable","true")
		items = []

		if mode == 3:
			items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=9&iconimage={2})'.format(sys.argv[0], urllib.quote_plus(url), iconimage)))
			items.append(('Add to israelive-favorites', 'XBMC.RunPlugin({0}?url={1}&mode=16&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
		elif mode == 4:
			items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=9&iconimage={2})'.format(sys.argv[0], urllib.quote_plus(url), iconimage)))
			items.append(('Remove from israelive-favorites', "XBMC.RunPlugin({0}?url={1}&mode=18&iconimage={2}&name={3})".format(sys.argv[0], urllib.quote_plus(url), iconimage, name)))
		elif mode == 10 or mode == 12:
			if isTvGuide:
				items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=5&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
			items.append(('Add to israelive-favorites', 'XBMC.RunPlugin({0}?url={1}&mode=16&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
		elif mode == 11 or mode == 13:
			if isTvGuide:
				items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=5&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
			items.append(('Remove from israelive-favorites', 'XBMC.RunPlugin({0}?url={1}&mode=18&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
		

		liz.addContextMenuItems(items = items)
	
	if background is not None:
		liz.setProperty("Fanart_Image", background)

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	return ok
	
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
					params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
							param[splitparams[0]]=splitparams[1]
							
	return param
		
params = get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	#name=urllib.unquote_plus(params["name"])
	name=params["name"]
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:		
	mode=int(params["mode"])
except:
	pass
try:		
	description=urllib.unquote_plus(params["description"])
except:
	pass
		
print "{0} -> Mode: {1}".format(AddonName, mode)
#print "{0} -> URL: {1}".format(AddonName, url)
print "{0} -> Name: {1}".format(AddonName, urllib.unquote_plus(str(name)))
#print "{0} -> IconImage: {1}".format(AddonName, iconimage)
		 
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
	CATEGORIES()
elif mode==1:
	play_Filmon(sys.argv[2])
elif mode==2:
	ListLive(url)
elif mode==3 or mode==4:
	play_Filmon(url)
elif mode == 5:
	ChannelGuide(name, iconimage)
elif mode==7:
	update_view(url) 
elif mode==8:
	common.downloader_is(url,description)	  
	CATEGORIES()
elif mode==9:   
	FilmonChannelGuide(url)
elif mode==10 or mode==11:
	#listitem = xbmcgui.ListItem(urllib.unquote_plus(name), iconImage='', thumbnailImage='', path=url)
	listitem = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
elif mode==12 or mode==13:
	Playf4m(url, name, iconimage)
elif mode==15:
	listFavorites()
elif mode==16: 
	addFavorites(url, iconimage, name) 
elif mode==18:
	removeFavorties(url)
elif mode == 20:
	SaveGuide()
	sys.exit()
elif mode == 21:
	SaveGuide(forceManual=True)
	sys.exit()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
