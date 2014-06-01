# -*- coding: utf-8 -*-
#code by Avigdor 
import urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
icon = Addon.getAddonInfo('icon')
AddonLogosDir = os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), AddonID, 'resources', 'logos')

libDir = os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import common, myFilmon, myIPTVSimple

def Categories():
	addDir("[COLOR yellow][{0}][/COLOR]".format(localizedString(20101).encode('utf-8')), "settings", 10, os.path.join(AddonLogosDir, "settings.jpg"))
	
	lists = ["israel", "news", "music", "radio", "localRadio", "france", "russia", "others"]
	markedLists = common.GetMarkedLists()
	for listName in markedLists:
		if listName == "israel":
			Category(listName)
		else:
			addDir("[COLOR blue][{0}][/COLOR]".format(localizedString(30101 + lists.index(listName)).encode('utf-8')) , listName, 1, os.path.join(AddonLogosDir, "{0}.png".format(listName)))
			
def Category(categoryName):	
	logosDir = os.path.join(xbmc.translatePath("special://userdata/addon_data").decode("utf-8"), AddonID, 'logos')
	list = common.ReadChannelsList(categoryName)
	common.updateLogos(list)
	for channel in list:
		logoFile = os.path.join(logosDir, "{0}.png".format(channel["logo"]))
		mode = 3 if channel["type"]== "filmon" else 2
		addDir(channel["display_name"].encode("utf-8"), channel["url"], mode, logoFile, isFolder=False)

def SettingsCat():
	addDir(localizedString(20102).encode('utf-8'), 'settings', 11, os.path.join(AddonLogosDir, "settings.jpg"), isFolder=False)
	addDir(localizedString(20103).encode('utf-8'), 'settings', 12, os.path.join(AddonLogosDir, "settings.jpg"), isFolder=False)
	
def PlayUrl(name, url, iconimage=None):
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def PlayFilmon(chNum):
	direct, channelName, programmeName, iconimage = myFilmon.GetChannelStream(chNum)
	if direct == None:
		return
	PlayUrl(programmeName, direct, iconimage)

def addDir(name, url, mode, iconimage, description="", isFolder=True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)

	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	if (mode == 2 or mode == 3):
		liz.setProperty('IsPlayable', 'true')
	
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
elif mode== 10:
	SettingsCat()
elif mode == 11:
	Addon.openSettings()
elif mode == 12:
	if myIPTVSimple.RefreshIPTVlinks():
		xbmc.executebuiltin('StartPVRManager')
		#common.OKmsg("IsraeLIVE", "Links updated.", "Please restart XBMC or PVR db.")

xbmcplugin.endOfDirectory(int(sys.argv[1]))
