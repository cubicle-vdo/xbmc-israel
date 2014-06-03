# -*- coding: utf-8 -*-
#code by Avigdor 
import urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json

AddonID = 'plugin.video.playlistLoader'
Addon = xbmcaddon.Addon(AddonID)
#localizedString = Addon.getLocalizedString
icon = Addon.getAddonInfo('icon')

libDir = os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import common

addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)
	
playlistsFile = os.path.join(addon_data_dir, "playLists.txt")

def Categories():
	addDir("[COLOR yellow][Add new list][/COLOR]".format("xbmcil").encode('utf-8') , "settings" , 20, os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), AddonID, 'resources', 'images', "NewList.ico"), isFolder=False)
	
	list = common.ReadList(playlistsFile)
	for item in list:
		mode = 1 if item["url"].find(".plx") > 0 else 2
		addDir("[COLOR blue][{0}][/COLOR]".format(item["name"]).encode('utf-8') ,item["url"], mode, "")

def AddNewList():
	keyboard = xbmc.Keyboard("", "Playlist name")
	keyboard.doModal()
	if keyboard.isConfirmed():
		listName = keyboard.getText()
	else:
		return
		
	keyboard = xbmc.Keyboard("", "Playlist URL")
	keyboard.doModal()
	if keyboard.isConfirmed():
		listUrl = keyboard.getText()
	else:
		return
	
	print "{0}. {1}".format(listName, listUrl)
	
	list = common.ReadList(playlistsFile)
	for item in list:
		if item["url"].lower() == listUrl.lower():
			xbmc.executebuiltin('Notification(Playlist Loader, "{0}" already in playlists, 5000, {1})'.format(listName, icon))
			return
	list.append({"name": listName, "url": listUrl})
	if common.SaveList(playlistsFile, list):
		xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
	
def removeFavorties(url):
	list = common.ReadList(playlistsFile)
	for item in list:
		if item["url"].lower() == url.lower():
			list.remove(item)
			if common.SaveList(playlistsFile, list):
				xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
			break
			
def PlxCategory(url):
	list = common.plx2list(url)
	for channel in list:
		iconimage = "" if not channel.has_key("thumb") else channel["thumb"]
		if channel["type"] == 'playlist':
			addDir("[COLOR blue][{0}][/COLOR]".format(channel["name"]).encode('utf-8') ,channel["url"], 1, iconimage)
		else:
			addDir(channel["name"].encode('utf-8') ,channel["url"], 3, iconimage, isFolder=False)
			
def m3uCategory(url):	
	list = common.m3u2list(url)
	for channel in list:
		iconimage = "" if not channel.has_key("tvg_logo") else channel["tvg_logo"]
		addDir(channel["display_name"].encode('utf-8') ,channel["url"], 3, iconimage, isFolder=False)
	
def PlayUrl(name, url, iconimage=None):
	print '--- Playing "{0}". {1}'.format(name, url).encode('utf-8')
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def addDir(name, url, mode, iconimage, description="", isFolder=True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)

	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	if mode == 3:
		liz.setProperty('IsPlayable', 'true')
	if mode == 1 or mode == 2:
		items = []
		items.append(('Remove from Playlist Loader', 'XBMC.RunPlugin({0}?url={1}&mode=21)'.format(sys.argv[0], urllib.quote_plus(url), iconimage,name)))
		liz.addContextMenuItems(items = items)
	
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
	PlxCategory(url)
elif mode == 2:
	m3uCategory(url)
elif mode == 3:
	PlayUrl(name, url, iconimage)
elif mode == 20:
	AddNewList()
elif mode == 21:
	removeFavorties(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
