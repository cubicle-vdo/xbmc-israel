# -*- coding: utf-8 -*-
# code by Avigdor (https://github.com/cubicle-vdo/xbmc-israel)
import urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json

AddonID = 'plugin.video.playlistLoader'
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')

addonDir = Addon.getAddonInfo('path').decode("utf-8")

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import common

addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)
	
playlistsFile = os.path.join(addon_data_dir, "playLists.txt")
tmpListFile = os.path.join(addon_data_dir, 'tempList.txt')
favoritesFile = os.path.join(addon_data_dir, 'favorites.txt')
if  not (os.path.isfile(favoritesFile)):
	f = open(favoritesFile, 'w') 
	f.write('[]') 
	f.close() 
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')
	
def Categories():
	AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(getLocaleString(10001)), "settings" , 20, os.path.join(addonDir, "resources", "images", "NewList.ico"), isFolder=False)
	AddDir("[COLOR white][B][{0}][/B][/COLOR]".format(getLocaleString(10003)), "favorites" ,30 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"))
	
	i = 0
	list = common.ReadList(playlistsFile)
	for item in list:
		mode = 1 if item["url"].find(".plx") > 0 else 2
		name = common.GetEncodeString(item["name"])
		image = item.get('image', '')
		if mode == 1:
			logos = ''
		else:
			logos = item.get('logos', '')
		AddDir("[COLOR blue][{0}][/COLOR]".format(name) ,item["url"].encode("utf-8"), mode, image.encode("utf-8"), logos.encode("utf-8"), index=i)
		i += 1

def AddNewList():
	listName = GetKeyboardText(getLocaleString(10004)).strip()
	if len(listName) < 1:
		return
	listUrl = GetChoice(10002, 10005, 10006, 10016, 10017, fileType=1, fileMask='.plx|.m3u|.m3u8')
	if len(listUrl) < 1:
		return
	image = GetChoice(10022, 10022, 10022, 10024, 10025, 10021, fileType=2)
	if listUrl.endswith('.plx'):
		logosUrl = ''
	else:
		logosUrl = GetChoice(10018, 10019, 10020, 10019, 10020, 10021, fileType=0)
		if logosUrl.startswith('http') and not logosUrl.endswith('/'):
			logosUrl += '/'
	list = common.ReadList(playlistsFile)
	for item in list:
		if item["url"].lower() == listUrl.lower():
			xbmc.executebuiltin('Notification({0}, "{1}" {2}, 5000, {3})'.format(AddonName, listName, getLocaleString(10007), icon))
			return
	list.append({"name": listName.decode("utf-8"), "url": listUrl, "image": image, "logos": logosUrl})
	if common.SaveList(playlistsFile, list):
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def GetChoice(choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone=None, fileType=1, fileMask=None, defaultText=""):
	choice = ''
	choiceList = [getLocaleString(choiceFile), getLocaleString(choiceUrl)]
	if choiceNone != None:
		choiceList.append(getLocaleString(choiceNone))
	method = GetSourceLocation(getLocaleString(choiceTitle), choiceList)	
	if method == 0:
		if not defaultText.startswith('http'):
			defaultText = ""
		choice = GetKeyboardText(getLocaleString(fileTitle), defaultText).strip().decode("utf-8")
	elif method == 1:
		if defaultText.startswith('http'):
			defaultText = ""
		choice = xbmcgui.Dialog().browse(fileType, getLocaleString(urlTitle), 'myprograms', fileMask, False, False, defaultText).decode("utf-8")
	return choice
	
def RemoveFromLists(index, listFile):
	list = common.ReadList(listFile) 
	if index < 0 or index >= len(list):
		return
	del list[index]
	common.SaveList(listFile, list)
	xbmc.executebuiltin("XBMC.Container.Refresh()")
			
def PlxCategory(url):
	tmpList = []
	list = common.plx2list(url)
	background = list[0]["background"]
	for channel in list[1:]:
		iconimage = "" if not channel.has_key("thumb") else common.GetEncodeString(channel["thumb"])
		name = common.GetEncodeString(channel["name"])
		if channel["type"] == 'playlist':
			AddDir("[COLOR blue][{0}][/COLOR]".format(name) ,channel["url"].encode("utf-8"), 1, iconimage, background=background.encode("utf-8"))
		else:
			AddDir(name, channel["url"].encode("utf-8"), 3, iconimage, isFolder=False, background=background)
			tmpList.append({"url": channel["url"], "image": iconimage.decode("utf-8"), "name": name.decode("utf-8")})
			
	common.SaveList(tmpListFile, tmpList)
			
def m3uCategory(url, logos):	
	tmpList = []
	list = common.m3u2list(url)

	for channel in list:
		name = common.GetEncodeString(channel["display_name"])
		image = channel.get("tvg_logo", "")
		if image == "":
			image = channel.get("logo", "")
		if logos is not None and logos != '' and image is not None and image != '' and not image.startswith('http'):
			image = logos + image
		url = common.GetEncodeString(channel["url"])
		AddDir(name ,url, 3, image, isFolder=False)
		tmpList.append({"url": url.decode("utf-8"), "image": image.decode("utf-8"), "name": name.decode("utf-8")})

	common.SaveList(tmpListFile, tmpList)
		
def PlayUrl(name, url, iconimage=None):
	print '--- Playing "{0}". {1}'.format(name, url)
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage, logos="", index=-1, move=0, isFolder=True, background=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&logos="+urllib.quote_plus(logos)+"&index="+str(index)+"&move="+str(move)

	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={ "Title": name})
	listMode = 21 # Lists
	if background != None:
		liz.setProperty('fanart_image', background)
	if mode == 1 or mode == 2:
		items = [(getLocaleString(10008), 'XBMC.RunPlugin({0}?index={1}&mode=22)'.format(sys.argv[0], index)),
		(getLocaleString(10026), 'XBMC.RunPlugin({0}?index={1}&mode=23)'.format(sys.argv[0], index)),
		(getLocaleString(10027), 'XBMC.RunPlugin({0}?index={1}&mode=24)'.format(sys.argv[0], index)),
		(getLocaleString(10028), 'XBMC.RunPlugin({0}?index={1}&mode=25)'.format(sys.argv[0], index))]
		if mode == 2:
			items.append((getLocaleString(10029), 'XBMC.RunPlugin({0}?index={1}&mode=26)'.format(sys.argv[0], index)))
	elif mode == 3:
		liz.setProperty('IsPlayable', 'true')
		liz.addContextMenuItems(items = [('{0}'.format(getLocaleString(10009)), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
	elif mode == 32:
		liz.setProperty('IsPlayable', 'true')
		items = [(getLocaleString(10010), 'XBMC.RunPlugin({0}?index={1}&mode=33)'.format(sys.argv[0], index)),
		(getLocaleString(10026), 'XBMC.RunPlugin({0}?index={1}&mode=35)'.format(sys.argv[0], index)),
		(getLocaleString(10027), 'XBMC.RunPlugin({0}?index={1}&mode=36)'.format(sys.argv[0], index)),
		(getLocaleString(10028), 'XBMC.RunPlugin({0}?index={1}&mode=37)'.format(sys.argv[0], index))]
		listMode = 38 # Favourits
	if mode == 1 or mode == 2 or mode == 32:
		items += [(getLocaleString(10030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, listMode)),
		(getLocaleString(10031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, listMode)),
		(getLocaleString(10032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, listMode))]
		liz.addContextMenuItems(items)
		
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text = "" if not keyboard.isConfirmed() else keyboard.getText()
	return text

def GetSourceLocation(title, list):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, list)
	return answer
	
def AddFavorites(url, iconimage, name):
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(10011), icon))
			return
	list = common.ReadList(tmpListFile)	
	for channel in list:
		if channel["name"].lower() == name.decode("utf-8").lower():
			url = channel["url"].encode("utf-8")
			iconimage = channel["image"].encode("utf-8")
			break
	if not iconimage:
		iconimage = ""
	data = {"url": url.decode("utf-8"), "image": iconimage.decode("utf-8"), "name": name.decode("utf-8")}
	favList.append(data)
	common.SaveList(favoritesFile, favList)
	xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(10012), icon))
	
def ListFavorites():
	AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(getLocaleString(10013)), "favorites" ,34 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"), isFolder=False)
	list = common.ReadList(favoritesFile)
	i = 0
	for channel in list:
		AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), 32, channel["image"].encode("utf-8"), index=i, isFolder=False)
		i += 1
		
def AddNewFavorite():
	chName = GetKeyboardText(getLocaleString(10014))
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText(getLocaleString(10015))
	if len(chUrl) < 1:
		return
	image = GetChoice(10023, 10023, 10023, 10024, 10025, 10021, fileType=2)
		
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == chUrl.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, getLocaleString(10011), icon))
			return
			
	data = {"url": chUrl.decode("utf-8"), "image": image, "name": chName.decode("utf-8")}
	
	favList.append(data)
	if common.SaveList(favoritesFile, favList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def ChangeKey(index, listFile, key, title):
	list = common.ReadList(listFile)
	str = GetKeyboardText(getLocaleString(title), list[index][key].encode("utf-8"))
	if len(str) < 1:
		return
	list[index][key] = str.decode("utf-8")
	if common.SaveList(listFile, list):
		xbmc.executebuiltin("XBMC.Container.Refresh()")
		
def ChangeChoice(index, listFile, key, choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone=None, fileType=1, fileMask=None):
	list = common.ReadList(listFile)
	if key == "logos":
		listUrl = list[index].get("url", "")
		if listUrl.endswith('.plx'):
			return
	defaultText = list[index].get(key, "")
	str = GetChoice(choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone, fileType, fileMask, defaultText.encode("utf-8"))
	if key == "url" and len(str) < 1:
		return
	elif key == "logos" and str.startswith('http') and not str.endswith('/'):
		str += '/'
	list[index][key] = str.decode("utf-8")
	if common.SaveList(listFile, list):
		xbmc.executebuiltin("XBMC.Container.Refresh()")
	
def MoveInList(index, step, listFile):
	theList = common.ReadList(listFile)
	if index + step >= len(theList) or index + step < 0:
		return
	if step == 0:
		step = GetIndexFromUser(len(theList), index)
	if step < 0:
		tempList = theList[0:index + step] + [theList[index]] + theList[index + step:index] + theList[index + 1:]
	elif step > 0:
		tempList = theList[0:index] + theList[index +  1:index + 1 + step] + [theList[index]] + theList[index + 1 + step:]
	else:
		return
	common.SaveList(listFile, tempList)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def GetIndexFromUser(listLen, index):
	dialog = xbmcgui.Dialog()
	location = dialog.input('{0} (1-{1})'.format(getLocaleString(10033), listLen), type=xbmcgui.INPUT_NUMERIC)
	if location is None or location == "":
		return 0
	try:
		location = int(location) - 1
		if location >= listLen or location < 0:
			return 0
	except:
		return 0
	return location - index

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
logos=None
name=None
mode=None
iconimage=None
description=None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	logos = urllib.unquote_plus(params.get("logos", ''))
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
	index = int(params["index"])
except:
	pass
try:        
	move = int(params["move"])
except:
	pass

	
if mode == None:
	Categories()
elif mode == 1:
	PlxCategory(url)
elif mode == 2:
	m3uCategory(url, logos)
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage)
elif mode == 20:
	AddNewList()
elif mode == 21:
	MoveInList(index, move, playlistsFile)
elif mode == 22:
	RemoveFromLists(index, playlistsFile)
elif mode == 23:
	ChangeKey(index, playlistsFile, "name", 10004)
elif mode == 24:
	ChangeChoice(index, playlistsFile, "url", 10002, 10005, 10006, 10016, 10017, None, 1, '.plx|.m3u|.m3u8')
elif mode == 25:
	ChangeChoice(index, playlistsFile, "image", 10022, 10022, 10022, 10024, 10025, 10021, 2)
elif mode == 26:
	ChangeChoice(index, playlistsFile, "logos", 10018, 10019, 10020, 10019, 10020, 10021, 0)
elif mode == 27:
	common.DelFile(playlistsFile)
	sys.exit()
elif mode == 30:
	ListFavorites()
elif mode == 31: 
	AddFavorites(url, iconimage, name) 
elif mode == 33:
	RemoveFromLists(index, favoritesFile)
elif mode == 34:
	AddNewFavorite()
elif mode == 35:
	ChangeKey(index, favoritesFile, "name", 10014)
elif mode == 36:
	ChangeKey(index, favoritesFile, "url", 10015)
elif mode == 37:
	ChangeChoice(index, favoritesFile, "image", 10023, 10023, 10023, 10024, 10025, 10021, 2)
elif mode == 38:
	MoveInList(index, move, favoritesFile)
elif mode == 39:
	common.DelFile(favoritesFile)
	sys.exit()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
