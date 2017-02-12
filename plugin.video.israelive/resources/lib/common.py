# -*- coding: utf-8 -*-
import os, io, re, time, base64, random, hashlib, urllib2, json, gzip
from StringIO import StringIO
import xbmc, xbmcgui, xbmcaddon
import multiChoiceDialog, UA

resolverAddonID = "script.module.israeliveresolver"
AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = "IsraeLIVE"
localizedString = Addon.getLocalizedString
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
listsFile = os.path.join(user_dataDir, "israelive.list")
favoritesFile = os.path.join(user_dataDir, 'favorites.txt')
remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")
listsDir = os.path.join(user_dataDir, 'lists')
if not os.path.exists(listsDir):
	os.makedirs(listsDir)

def isFileOld(file, deltaInSec):
	lastUpdate = 0 if not os.path.isfile(file) else int(os.path.getmtime(file))
	now = int(time.time())
	isFileNotUpdate = True if (now - lastUpdate) > deltaInSec else False 
	return isFileNotUpdate
	
def GetSubKeyValue(remoteSettings, key, subKey):
	return remoteSettings[key][subKey] if (remoteSettings and remoteSettings.has_key(key) and remoteSettings[key].has_key(subKey)) else None
	
def UpdateFile(file, key, remoteSettings=None, zip=False, forceUpdate=False):
	if remoteSettings is None:
		remoteSettings = ReadList(remoteSettingsFile)
	if remoteSettings == []:
		return False
	i = file.rfind('.')
	zipFile = "{0}.zip".format(file[:i])
	lastModifiedFile = "{0}LastModified.txt".format(file[:i])
	if (not zip and not os.path.isfile(file)) or not os.path.isfile(lastModifiedFile):
		old_modified = "0"
	else:
		with open(lastModifiedFile, 'r') as f:
			old_modified = f.read()
	last_modified = GetSubKeyValue(remoteSettings, key, "lastModified")
	
	if not (forceUpdate or last_modified is None or (old_modified < last_modified)):
		return False
	
	urls = GetSubKeyValue(remoteSettings, key, "urls")
	if urls is None or len(urls) == 0:
		return False
		
	url1 = random.choice(urls)
	urla = Decode(url1).split(';')
	url = urla[0]
	a = '' if len(urla) < 2 else urla[1]
	
	if a == Decode('ttk='):
		response = None
		try:
			req = urllib2.Request(url)
			req.add_header(Decode('nubX05KNsLuzvQ=='), Decode('luLsytG4qoV6d6OSiby1t7q0wOaSr7lsf4R2hJPk1599eoR1cpO5xsi3uIV3eaSikZZ8enaLsuXXx9TEeId2d6M='))
			req.add_header(Decode('m9jYxtexuw=='), Decode('sefm0Z97eM28wKG71NetrqKOn7ig0NezeA=='))
			response = urllib2.urlopen(req)
			text = response.read()
			match = re.compile(Decode('tMHBgaJsa35zc7Kbg6A=')).findall(text)
			response.close()
			if len(match) < 1:
				return False
			url = Decode('xKPvoNeJxIfC').format(match[0], random.randint(0, 9223372036854775807))
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)
			if response is not None:
				response.close()
			return False
	
	response = None
	try:
		req = urllib2.Request(url)
		if a == Decode('ttk='):
			req.add_header('User-Agent', UA.GetUA())
		else:
			req.add_header(Decode('nubX05KNsLuzvQ=='), Decode('luLsytG4qoV6d6OSiby1t7q0wOaSr7lsf4R2hJPk1599eoR1cpO5xsi3uIV3eaSikZZ8enaLsuXXx9TEeId2d6M='))
			req.add_header(Decode('m9jYxtexuw=='), Decode('sefm0Z97eM28wKG71NetrqKOn7ig0NezeA=='))
		req.add_header('Accept-encoding', 'gzip')
		response = urllib2.urlopen(req)
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		else:
			data = response.read()
		response.close()
		if zip:
			with open(zipFile, 'wb') as f:
				f.write(data)
			xbmc.executebuiltin("XBMC.Extract({0}, {1})".format(zipFile, user_dataDir), True)
			try:
				os.remove(zipFile)
			except:
				pass
		else:
			data = data.replace('\r','')
			with open(file, 'w') as f:
				f.write(data)
		if key == "remoteSettings":
			remoteSettings = json.loads(data)
			last_modified = GetSubKeyValue(remoteSettings, key, "lastModified")
		elif key == "remoteSettingsZip":
			remoteSettings = ReadList(remoteSettingsFile)
			last_modified = GetSubKeyValue(remoteSettings, key, "lastModified")
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		if response is not None:
			response.close()
		return False
	with open(lastModifiedFile, 'w') as f:
		f.write(last_modified)
	return True
	
def ReadList(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		content=[]

	return content

def WriteList(filename, list, indent=True):
	try:
		with io.open(filename, 'w', encoding='utf-8') as handle:
			if indent:
				handle.write(unicode(json.dumps(list, indent=2, ensure_ascii=False)))
			else:
				handle.write(unicode(json.dumps(list, ensure_ascii=False)))
		success = True
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		success = False
		
	return success
	
def GetUnSelectedList(fullList, selectedList):
	unSelectedList = []
	for index, item in enumerate(fullList):
		if not any(selectedItem["id"] == item.get("id", "") for selectedItem in selectedList):
			unSelectedList.append(item)
	return unSelectedList
	
def GetEncodeString(str):
	try:
		import chardet
		str = str.decode(chardet.detect(str)["encoding"]).encode("utf-8")
	except:
		try:
			str = str.encode("utf-8")
		except:
			pass
	return str

def UpdateFavouritesFromRemote():
	remoteFavouritesType = Addon.getSetting("remoteFavouritesType")
	if remoteFavouritesType == "1" or remoteFavouritesType == "2":
		if remoteFavouritesType == "1":
			try:
				req = urllib2.Request(Addon.getSetting("remoteFavouritesUrl"))
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
				responseData = urllib2.urlopen(req).read().replace('\r','')
				remoteFavouritesList = json.loads(responseData)
			except Exception as ex:
				xbmc.log("{0}".format(ex), 3)
				remoteFavouritesList = []
		elif remoteFavouritesType == "2":
			remoteFavouritesList = ReadList(Addon.getSetting("remoteFavouritesFile"))
			
		favoritesList = ReadList(favoritesFile)
		if remoteFavouritesList != [] and cmp(favoritesList, remoteFavouritesList) != 0:
			WriteList(favoritesFile, remoteFavouritesList)
			return True
	return False
	
def SearchByID(item, id):
	if item["id"] == id: 
		return item
	else:
		if item["type"] == "playlist":
			for item1 in item["list"]:
				item2 = SearchByID(item1, id)
				if item2 is not None:
					return item2
	return None
	
def FindByID(chanList, id):
	item1 = None
	for item in chanList:
		item1 = SearchByID(item, id)
		if item1 is not None:
			break
	return item1

def GetChannelByID(chID):
	chList = ReadList(listsFile)
	channel = FindByID(chList, chID)
	return channel

def GetChannels(categoryID):
	if categoryID == "Favourites":
		retList = ReadList(favoritesFile)
	elif categoryID == 'categories' or categoryID == 'selectedCategories':
		retList = ReadList(os.path.join(listsDir, "{0}.list".format(categoryID)))
	else:
		retList = ReadList(listsFile)
		if categoryID is not None and categoryID != '9999':
			listItem = FindByID(retList, categoryID)
			retList = [] if listItem is None or listItem["type"] != "playlist" else listItem["list"]
	return retList

global_catList = []
global_fullChList = []
def MakeFullLists(current_list):
	for item in current_list:
		if item["type"] == "playlist":
			global_catList.append({"image": item["image"], "group": item["group"], "name": item["name"], "id": item["id"]})
			MakeFullLists(item["list"])
		else:
			global_fullChList.append(item)

def GetChannelsFlat(categoryID):
	catList = GetChannels(categoryID)
	MakeFullLists(catList)
	return global_fullChList
		
def UpdateChList(remoteSettings=None, refreshInterval=0, forceUpdate=True):
	if remoteSettings is None:
		remoteSettings = ReadList(remoteSettingsFile)
	if remoteSettings == []:
		return False
	isListUpdated = False
	if UpdateFavouritesFromRemote():
		isListUpdated = True
	if isFileOld(listsFile, refreshInterval):
		isListUpdated = True
	lastModifiedFile = os.path.join(user_dataDir, "listsLastModified.txt")
	if not os.path.isfile(lastModifiedFile):
		old_modified = "0"
	else:
		with open(lastModifiedFile, 'r') as f:
			old_modified = f.read()
	new_modified = GetSubKeyValue(remoteSettings, "lists", "lastModified")
	if not (forceUpdate or new_modified is None or (old_modified < new_modified)):
		return False
	if new_modified is not None:
		data = GetSubKeyValue(remoteSettings, "lists", "content")
		with open(listsFile, 'w') as f:
			f.write(base64.b64decode(data))
		with open(lastModifiedFile, 'w') as f:
			f.write(new_modified)
	if isListUpdated:
		fullList = ReadList(listsFile)
		MakeFullLists(fullList)
		WriteList(os.path.join(listsDir, "categories.list"), global_catList)
		
		selectedCatList = ReadList(os.path.join(listsDir, "selectedCategories.list"))
		for index, cat in enumerate(selectedCatList):
			if any(f["id"] == cat.get("id", "") for f in global_catList):
				categoty = [f for f in global_catList if f["id"] == cat.get("id", "")]
				selectedCatList[index] = categoty[0]
			else:
				selectedCatList[index]["type"] = "ignore"
		WriteList(os.path.join(listsDir, "selectedCategories.list"), selectedCatList)
		
		favsList = ReadList(favoritesFile)
		for index, favourite in enumerate(favsList):
			if any(f["id"] == favourite.get("id", "") for f in global_fullChList):
				channel = [f for f in global_fullChList if f["id"] == favourite.get("id", "")]
				favsList[index] = {"url": channel[0]["url"], "image": channel[0]["image"], "name": channel[0]["name"], "type": channel[0]["type"], "group": channel[0]["group"], "id": channel[0]["id"]}
			else:
				if favsList[index].has_key("id"):
					favsList[index]["type"] = "ignore"
		WriteList(favoritesFile, favsList)
	return isListUpdated

def OKmsg(title, line1, line2="", line3=""):
	dlg = xbmcgui.Dialog()
	dlg.ok(title, line1, line2, line3)
	
def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text = "" if not keyboard.isConfirmed() else keyboard.getText()
	return text
	
def YesNoDialog(title, line1, line2="", line3="", nolabel="No", yeslabel="Yes"):
	dialog = xbmcgui.Dialog()
	ok = dialog.yesno(title, line1=line1, line2=line2, line3=line3, nolabel=nolabel, yeslabel=yeslabel)
	return ok
	
def GetMenuSelected(title, list, autoclose=0):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, list, autoclose=autoclose)
	return answer

def GetMultiChoiceSelected(title, list):
	dialog = multiChoiceDialog.MultiChoiceDialog(title, list)
	dialog.doModal()
	selected = dialog.selected[:]
	del dialog #You need to delete your instance when it is no longer needed because underlying xbmcgui classes are not grabage-collected. 
	return selected
	
def GetLogoFileName(item):
	if item.has_key('image') and item['image'] is not None and item['image'] != "":
		ext = item['image'][item['image'].rfind('.')+1:]
		i = ext.rfind('?')
		if i > 0: 
			ext = ext[:i]
		if len(ext) > 4:
			ext = "png"
		tvg_logo = hashlib.md5(item['image'].strip()).hexdigest()
		logoFile = "{0}.{1}".format(tvg_logo, ext)
	else:
		logoFile = ""
		
	return logoFile

def Decode(string, key=None):
	if key is None:
		key = GetKey()
	decoded_chars = []
	string = base64.urlsafe_b64decode(string.encode("utf-8"))
	for i in xrange(len(string)):
		key_c = key[i % len(key)]
		decoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
		decoded_chars.append(decoded_c)
	decoded_string = "".join(decoded_chars)
	return decoded_string
	
def GetKey():
	return AddonName
	
def GetAddonDefaultRemoteSettingsUrl():
	remoteSettingsUrl = ""
	try:
		with open(os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'settings.xml'), 'r') as f:
			data = f.read()
		matches = re.compile('setting id="remoteSettingsUrl".+?default="(.+?)"',re.I+re.M+re.U+re.S).findall(data)
		remoteSettingsUrl = matches[0]
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
	return remoteSettingsUrl
	
def GetRemoteSettings():
	remoteSettingsUrl = Addon.getSetting("remoteSettingsUrl")
	if Addon.getSetting("forceRemoteDefaults") == "true":
		defaultRemoteSettingsUrl = GetAddonDefaultRemoteSettingsUrl()
		if (defaultRemoteSettingsUrl != "") and (defaultRemoteSettingsUrl != remoteSettingsUrl):
			remoteSettingsUrl = defaultRemoteSettingsUrl
			Addon.setSetting("remoteSettingsUrl", remoteSettingsUrl)
	remoteSettings = ReadList(remoteSettingsFile)
	urls = GetSubKeyValue(remoteSettings, "remoteSettingsZip", "urls")
	if urls is None or len(urls) == 0:
		try:
			os.unlink(remoteSettingsFile)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)
		remoteSettings = {"remoteSettingsZip": {"urls": remoteSettingsUrl.split(","), "lastModified": "0", "refresh": 12}}
	return remoteSettings

def MakeCatGuides(categories, epg):
	for category in categories:
		MakeCatGuide(category["id"], epg)
	
def MakeCatGuide(categoryID, epg):
	filename = os.path.join(listsDir, "{0}.guide".format(categoryID))
	channels = GetChannels(categoryID)
	categoryEpg = []
	for channel in channels:
		if channel["type"] == 'video' or channel["type"] == 'audio':
			channelName = channel['name'].encode("utf-8").replace("[COLOR yellow][B]", "").replace("[/B][/COLOR]", "")
			try:
				ch = [x for x in epg if x["channel"].encode('utf-8') == channelName]
				if not any(d.get('channel', '').encode('utf-8') == channelName for d in categoryEpg):
					categoryEpg.append(ch[0])
			except Exception, e:
				pass
	WriteList(filename, categoryEpg, indent=False)
	
def MakeFavouritesGuide(fullGuideFile, epg=None):
	if epg is None:
		epg = ReadList(fullGuideFile)
	MakeCatGuide("Favourites", epg)
			
def GetGuide(categoryID):
	if categoryID == '9999':
		return []
	fileName = os.path.join(listsDir, "{0}.guide".format(categoryID))
	return ReadList(fileName)

def InstallAddon(addonID):
	try:
		req = urllib2.Request('https://github.com/cubicle-vdo/xbmc-israel/raw/master/addons.xml')
		response = urllib2.urlopen(req)
		data = response.read()
		response.close()
		data = re.compile('<addon id="(.+?)".+?version="(.+?)"', re.I+re.M+re.U+re.S).findall(data)
		for i in range(len(data)):
			if data[i][0] == addonID:
				addonVer = data[i][1]
				break
		addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
		url = 'https://github.com/cubicle-vdo/xbmc-israel/raw/master/repo/{0}/{0}-{1}.zip'.format(addonID, addonVer)
		packageFile = os.path.join(addonsDir, 'packages', 'isr.zip')
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		else:
			data = response.read()
		response.close()
		with open(packageFile, 'wb') as f:
			f.write(data)
		xbmc.executebuiltin("XBMC.Extract({0}, {1})".format(packageFile, addonsDir), True)
		try:
			os.remove(packageFile)
		except:
			pass
				
		xbmc.executebuiltin("UpdateLocalAddons")
		xbmc.executebuiltin("UpdateAddonRepos")
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		return False

	return True
	
def CheckNewVersion(remoteSettings):
	resolverVerFile = os.path.join(user_dataDir, "resolverVersion.txt")
	if not os.path.isfile(resolverVerFile):
		resolverVersion = ""
	else:
		with open(resolverVerFile, 'r') as f:
			resolverVersion = f.read()
		
	resolverNewVersion = ""
	try:
		resolverNewVersion = xbmcaddon.Addon(resolverAddonID).getAddonInfo("version")	
	except:
		if InstallAddon(resolverAddonID):
			try:
				resolverNewVersion = xbmcaddon.Addon(resolverAddonID).getAddonInfo("version")	
			except Exception as ex:
				xbmc.log("{0}".format(ex), 3)
				return
		else:
			OKmsg(localizedString(30237).encode('utf-8'), localizedString(30237).encode('utf-8'), localizedString(30238).encode('utf-8'))
			return
			
	isUpdated = False
	if resolverNewVersion > resolverVersion:
		isUpdated = True
		with open(resolverVerFile, 'w') as f:
			f.write(resolverNewVersion)
	
	if CheckNewResolver(remoteSettings):
		isUpdated = True
		
	if isUpdated and getUseIPTV() and Addon.getSetting("dynamicPlayer") != "1":
		OKmsg(localizedString(30235).encode('utf-8'), localizedString(30235).encode('utf-8'), localizedString(30201).encode('utf-8'))

def CheckNewResolver(remoteSettings):
	try:
		newModified = GetSubKeyValue(remoteSettings, "resolver", "lastModified")
		resolverContent = Decode(GetSubKeyValue(remoteSettings, "resolver", "content"))
		resolverDir = xbmc.translatePath(xbmcaddon.Addon(resolverAddonID).getAddonInfo('path')).decode("utf-8")
		resolverFile = os.path.join(resolverDir, 'lib', 'myResolver.py')
		lastModifiedFile = os.path.join(user_dataDir, 'resolverLastModified.txt')
		if not os.path.isfile(lastModifiedFile):
			lastModified = "0"
		else:
			with open(lastModifiedFile, 'r') as f:
				lastModified = f.read()
		if newModified is not None and resolverContent is not None and lastModified < newModified:
			with open(resolverFile, 'w') as f:
				f.write(resolverContent)
			with open(lastModifiedFile, 'w') as f:
				f.write(newModified)
			return True
		return False
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		return False

def GetLivestreamerPort():
	portNum = 65007
	try:
		portNum = int(Addon.getSetting("LiveStreamerPort"))
	except:
		pass
	return portNum
	
def getUseIPTV():
	useIPTV = Addon.getSetting("useIPTV")
	if useIPTV == "":	#if useIPTV not set (first time or reset to default) ask the user his choice
		useIPTVval = YesNoDialog(Addon.getAddonInfo("name"), localizedString(30311).encode('utf-8'), localizedString(30312).encode('utf-8'), localizedString(30313).encode('utf-8'), nolabel=localizedString(30002).encode('utf-8'), yeslabel=localizedString(30001).encode('utf-8'))
		useIPTV = "true" if useIPTVval == 1 else "false"
		Addon.setSetting("useIPTV", useIPTV)
	return useIPTV == "true"
	
def getAutoIPTV():
	autoIPTV = Addon.getSetting("autoIPTV")
	# convert old versions values from int to bool.
	if autoIPTV == "0" or autoIPTV == "2":
		Addon.setSetting("autoIPTV", "true")
		autoIPTV = Addon.getSetting("autoIPTV")
	elif autoIPTV == "1" or autoIPTV == "3":
		Addon.setSetting("autoIPTV", "false")
		autoIPTV = Addon.getSetting("autoIPTV")
	return autoIPTV == "true"

def GetUnColor(name):
	regex = re.compile("(\[/?(?:COLOR|B).*?\])", re.IGNORECASE)
	return regex.sub('', name).strip()