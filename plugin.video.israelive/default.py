# -*- coding: utf-8 -*-
#code by Avigdor 
import urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
icon = Addon.getAddonInfo('icon')

libDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import myIPTVSimple, common

listsFile = os.path.join(xbmc.translatePath("special://userdata/addon_data"), AddonID, 'lists', "lists.list")

def Categories():
	logosDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'logos')
	
	isRadio = False if (Addon.getSetting('radio').lower() == 'false') else True
	if isRadio:
		addDir("[COLOR blue][{0}][/COLOR]".format(localizedString(30102).encode('utf-8')) ,"radio", 1, os.path.join(logosDir, "radio.jpg"), description=localizedString(30102).encode('utf-8'))
	
	Category("israel")
	
	isFrench = False if (Addon.getSetting('french').lower() == 'false') else True
	if isFrench:
		addDir("[COLOR blue][{0}][/COLOR]".format(localizedString(30103).encode('utf-8')) ,"france", 1, os.path.join(logosDir, "france.png"), description=localizedString(30103).encode('utf-8'))
	isRussian = False if (Addon.getSetting('russian').lower() == 'false') else True
	if isRussian:
		addDir("[COLOR blue][{0}][/COLOR]".format(localizedString(30104).encode('utf-8')) ,"russia", 1, os.path.join(logosDir, "russia.png"), description=localizedString(30104).encode('utf-8'))

def Category(categoryName):	
	lists = ReadList(listsFile)

	logosDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'logos')
	
	for channel in lists[categoryName]:
		logoFile = os.path.join(logosDir, "{0}.png".format(channel["tvg_id"]))
		addDir(channel["display_name"].encode("utf-8"), channel["url"], 2, logoFile, isFolder=False)

def PlayUrl(name, url, iconimage=None):
	listitem = xbmcgui.ListItem(name, path=url)
	if iconimage:
		listitem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def ReadList(fileName):
	try:
		f = open(fileName,'r')
		fileContent = f.read()
		f.close()
		content = json.loads(fileContent)
	except:
		content = []

	return content
	
def addDir(name, url, mode, iconimage, description="", isFolder=True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)

	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	if (not isFolder):
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
 
if not os.path.isfile(listsFile):
	common.UpdateLists()
	
if mode == None or url == None or len(url) < 1:
	Categories()
elif mode == 1:
	Category(url)
elif mode == 2:
	PlayUrl(name, url, iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
