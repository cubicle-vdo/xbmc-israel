# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import sys, os, time, datetime, re, platform
import urllib ,urllib2, json
import repoCheck

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
xbmcLang = xbmc.getLanguage(0)
if xbmcLang != "he":
	xbmcLang = "en"

libDir = os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'lib')
sys.path.insert(0, libDir)
import myFilmon, common, myResolver

filmonOldStrerams = Addon.getSetting("StreramsMethod") == "0"
useRtmp = Addon.getSetting("StreramProtocol") == "1"
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
remoteSettingsUrl = Addon.getSetting("remoteSettingsUrl")
if os.path.isfile(remoteSettingsFile):
	remoteSettings = common.ReadList(remoteSettingsFile)
else:
	remoteSettings = common.GetUpdatedList(remoteSettingsFile, remoteSettingsUrl)

if remoteSettings == []:
	xbmc.executebuiltin('Notification({0}, Cannot load settings, {1}, {2})'.format(AddonName, 5000, icon))
	sys.exit()

package = remoteSettings["packages"]["full"]

plxFile = os.path.join(user_dataDir, "israelive.plx")
if not os.path.isfile(plxFile):
	common.UpdatePlx(package["url"], plxFile)

globalGuideFile = os.path.join(user_dataDir, "guide.txt")
filmonGuideFile = os.path.join(user_dataDir, 'filmonFullGuide.txt')
epgGlobal = None
epgFilmon = None

useEPG = Addon.getSetting("useEPG") == "true"

def CATEGORIES():
	repoCheck.UpdateRepo()
	addDir("[COLOR green][B][{0}][/B][/COLOR]".format(localizedString(30000).encode('utf-8')),'favorits',16,'http://cdn3.tnwcdn.com/files/2010/07/bright_yellow_star.png','')
	ListLive("israelive", "http://3.bp.blogspot.com/-vVfHI8TbKA4/UBAbrrZay0I/AAAAAAAABRM/dPFgXAnF8Sg/s1600/retro-tv-icon.jpg")
	SetViewMode()
		
def update_view(url):
	ok=True		
	xbmc.executebuiltin('XBMC.Container.Update({0})'.format(url))
	return ok

def SetViewMode():
	if useEPG:
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmc.executebuiltin("Container.SetViewMode(504)")

def ListLive(name, iconimage=None):
	list = []
	list1 = common.GetListFromPlx(filterCat=name)
	for item_data in list1:
		url = item_data['url']
		image = item_data['image']
		description = ""
		channelName = common.GetEncodeString(item_data['name'])
		background = None
		isTvGuide = False
		
		if item_data["type"] == 'video' or item_data["type"] == 'audio':
			channelName = "[COLOR yellow][B]{0}[/B][/COLOR]".format(channelName)
			displayName = channelName
			chNum = None
			filmon = False
			
			if url.find('plugin.video.israelive') > 0:
				itemMode = re.compile('url=([0-9]*).*?mode=([0-9]*)(.*?)$',re.I+re.M+re.U+re.S).findall(url)
				if len(itemMode) > 0 and itemMode[0] != '':
					mode = int(itemMode[0][1])
				if mode == 1:
					mode = 3
					chNum = itemMode[0][0]
					if itemMode[0][2].find("&ignorefilmonguide=1") < 0:
						filmon = True
			elif url.find('plugin.video.f4mTester') > 0:
				mode = 12
			elif url.find('?mode=2') > 0:
				mode = 14
			else:
				mode = 10
				
			displayName, description, background, isTvGuide = GetProgrammeDetails(channelName, chNum, filmon=filmon)
		
		elif item_data["type"] == 'playlist':
			mode = 2
			displayName = "[COLOR blue][B][{0}][/B][/COLOR]".format(channelName)
			background = image
		else:
			continue
					
		if background is None or background == "":
			background = iconimage
		addDir(displayName, url, mode, image, description, channelName = channelName, background=background, isTvGuide=isTvGuide)
		list.append({"url": url, "image": image, "name": channelName.decode("utf-8"), "type": item_data["type"]})

	common.WriteList(tmpList, list)
	SetViewMode()

def PlayChannel(url, name, iconimage):
	u, channelName, programmeName, icon = GetPlayingDetails(urllib.unquote_plus(name))
	Play(url, channelName, programmeName, iconimage)
	
def Playf4m(url, name=None, iconimage=None):
	i = url.find('http://')
	if url.find('keshet') > 0:
		makoTicket = urllib.urlopen('http://mass.mako.co.il/ClicksStatistics/entitlementsServices.jsp?et=gt&rv=akamai').read()
		result = json.loads(makoTicket)
		ticket = result['tickets'][0]['ticket']
		url = "{0}?{1}&hdcore=3.0.3".format(url[i:], ticket)
	else:
		url = url[i:]
	
	channelName = "" 
	programmeName = ""
	if name is not None:
		u, channelName, programmeName, icon = GetPlayingDetails(urllib.unquote_plus(name))
		
	from F4mProxy import f4mProxyHelper
	player = f4mProxyHelper()
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
	#player.playF4mLink(urllib.unquote_plus(url), name, use_proxy_for_chunks=True)
	player.playF4mLink(urllib.unquote_plus(url), programmeName, use_proxy_for_chunks=True, iconimage=iconimage, channelName=channelName)
	
def PlayGLArabLink(url, name, iconimage):
	url = myResolver.GetGLArabFullLink(url)
	u, channelName, programmeName, icon = GetPlayingDetails(urllib.unquote_plus(name))
	Play(url, channelName, programmeName, iconimage)
	
def PlayFilmon(chNum, channelName="", ignoreFilmonGuide=False):
	url, channelName, programmeName, iconimage = GetPlayingDetails(urllib.unquote_plus(channelName), chNum, filmon=True, ignoreFilmonGuide=ignoreFilmonGuide)
	if url is None:
		return None
	Play(url, channelName, programmeName, iconimage)
	
def Play(url, channelName, programmeName, iconimage=None):
	listItem = xbmcgui.ListItem(path=url)
	listItem.setInfo(type="Video", infoLabels={"Title": programmeName})
	#listItem.setInfo(type="Video", infoLabels={ "studio": channelName})
	listItem.setInfo(type="Video", infoLabels={"tvshowtitle": channelName, "episode": "0", "season": "0"})
	if iconimage is not None:
		listItem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

def GetPlayingDetails(channelName, channelNum=None, filmon=False, ignoreFilmonGuide=False):
	global epgGlobal
	url = None
	programmeName = ""
	iconimage = None

	if filmon:
		url, chName, iconimage, programmes = myFilmon.GetUrlStream(channelNum, filmonOldStrerams, useRtmp)
		if url is None:
			return None, None, None, None
		
	if not filmon or (filmon and ignoreFilmonGuide):
		if not useEPG:
			programmeName = channelName
			return url, channelName, programmeName, iconimage

		if epgGlobal is None:
			epgGlobal = common.ReadList(globalGuideFile)
		programmes = GetProgrammes(epgGlobal, channelName)
	
	if len(programmes) > 0:
		programme = programmes[0]
		if not filmon:
			programme["name"] = programme["name"].encode('utf-8')
		programmeName = '[B]{0}[/B] [{1}-{2}]'.format(programme["name"], datetime.datetime.fromtimestamp(programme["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programme["end"]).strftime('%H:%M'))
		if len(programmes) > 1:
			nextProgramme = programmes[1]
			if not filmon:
				nextProgramme["name"] = nextProgramme["name"].encode("utf-8")
			channelName = "{0} - [COLOR white]Next: [B]{1}[/B] [{2}-{3}][/COLOR]".format(channelName, nextProgramme["name"], datetime.datetime.fromtimestamp(nextProgramme["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(nextProgramme["end"]).strftime('%H:%M'))
	else:
		programmeName = channelName

	return url, channelName, programmeName, iconimage
	
def FilmonChannelGuide(url, channelName, iconimage, ignoreFilmonGuide=False):
	filmon = False
	programmes = []
	channelDescription = ""

	if not ignoreFilmonGuide:
		chNum, referrerCh, chName, filmonMethod = myFilmon.GetUrlParams(url)
		if referrerCh is None:
			filmon = True
			chName, channelDescription, iconimage, programmes = myFilmon.GetChannelGuide(chNum, filmonOldStrerams=True)
	
	if not filmon:
		epg = common.ReadList(globalGuideFile)
		programmes = GetProgrammes(epg, channelName, full=True)

	if iconimage is None:
		iconimage = ""
	if channelDescription is None:
		channelDescription = ""
		
	ShowGuide(programmes, channelName, iconimage, channelDescription, filmon=filmon)

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
			if not filmon:
				programme["name"] = programme["name"].encode('utf-8')
				programme["description"] = "" if programme["description"] is None else programme["description"].encode('utf-8')
			programmeName = "[COLOR orange][{0}-{1}][/COLOR] [COLOR yellow][B]{2}[/B][/COLOR]".format(startdatetime, enddatetime, programme["name"])
			description = programme["description"]
			image = programme["image"] if programme["image"] else iconimage
			addDir(programmeName, channelName, 99, image, description)
		
	SetViewMode()

def GetProgrammeDetails(channelName, channelNum=None, filmon=False):
	global epgFilmon
	global epgGlobal
	displayName = channelName
	description = ""
	background = None
	isTvGuide = False
	if useEPG:
		if filmon:
			if epgFilmon is None:
				epgFilmon = common.ReadList(filmonGuideFile)
			programmes = GetProgrammes(epgFilmon, channelNum, filmon=filmon)
		else:
			if epgGlobal is None:
				epgGlobal = common.ReadList(globalGuideFile)
			programmes = GetProgrammes(epgGlobal, channelName)
		
		if programmes is not None and len(programmes) > 0:
			isTvGuide = True
			programmeName = "[COLOR orange][B]{0}[/B][/COLOR] [COLOR grey][{1}-{2}][/COLOR]".format(programmes[0]["name"].encode('utf-8'), datetime.datetime.fromtimestamp(programmes[0]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[0]["end"]).strftime('%H:%M'))
			displayName = "{0} - {1}".format(channelName, programmeName)
			if programmes[0]["description"] is not None:
				description = programmes[0]["description"].encode('utf-8')
			if programmes[0]["image"] is not None:
				background = programmes[0]["image"]
			if len(programmes) > 1:
				displayName = "{0} - [COLOR white]Next: [B]{1}[/B] [{2}-{3}][/COLOR]".format(displayName, programmes[1]["name"].encode('utf-8'), datetime.datetime.fromtimestamp(programmes[1]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[1]["end"]).strftime('%H:%M'))
				
	return displayName, description, background, isTvGuide
		
def GetProgrammes(epg, channelName ,full=False, filmon=False):
	programmes = []
	try:
		matches = [x["tvGuide"] for x in epg if (filmon and str(x["channel"]) == channelName) or (not filmon and x["channel"].encode('utf-8') == channelName)]
		programmes = matches[0]
	except Exception, e:
		pass

	now = int(time.time())
	programmesCount = len(programmes)

	for i in range(programmesCount):
		start = programmes[i]["start"]
		stop = programmes[i]["end"]
		#if (start < now and now < stop):
		if now >= stop:
			continue
		if now < start:
			newStart = now if i == 0 else programmes[i-1]["end"]
			programme = {"start": newStart, "end": programmes[i]["start"], "name": "No Details", "description": None, "image": None}
			programmes.insert(i, programme)
			
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
		addDir('[COLOR red]{0}[/COLOR]'.format(localizedString(30202).encode('utf-8')), '', 99, '', '')
		addDir('[COLOR red]{0}[/COLOR]'.format(localizedString(30203).encode('utf-8')), '', 99, '', '')
		
	for item in data:
		channelName = item["name"].encode("utf-8")
		displayName = channelName
		url = item["url"]
		image = item["image"].encode("utf-8")
		description = ""
		background = None
		isTvGuide = False
		chNum = None
		filmon = False

		if url.lower().find('israelive') > 0:
			itemMode = re.compile('url=([0-9]*).*?mode=([0-9]*)(.*?)$',re.I+re.M+re.U+re.S).findall(url)
			if len(itemMode) > 0 and itemMode[0] != '':
				mode = int(itemMode[0][1])
			if mode == 1:
				mode = 4
				chNum = itemMode[0][0]
				if itemMode[0][2].find("&ignorefilmonguide=1") < 0:
					filmon = True
		elif url.lower().find('f4mtester') > 0:
			mode = 13
		elif url.find('?mode=2') > 0:
			mode = 15
		else:
			mode = 11
			
		displayName, description, background, isTvGuide = GetProgrammeDetails(channelName, chNum, filmon=filmon)
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
	data = {"url": url, "image": iconimage, "name": name.decode("utf-8"), "type": type}
	dirs.append(data)
	common.WriteList(FAV, dirs)
	xbmc.executebuiltin('Notification({0}, {1} added to favorites, {2}, {3})'.format(AddonName, name, 5000, __icon__))
		
def removeFavorties(url):
	dirs=common.ReadList(FAV)
	for item in dirs:
		if item["url"].lower() == url.lower():
			dirs.remove(item)
			common.WriteList(FAV, dirs)
			xbmc.executebuiltin("XBMC.Container.Refresh()")

def SaveGuide(forceManual=False, showNotification=True):
	try:
		if showNotification:
			xbmc.executebuiltin("XBMC.Notification({0}, Saving Guide..., {1}, {2})".format(AddonName, 300000 ,icon))
		common.UpdateZipedFile(globalGuideFile, remoteSettings["globalGuide"]["url"])
		if forceManual:
			common.UpdatePlx(package["url"], plxFile)
			myFilmon.MakePLXguide(filmonGuideFile)
			if showNotification:
				xbmc.executebuiltin("XBMC.Notification({0}, Guide saved., {1}, {2})".format(AddonName, 5000 ,icon))
		else:
			if common.UpdateZipedFile(filmonGuideFile, package["guide"]):
				if showNotification:
					xbmc.executebuiltin("XBMC.Notification({0}, Guide saved., {1}, {2})".format(AddonName, 5000 ,icon))
			else:
				if showNotification:
					xbmc.executebuiltin("XBMC.Notification({0}, Guide is up to date., {1}, {2})".format(AddonName, 5000 ,icon))
		return True
	except:
		if showNotification:
			xbmc.executebuiltin("XBMC.Notification({0}, Guide NOT saved!, {1}, {2})".format(AddonName, 5000 ,icon))
		return False

def addDir(name, url, mode, iconimage, description, isFolder=True, channelName=None, background=None, isTvGuide=False):
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	
	if mode==3 or mode==4 or mode==7 or mode==8 or mode==10 or mode==11 or mode==12 or mode == 13 or mode == 14 or mode==15 or mode==99:
		isFolder=False
	
	if mode==3 or mode==4 or mode==10 or mode==11 or mode==12 or mode == 13 or mode == 14 or mode==15:
		liz.setProperty("IsPlayable","true")
		items = []

		if mode == 3:
			items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=9&iconimage={2}&displayname={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
			items.append(('Add to israelive-favorites', 'XBMC.RunPlugin({0}?url={1}&mode=17&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
		elif mode == 4:
			items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=9&iconimage={2}&displayname={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
			items.append(('Remove from israelive-favorites', "XBMC.RunPlugin({0}?url={1}&mode=18&iconimage={2}&name={3})".format(sys.argv[0], urllib.quote_plus(url), iconimage, name)))
		elif mode == 10 or mode == 12 or mode == 14:
			if isTvGuide:
				items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=5&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
			items.append(('Add to israelive-favorites', 'XBMC.RunPlugin({0}?url={1}&mode=17&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
		elif mode == 11 or mode == 13 or mode == 15:
			if isTvGuide:
				items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=5&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
			items.append(('Remove from israelive-favorites', 'XBMC.RunPlugin({0}?url={1}&mode=18&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, channelName)))
		

		liz.addContextMenuItems(items = items)
	
	if background is not None:
		liz.setProperty("Fanart_Image", background)

	fullUrl = "{0}?url={1}&mode={2}&name={3}&iconimage={4}&description={5}".format(sys.argv[0], urllib.quote_plus(url), mode, urllib.quote_plus(name), urllib.quote_plus(iconimage), urllib.quote_plus(description))
	if channelName is not None:
		fullUrl = "{0}&displayname={1}".format(fullUrl, urllib.quote_plus(channelName))
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=fullUrl, listitem=liz, isFolder=isFolder)
	return ok
	
def InstallAddon(url, description):
	urls = url.split(';')
	for url in urls:
		common.downloader_is(url, description)
	dlg = xbmcgui.Dialog()
	dlg.ok(AddonName, localizedString(30201).encode('utf-8'))
	
def UpdateChannelsLists():
	xbmc.executebuiltin("XBMC.Notification({0}, Updating Channels Lists..., {1}, {2})".format(AddonName, 300000 ,icon))
	remoteSettings = common.GetUpdatedList(remoteSettingsFile, remoteSettingsUrl)
	if remoteSettings == []:
		xbmc.executebuiltin('Notification({0}, Cannot load settings, {1}, {2})'.format(AddonName, 5000, icon))
		sys.exit()
	package = remoteSettings["packages"]["full"]
	common.UpdatePlx(package["url"], plxFile)
	xbmc.executebuiltin("XBMC.Notification({0}, Channels Lists updated., {1}, {2})".format(AddonName, 5000 ,icon))

def MakeIPTVlists():
	xbmc.executebuiltin("XBMC.Notification({0}, Making IPTV channels list..., {1}, {2})".format(AddonName, 300000 ,icon))
	portNum = 65007
	try:
		portNum = int(Addon.getSetting("LiveStreamerPort"))
	except:
		pass
	import myIPTV
	if not os.path.isfile(plxFile):
		common.UpdatePlx(package["url"], plxFile)
	myIPTV.makeIPTVlist(user_dataDir, "israelive.plx", "Main", os.path.join(user_dataDir, "iptv.m3u"), portNum)
	xbmc.executebuiltin("XBMC.Notification({0}, Making IPTV TV-guide..., {1}, {2})".format(AddonName, 300000 ,icon))
	myIPTV.MakeChannelsGuide(globalGuideFile, remoteSettings["globalGuide"]["url"], filmonGuideFile, package["guide"], os.path.join(user_dataDir, "guide.xml"))
	myIPTV.RefreshPVR(os.path.join(user_dataDir, "iptv.m3u"), os.path.join(user_dataDir, "guide.xml"), os.path.join(user_dataDir, "logos"))
	xbmc.executebuiltin("XBMC.Notification({0}, IPTV channels list and TV-guide created., {1}, {2})".format(AddonName, 5000 ,icon))
	
def DownloadLogos():
	xbmc.executebuiltin("XBMC.Notification({0}, Downloading channels logos..., {1}, {2})".format(AddonName, 300000 ,icon))
	import myIPTV
	if not os.path.isfile(plxFile):
		common.UpdatePlx(package["url"], plxFile)
	myIPTV.SaveChannelsLogos(user_dataDir, "israelive.plx", "Main", os.path.join(user_dataDir, "logos"))
	xbmc.executebuiltin("XBMC.Notification({0}, Chhannels logos saved., {1}, {2})".format(AddonName, 5000 ,icon))

def UpdateIPTVSimple():
	xbmc.executebuiltin("XBMC.Notification({0}, Updating IPTVSimple settings..., {1}, {2})".format(AddonName, 300000 ,icon))
	import myIPTV
	myIPTV.RefreshPVR(os.path.join(user_dataDir, "iptv.m3u"), os.path.join(user_dataDir, "guide.xml"), os.path.join(user_dataDir, "logos"), 0)
	xbmc.executebuiltin("XBMC.Notification({0}, IPTVSimple settings Updated., {1}, {2})".format(AddonName, 5000 ,icon))

def CleanLogosFolder():
	xbmc.executebuiltin("XBMC.Notification({0}, Cleaning channels logos folder..., {1}, {2})".format(AddonName, 300000 ,icon))
	logosFolder = os.path.join(user_dataDir, "logos")
	for the_file in os.listdir(logosFolder):
		file_path = os.path.join(logosFolder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception, e:
			print e
	xbmc.executebuiltin("XBMC.Notification({0}, Chhannels logos filder cleaned., {1}, {2})".format(AddonName, 5000 ,icon))

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
		
		
if useEPG and (not os.path.isfile(filmonGuideFile) or not os.path.isfile(globalGuideFile)):
	if not SaveGuide():
		useEPG = False
		
		
params = get_params()
url = None
name = None
mode = None
iconimage = None
description = None
displayname = None
ignoreFilmonGuide = False

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = params["name"]
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass
try:		
	mode = int(params["mode"])
except:
	pass
try:		
	description = urllib.unquote_plus(params["description"])
except:
	pass
try:		
	displayname = params["displayname"]
except:
	pass
try:	
	if url is not None and url.find("&ignorefilmonguide=1") > 0:
		ignoreFilmonGuide = True
except:
	pass
		
#print "{0} -> Mode: {1}".format(AddonName, mode)
#print "{0} -> URL: {1}".format(AddonName, url)
#print "{0} -> Name: {1}".format(AddonName, urllib.unquote_plus(str(name)))
#print "{0} -> IconImage: {1}".format(AddonName, iconimage)
		 
if mode==None:# or url==None or len(url)<1:
	CATEGORIES()
elif mode==1:
	PlayFilmon(sys.argv[2])
elif mode==2:
	ListLive(urllib.unquote_plus(displayname), iconimage)
elif mode==3 or mode==4:
	PlayFilmon(url, displayname, ignoreFilmonGuide)
elif mode == 5:
	ChannelGuide(name, iconimage)
elif mode==7:
	update_view(url) 
elif mode==8:
	InstallAddon(url, description)
elif mode==9:   
	FilmonChannelGuide(url, displayname, iconimage, ignoreFilmonGuide)
elif mode==10 or mode==11:
	PlayChannel(url, displayname, iconimage)
elif mode==12 or mode==13:
	Playf4m(url, displayname, iconimage)
elif mode==14 or mode==15:
	PlayGLArabLink(url[:url.find('?mode')], displayname, iconimage)
elif mode==16:
	listFavorites()
elif mode==17: 
	addFavorites(url, iconimage, name) 
elif mode==18:
	removeFavorties(url)
elif mode == 20: # Download Guide now - from server
	SaveGuide()
	sys.exit()
elif mode == 21: # Create Guide now (local scan)
	SaveGuide(forceManual=True)
	sys.exit()
elif mode == 22: # Update Channels Lists now
	UpdateChannelsLists()
	sys.exit()
elif mode == 30: # Make IPTV channels list and TV-guide
	MakeIPTVlists()
	sys.exit()
elif mode == 31: # Download channels logos
	DownloadLogos()
	sys.exit()
elif mode == 32: # Update IPTVSimple settings
	UpdateIPTVSimple()
	sys.exit()
elif mode == 33: # Empty channels logos folder
	CleanLogosFolder()
	sys.exit()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
