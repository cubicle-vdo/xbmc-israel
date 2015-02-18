# -*- coding: utf-8 -*-
import sys, os, io, re, time, base64, random
import urllib, urllib2, json
import xbmc, xbmcgui, xbmcaddon
import multiChoiceDialog
import itertools, operator

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
localizedString = Addon.getLocalizedString
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
listsDir = os.path.join(user_dataDir, 'lists')
remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")

def downloader_is(url, name, showProgress=True):
	import downloader, extract

	addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
	packageFile = os.path.join(addonsDir, 'packages', 'isr.zip')

	if showProgress:
		dp = xbmcgui.DialogProgress()
		dp.create(AddonName, "Downloading", name, "Please Wait")
		downloader.download(url, packageFile, dp)
		dp.update(0, "", "Extracting Zip Please Wait")
		extract.all(packageFile, addonsDir, dp)
	else:
		urllib.urlretrieve(url, packageFile)
		extract.all(packageFile, addonsDir)
		
	try:
		os.remove(packageFile)
	except:
		pass
			
	xbmc.executebuiltin("UpdateLocalAddons")
	xbmc.executebuiltin("UpdateAddonRepos")

def isFileOld(file, deltaInSec):
	lastUpdate = 0 if not os.path.isfile(file) else int(os.path.getmtime(file))
	now = int(time.time())
	isFileNotUpdate = True if (now - lastUpdate) > deltaInSec else False 
	return isFileNotUpdate
	
def GetSubKeyValue(remoteSettings, key, subKey):
	return remoteSettings[key][subKey] if (remoteSettings.has_key(key) and remoteSettings[key].has_key(subKey)) else None
	
def UpdateFile(file, key, remoteSettings=None, zip=False, forceUpdate=False):
	if remoteSettings is None:
		remoteSettings = ReadList(os.path.join(user_dataDir, "remoteSettings.txt"))
	
	if remoteSettings == []:
		return False
			
	lastModifiedFile = "{0}LastModified.txt".format(file[:file.rfind('.')])
	if (zip == False and not os.path.isfile(file)) or not os.path.isfile(lastModifiedFile):
		fileContent = ""
	else:
		f = open(lastModifiedFile,'r')
		fileContent = f.read()
		f.close()
	last_modified = GetSubKeyValue(remoteSettings, key, "lastModified")
	isNew = forceUpdate or last_modified is None or (fileContent != last_modified)
	if not isNew:
		return False
	
	urls = GetSubKeyValue(remoteSettings, key, "urls")
	if urls is None or len(urls) == 0:
		return False
		
	random.seed()
	random.shuffle(urls)
	url = Decode(urls[0])
	
	response = None
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
		req.add_header('Referer', 'http://www.IsraeLIVE.org/')
		response = urllib2.urlopen(req)
	
		if zip:
			urllib.urlretrieve(url, file)
		else:
			data = response.read().replace('\r','')
			f = open(file, 'w')
			f.write(data)
			f.close()
		
		response.close()

	except Exception as ex:
		print ex
		if not response is None:
			response.close()
		return False

	if key == "remoteSettings":
		remoteSettings = json.loads(data)
		last_modified = GetSubKeyValue(remoteSettings, key, "lastModified")
		
	f = open(lastModifiedFile, 'w')
	f.write(last_modified)
	f.close()
	
	return True
	
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
	
def GetUpdatedList(file, key, remoteSettings=None, forceUpdate=False):
	UpdateFile(file, key, remoteSettings=remoteSettings, forceUpdate=forceUpdate)
	return ReadList(file)
	
def UpdateZipedFile(file, key, remoteSettings=None, forceUpdate=False):
	import extract
	zipFile = "{0}.zip".format(file[:file.rfind('.')])
	if UpdateFile(zipFile, key, remoteSettings=remoteSettings, zip=True, forceUpdate=forceUpdate):
		extract.all(zipFile, user_dataDir)
		try:
			os.remove(zipFile)
		except:
			pass
		return True
	return False
	
def GetEncodeString(str):
	import chardet
	try:
		str = str.decode(chardet.detect(str)["encoding"]).encode("utf-8")
	except:
		pass
	return str

def UpdatePlx(file, key, remoteSettings=None, refreshInterval=0, forceUpdate=False):
	isListUpdated = False
	if isFileOld(file, refreshInterval):
		isListUpdated = UpdateFile(file, key, remoteSettings=remoteSettings, forceUpdate=forceUpdate)

	if not os.path.exists(listsDir):
		os.makedirs(listsDir)
		isListUpdated = True
			
	if isListUpdated:
		fullList = GetListFromPlx(fullScan=True)
		fullList.sort(key=operator.itemgetter('group'))
		categories_list = []
		for key, group in itertools.groupby(fullList, lambda item: item["group"]):
			list1 = [{"url": item["url"], "image": item["image"], "name": item["name"].decode("utf-8"), "type": item["type"], "group": item["group"].decode("utf-8"), "id": item["id"]} for item in group]
			filename = os.path.join(listsDir, "{0}.list".format(key.strip()))
			WriteList(filename, list1)
			categories = [{"name": item["name"], "image": item["image"], "group": item["group"], "id": item["id"]} for item in list1 if item['type'] == "playlist"]
			if len(categories) > 0:
				for category in categories:
					categories_list.append(category)

		categories_list.sort(key=operator.itemgetter('id'))
		WriteList(os.path.join(listsDir, "categories.list"), categories_list)
		
		selectedCatList = ReadList(os.path.join(listsDir, "selectedCategories.list"))
		for index, cat in enumerate(selectedCatList):
			if any(f["id"] == cat.get("id", "") for f in categories_list):
				categoty = [f for f in categories_list if f["id"] == cat.get("id", "")]
				selectedCatList[index] = categoty[0]
			else:
				selectedCatList[index]["type"] = "ignore"
		WriteList(os.path.join(listsDir, "selectedCategories.list"), selectedCatList)
		
		favsList = ReadList(os.path.join(user_dataDir, 'favorites.txt'))
		for index, favourite in enumerate(favsList):
			if any(f["id"] == favourite.get("id", "") for f in fullList):
				channel = [f for f in fullList if f["id"] == favourite.get("id", "")]
				favsList[index] = {"url": channel[0]["url"], "image": channel[0]["image"], "name": channel[0]["name"].decode("utf-8"), "type": channel[0]["type"], "group": channel[0]["group"].decode("utf-8"), "id": channel[0]["id"]}
			else:
				if favsList[index].has_key("id"):
					favsList[index]["type"] = "ignore"
		WriteList(os.path.join(user_dataDir, 'favorites.txt'), favsList)
		
	return isListUpdated
		
def OKmsg(title, line1, line2="", line3=""):
	dlg = xbmcgui.Dialog()
	dlg.ok(title, line1, line2, line3)
	
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
	
def Encode(string, key=None):
	if key is None:
		key = GetKey()
	encoded_chars = []
	for i in xrange(len(string)):
		key_c = key[i % len(key)]
		encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
		encoded_chars.append(encoded_c)
	encoded_string = "".join(encoded_chars)
	return base64.urlsafe_b64encode(encoded_string)
 
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
		f = open(os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'settings.xml') ,'r')
		data = f.read()
		f.close()
		matches = re.compile('setting id="remoteSettingsUrl".+?default="(.+?)"',re.I+re.M+re.U+re.S).findall(data)
		remoteSettingsUrl = matches[0]
	except Exception as ex:
		print ex
	return remoteSettingsUrl
	
def GetRemoteSettings(updateDefault=False):
	remoteSettingsUrl = Addon.getSetting("remoteSettingsUrl")
	if Addon.getSetting("forceRemoteDefaults") == "true":
		defaultRemoteSettingsUrl = GetAddonDefaultRemoteSettingsUrl()
		if defaultRemoteSettingsUrl != remoteSettingsUrl:
			remoteSettingsUrl = defaultRemoteSettingsUrl
			Addon.setSetting("remoteSettingsUrl", remoteSettingsUrl)
			
	remoteSettings = ReadList(remoteSettingsFile)
	if remoteSettings == []:
		remoteSettings = {}

	urls = GetSubKeyValue(remoteSettings, "remoteSettings", "urls")
	if urls is None or len(urls) == 0:
		remoteSettings = {"remoteSettings": {"urls": [remoteSettingsUrl], "lastModified": "0", "refresh": 12}}
	
	return remoteSettings

def GetListFromPlx(filterCat="9999", includeChannels=True, includeCatNames=True, fullScan=False):
	plxFile = os.path.join(user_dataDir, "israelive.plx")
	f = open(plxFile,'r')
	data = f.read()
	f.close()
	
	matches = re.compile('^type(.+?)#$',re.I+re.M+re.U+re.S).findall(data)
	categories = ["9999"]
	list = []
	for match in matches:
		item=re.compile('^(.*?)=(.*?)$',re.I+re.M+re.U+re.S).findall("type{0}".format(match))
		item_data = {}
		for field, value in item:
			item_data[field.strip().lower()] = value.strip()
		if not item_data.has_key("type"):
			continue
		
		url = item_data['url']
		thumb = "" if not item_data.has_key("thumb") else item_data['thumb']
		channelName = GetEncodeString(item_data['name'])
		
		if item_data["type"] == 'audio' and item_data["url"] == '':
			if channelName.find("-") != 0:
				categories.append(item_data["id"])
				item_data["type"] = "playlist"
				if not includeCatNames:
					continue
			else:
				del categories[-1]
				continue
		elif not includeChannels:
			continue
		
		lenCat = len(categories)
		subCat = categories[lenCat-1] if item_data["type"] != "playlist" else categories[lenCat-2]

		if subCat == filterCat or fullScan:
			list.append({"url": url, "image": thumb, "name": channelName, "type": item_data["type"], "group": subCat, "id": item_data["id"]})
		
	return list
	
def GetChannels(categoryID):
	fileName = os.path.join(listsDir, "{0}.list".format(categoryID))
	return ReadList(fileName)
	
def MergeGuides(globalGuideFile, filmonGuideFile, fullGuideFile):
	guideList = ReadList(globalGuideFile)
	filmonGuideList = ReadList(filmonGuideFile)
	WriteList(fullGuideFile, guideList + filmonGuideList)
	MakeCatGuides(fullGuideFile, os.path.join(listsDir, "categories.list"))
	
def MakeCatGuides(fullGuideFile, categoriesFile):
	if not os.path.exists(listsDir):
		os.makedirs(listsDir)
		
	epg = ReadList(fullGuideFile)
	
	categories = ReadList(categoriesFile)
	categories.append({"id": "Favourites"})

	for category in categories:
		MakeCatGuide(fullGuideFile, category["id"], epg)
	
def MakeCatGuide(fullGuideFile, categoryID, epg=None):
	if epg is None:
		epg = ReadList(fullGuideFile)
		
	filename = os.path.join(listsDir, "{0}.guide".format(categoryID))
	channels = GetChannels(categoryID) if categoryID != "Favourites" else ReadList(os.path.join(user_dataDir, 'favorites.txt'))
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
	WriteList(filename, categoryEpg)
		
def GetGuide(categoryID):
	fileName = os.path.join(listsDir, "{0}.guide".format(categoryID))
	return ReadList(fileName)
	
def CheckNewVersion():
	versionFile = os.path.join(user_dataDir, "addonVersion.txt")
	if not os.path.isfile(versionFile):
		version = ""
	else:
		f = open(versionFile,'r')
		version = f.read()
		f.close()
	
	newVersion = Addon.getAddonInfo("version")
	if newVersion > version:
		if Addon.getSetting("useIPTV") == "true":
			OKmsg("{0}{1}".format(localizedString(30200).encode('utf-8'), newVersion), localizedString(30201).encode('utf-8'))
		f = open(versionFile, 'w')
		f.write(newVersion)
		f.close()
