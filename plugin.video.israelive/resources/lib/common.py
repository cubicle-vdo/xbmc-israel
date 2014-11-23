# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcgui,xbmc,os,time,json,xbmcaddon,io,base64

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
listsDir = os.path.join(user_dataDir, 'lists')

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
	isM3uFileNotUpdate = True if (now - lastUpdate) > deltaInSec else False 
	return isM3uFileNotUpdate
	
def UpdateFile(file, url, zip=False):
	lastModifiedFile = "{0}LastModified.txt".format(file[:file.rfind('.')])
	if (zip == False and not os.path.isfile(file)) or not os.path.isfile(lastModifiedFile):
		fileContent = ""
	else:
		f = open(lastModifiedFile,'r')
		fileContent = f.read()
		f.close()
	
	last_modified = None
	try:
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		headers = response.info()
		etag = headers.getheader("ETag")
		last_modified = headers.getheader("Last-Modified")
		if not last_modified:
			last_modified = etag
	except:
		return False
		
	if last_modified is None:
		return False
		
	isNew = fileContent != last_modified
	
	if isNew:
		if zip:
			urllib.urlretrieve(url, file)
		else:
			try:
				data = response.read().replace('\r','')
			except:
				return False
			
			f = open(file, 'w')
			f.write(data)
			f.close()
		
		f = open(lastModifiedFile, 'w')
		f.write(last_modified)
		f.close()
		
	response.close()
	return isNew
	
def ReadList(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		print ex
		content=[]

	return content

def WriteList(filname, list):
	try:
		with io.open(filname, 'w', encoding='utf-8') as handle:
			handle.write(unicode(json.dumps(list, indent=4, ensure_ascii=False)))
		success = True
	except Exception as ex:
		print ex
		success = False
		
	return success
	
def GetUpdatedList(file, url):
	UpdateFile(file, Decode(url))
	return ReadList(file)
	
def UpdateZipedFile(file, url):
	import extract
	zipFile = "{0}.zip".format(file[:file.rfind('.')])
	if UpdateFile(zipFile, Decode(url), zip=True):
		user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
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
	
def Plx2list(url, name, refreshInterval=0):
	list = []
	isListUpdated = False
	try:
		file = "{0}.plx".format(os.path.join(listsDir, name.replace(" ", "_")))
		if isFileOld(file, refreshInterval):
			isListUpdated = UpdateFile(file, Decode(url))

		f = open(file, 'r')
		data = f.read()
		f.close()

		matches = re.compile('^type(.*?)#$',re.I+re.M+re.U+re.S).findall(data)
		for match in matches:
			item=re.compile('^(.*?)=(.*?)$',re.I+re.M+re.U+re.S).findall("type{0}".format(match))
			item_data = {}
			for field, value in item:
				item_data[field.strip().lower()] = value.strip()
			if item_data["type"] != 'playlist':
				continue

			list.append(item_data)
			
	except Exception as e:
		print e
		pass
		
	return list, isListUpdated

flattenList = []
isFlattenListUpdated = False
def FlatPlxList(list, refreshInterval=0):
	global flattenList
	global isFlattenListUpdated
	for item in list:
		flattenList.append(item)
		list2, isListUpdated = Plx2list(item['url'], item['name'])
		if isListUpdated:
			isFlattenListUpdated = True
		FlatPlxList(list2, refreshInterval=refreshInterval)
	return isFlattenListUpdated

def UpdatePlx(url, name, refreshInterval=0, includeSubPlx=True):
	if not os.path.exists(listsDir):
		os.makedirs(listsDir)
	
	list, isListUpdated = Plx2list(url, name, refreshInterval=refreshInterval)
	if includeSubPlx and FlatPlxList(list, refreshInterval=refreshInterval):
		isListUpdated = True
		
	return isListUpdated
		
def OKmsg(title, line1, line2 = None, line3 = None):
	dlg = xbmcgui.Dialog()
	dlg.ok(title, line1, line2, line3)
	
def GetMenuSelected(title, list):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, list)
	return answer

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
	
def GetAddonDefaults(addon):
	try:
		f = open(os.path.join(addon.getAddonInfo("path").decode("utf-8"), 'resources', 'settings.xml') ,'r')
		data = f.read()
		f.close()
		matches = re.compile('^.*?<setting id="(.*?)".*?default="(.*?)".*?$',re.I+re.M+re.U+re.S).findall(data)
		dict = {}
		for match in matches:
			dict[match[0]] = match[1]
		return dict

	except Exception as ex:
		print ex
	return dict
	
def GetRemoteSettingsUrl():
	remoteSettingsUrl = Addon.getSetting("remoteSettingsUrl")
	if Addon.getSetting("forceRemoteDefaults") == "true":
		defaultRemoteSettingsUrl = GetAddonDefaults(Addon)["remoteSettingsUrl"]
		if defaultRemoteSettingsUrl != remoteSettingsUrl:
			remoteSettingsUrl = defaultRemoteSettingsUrl
			Addon.setSetting("remoteSettingsUrl", remoteSettingsUrl)
	return remoteSettingsUrl