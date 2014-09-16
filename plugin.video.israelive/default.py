# -*- coding: utf-8 -*-
#code by Avigdor 
import urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, time
import xml.etree.ElementTree as ET
from datetime import timedelta, datetime

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
icon = Addon.getAddonInfo('icon')
addonDir = Addon.getAddonInfo('path').decode("utf-8")
libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import common, myFilmon, myIPTVSimple

AddonLogosDir = os.path.join(addonDir, 'resources', 'logos')
addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)
epgFile = os.path.join(addon_data_dir, 'guide.xml')

def Categories():
	addDir("[COLOR orange][{0}][/COLOR]".format(localizedString(20101).encode('utf-8')), "settings", 10, os.path.join(AddonLogosDir, "settings.jpg"))
	
	lists = ["israel", "news", "music", "radio", "localRadio", "france", "russia", "others"]
	markedLists = common.GetMarkedLists()
	for listName in markedLists:
		if listName == "israel":
			Category(listName)
		else:
			addDir("[COLOR blue][{0}][/COLOR]".format(localizedString(30101 + lists.index(listName)).encode('utf-8')) , listName, 1, os.path.join(AddonLogosDir, "{0}.png".format(listName)))
			
def Category(categoryName):	
	list = common.ReadChannelsList(categoryName)
	common.updateLogos(list)
	
	logosDir = os.path.join(addon_data_dir, 'logos')

	epgFileLastUpdate = common.getFileLastUpdate(epgFile)
	now = int(time.time())
	isEpgUpdate = True if (now - epgFileLastUpdate) < 86400 else False # 24 hours
	if not isEpgUpdate:
		myIPTVSimple.RefreshEPG(updateIPTVSimple=False)
	epg = ET.parse(epgFile)
	
	for channel in list:
		description = ""
		logoFile = os.path.join(logosDir, "{0}.png".format(channel["logo"]))
		tvg_id = channel["tvg_id"].encode("utf-8")

		channelName = "[COLOR yellow]{0}[/COLOR]".format(channel["display_name"].encode("utf-8"))
		programme = GetProgrammes(epg, tvg_id)

		if programme is not None:
			programmeDetails = GetGetProgrammeDetails(programme)
			programmeName = "[COLOR orange]{0}[/COLOR] [COLOR grey][{1}-{2}][/COLOR]".format(programmeDetails["title"], programmeDetails["start"].strftime('%H:%M'), programmeDetails["stop"].strftime('%H:%M'))
			channelName = "{0} - {1}".format(channelName, programmeName)
			description = programmeDetails["desc"]
		else:
			tvg_id = None
			
		mode = 3 if channel["type"]== "filmon" else 2
		addDir(channelName, channel["url"], mode, logoFile, description, tvg_id=tvg_id, display_name=channel["display_name"].encode("utf-8"), isFolder=False)
		
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin("Container.SetViewMode(515)")

def SettingsCat():
	addDir("[COLOR orange]{0}[/COLOR]".format(localizedString(20102).encode('utf-8')), 'settings', 11, os.path.join(AddonLogosDir, "settings.jpg"), isFolder=False)
	addDir("[COLOR orange]{0}[/COLOR]".format(localizedString(20103).encode('utf-8')), 'settings', 12, os.path.join(AddonLogosDir, "settings.jpg"), isFolder=False)

def GetProgrammes(epg, channelName ,full=False):
	try:
		programmes = epg.findall('.//programme[@channel="{0}"]'.format(channelName))
	except:
		return None
	
	if (full):
		return programmes
		
	now = datetime.now()
	for programme in programmes:
		start = programme.get('start')
		stop = programme.get('stop')
		programmeStart = datetime(int(start[:4]), int(start[4:6]), int(start[6:8]), int(start[8:10]), int(start[10:12]), int(start[12:14]))#, tzinfo=IsraelTime())
		programmeStop = datetime(int(stop[:4]), int(stop[4:6]), int(stop[6:8]), int(stop[8:10]), int(stop[10:12]), int(stop[12:14]))#, tzinfo=IsraelTime())
		#programmeStart = programmeStart + timedelta(seconds=3*60*60)
		if (programmeStart < now and now < programmeStop):
			return programme
			
	return None
	
def GetGetProgrammeDetails(programme):
	start = programme.get('start')
	stop = programme.get('stop')
	item_data = {"start": datetime(int(start[:4]), int(start[4:6]), int(start[6:8]), int(start[8:10]), int(start[10:12]), int(start[12:14]))}
	item_data["stop"] = datetime(int(stop[:4]), int(stop[4:6]), int(stop[6:8]), int(stop[8:10]), int(stop[10:12]), int(stop[12:14]))
	programmeDetails = list(programme)
	for PD in programmeDetails:
		item_data[PD.tag.lower()] = PD.text.encode("utf-8")
		
	return item_data

def ChannelGuide(tvg_id, channelName, iconimage):
	epg = ET.parse(epgFile)
	programmes = GetProgrammes(epg, tvg_id, full=True)
	
	if programmes is None:
		addDir('[COLOR red][B]No TV-Guide for "{0}".[/B][/COLOR]'.format(channelName), '.', 99, iconimage)
	else:
		addDir('------- [COLOR yellow][B]{0}[/COLOR] - [COLOR orange]TV-Guide[/B][/COLOR] -------'.format(channelName), '.', 99, iconimage)
		now = datetime.now()
		day = ""
		for programme in programmes:
			programmeDetails = GetGetProgrammeDetails(programme)
			if now > programmeDetails["stop"]:
				continue
			startdate = programmeDetails["start"].strftime('%d/%m/%y')
			if startdate != day:
				day = startdate
				addDir('[COLOR white][B]{0}:[/B][/COLOR]'.format(day), '.', 99, iconimage)
			programmeName = "[COLOR orange][{0}-{1}][/COLOR] [COLOR yellow][B]{2}[/B][/COLOR]".format(programmeDetails["start"].strftime('%H:%M'), programmeDetails["stop"].strftime('%H:%M'), programmeDetails["title"])
			description = programmeDetails["desc"]
			addDir(programmeName, tvg_id, 99, iconimage, description)
		
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin("Container.SetViewMode(515)")
	
def FilmonChannelGuide(chNum):
	channelName, channelDescription, iconimage, tvGuide = myFilmon.GetChannelGuide(chNum)

	if tvGuide == None:
		addDir('[COLOR red][B]No TV-Guide for this channel.[/B][/COLOR]', '.', 99, '', '')
		return
	elif len(tvGuide) == 0:
		addDir('[COLOR red][B]No TV-Guide for "{0}".[/B][/COLOR]'.format(channelName), '.', 99, iconimage, channelDescription)
	else:
		addDir('------- [COLOR yellow][B]{0}[/COLOR] - [COLOR orange]TV-Guide[/B][/COLOR] -------'.format(channelName), '.', 99, iconimage, channelDescription)
		day = ""
		for programme in tvGuide:
			startdate = datetime.fromtimestamp(programme[0]).strftime('%d/%m/%y')
			if startdate != day:
				day = startdate
				addDir('[COLOR white][B]{0}:[/B][/COLOR]'.format(day), '.', 99, iconimage, channelDescription)
			startdatetime = datetime.fromtimestamp(programme[0]).strftime('%H:%M')
			enddatetime = datetime.fromtimestamp(programme[1]).strftime('%H:%M')
			programmename = '[COLOR orange][{0}-{1}][/COLOR] [COLOR yellow][B]{2}[/B][/COLOR]'.format(startdatetime,enddatetime,programme[2])
			description = programme[3]
			image = programme[4] if programme[4] else iconimage
			addDir(programmename, chNum, 99, image, description)
		
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin("Container.SetViewMode(515)")
	
def RefreshIPTVlinks():
	if myIPTVSimple.RefreshIPTVlinks():
		xbmc.executebuiltin('StartPVRManager')

def PlayUrl(name, url, iconimage=None):
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def PlayFilmon(chNum):
	direct, channelName, programmeName, iconimage = myFilmon.GetChannelStream(chNum)
	if direct == None:
		return
	PlayUrl(programmeName, direct, iconimage)

def addDir(name, url, mode, iconimage, description="", tvg_id=None, display_name=None, isFolder=True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)

	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
	if (mode == 2 or mode == 3):
		liz.setProperty('IsPlayable', 'true')
		if tvg_id is not None:
			liz.addContextMenuItems(items = [('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=8&name={2}&iconimage={3})'.format(sys.argv[0], urllib.quote_plus(tvg_id), urllib.quote_plus(display_name), urllib.quote_plus(iconimage)))])
		elif mode == 3:
			liz.addContextMenuItems(items = [('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=9&iconimage={2})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage)))])
	elif mode == 99:
		isFolder = False
		
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

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
url=None
name=None
mode=None
iconimage=None
description=None

try:
	url = urllib.unquote_plus(params["url"])
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
	mode = int(params["mode"])
except:
	pass
try:        
	description = urllib.unquote_plus(params["description"])
except:
	pass
 
if mode == None or url == None or len(url) < 1:
	Categories()
elif mode == 1:
	Category(url)
elif mode == 2:
	PlayUrl(name, url, iconimage)
elif mode == 3:
	PlayFilmon(url)
elif mode == 8:
	ChannelGuide(url, name, iconimage)
elif mode==9:   
	FilmonChannelGuide(url)
elif mode== 10:
	SettingsCat()
elif mode == 11:
	Addon.openSettings()
elif mode == 12:
	RefreshIPTVlinks()
elif mode == 20:
	RefreshIPTVlinks()
	sys.exit()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
