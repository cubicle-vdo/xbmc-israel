# -*- coding: utf-8 -*-
import urllib2, sys, re, xbmcgui, xbmcaddon, xbmc, os, json
import xml.etree.ElementTree as ET
import myFilmon

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)

dire=os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(dire):
	os.makedirs(dire)
__icon__='http://static2.wikia.nocookie.net/__cb20121121053458/spongebob/images/f/f4/Check-icon.png'
__icon2__='https://svn.apache.org/repos/asf/openoffice/symphony/trunk/main/extras/source/gallery/symbols/Sign-QuestionMark02-Red.png'
icon = Addon.getAddonInfo('icon')
	
def GetIptvAddon():
	import platform
	
	if os.path.exists(xbmc.translatePath("special://home/addons/") + 'pvr.iptvsimple') or os.path.exists(xbmc.translatePath("special://xbmc/addons/") + 'pvr.iptvsimple'):
		return xbmcaddon.Addon("pvr.iptvsimple")
		
	osType = platform.system()
	osVer = platform.release()
	xbmcVer = xbmc.getInfoLabel( "System.BuildVersion" )[:2]

	if osType == "Windows":
		if int(xbmcVer) > 12:
			downloader_is("https://dl.dropboxusercontent.com/u/5461675/pvr.iptvsimple.1.9.3.win32.zip", "IPTVSIMPLE version 1.9.3")
		else: # frodo i hope...
			downloader_is("https://dl.dropboxusercontent.com/u/5461675/pvr.iptvsimple.1.6.1.win32.zip", "IPTVSIMPLE version 1.6.1")
		return xbmcaddon.Addon("pvr.iptvsimple")
	else:
		msg1 = "PVR IPTVSimple is NOT installed on your machine."
		msg2 = "Please install XBMC version that include IPTVSimple in it."
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', msg1, msg2)
		return None

def GetSourceSettings():
	iptvAddon = GetIptvAddon()
	if iptvAddon == None:
		return None, None
	
	isIptvAddonGotham = iptvAddon.getAddonInfo('version')  >= "1.9.3"
	
	iptvPackage = Addon.getSetting("iptvPackage")
	
	if iptvPackage == "0":
		settingsUrl = "https://www.dropbox.com/s/tgenfqcajmr9pfg/TVLight.xml?dl=1"
	elif iptvPackage == "1":
		settingsUrl = "https://www.dropbox.com/s/p8emq70ih3au9av/EnglishOptimized.xml?dl=1"
	elif iptvPackage == "2":
		settingsUrl = "https://www.dropbox.com/s/1q184wd148kd03c/ZipTV.xml?dl=1"
	
	settingsString = OPEN_URL(settingsUrl).replace('\r','')
	sourceSettings = ReadSettings(settingsString)

	sourceSettings['staticM3Uurl'] = sourceSettings['staticM3UdefaultGothamUrl'] if isIptvAddonGotham else sourceSettings['staticM3UdefaultUrl'] # Take URL for static-channels by xbmc version from default URLs.
	sourceSettings['logoBaseUrl'] = "https://www.dropbox.com/sh/94r40pxohmi415p/xa7wCOsPPS?dl=1"
	sourceSettings['IPTVepgPathType'] = "1"
	sourceSettings['IPTVepgUrl'] = "https://copy.com/IzBkjGdaPq8w?download=1"
	sourceSettings['IPTVlogoPathType'] = "0"
	sourceSettings['IPTVlogoPath'] = os.path.join(dire, 'Channel Logos')
	sourceSettings['IPTVm3uPathType'] = "0"
	sourceSettings['packageFolder'] =  os.path.join(dire, sourceSettings['packageName'])
	sourceSettings['IPTVm3uPath'] = os.path.join(sourceSettings['packageFolder'], 'myM3U.m3u')
	
	return iptvAddon, sourceSettings

def CheckIPTVupdates():
	iptvAddon, sourceSettings = GetSourceSettings()
	if iptvAddon == None:
		return None
		
	packageFolder = sourceSettings['packageFolder']
	if not os.path.exists(packageFolder):
		os.makedirs(packageFolder)
		
	sourceSettings['localM3ULastUpdateFile'] = os.path.join(packageFolder, 'iptvLastUpdate.txt')
	sourceSettings['localFilmonLastUpdateFile'] = os.path.join(packageFolder, 'iptv2LastUpdate.txt')
	sourceSettings['localIPFile'] = os.path.join(packageFolder, 'myPublicIP.txt') # stored IP in file for compare on next run (if IP chaneged, there is need to refresh filmon's channels). 
	
	sourceSettings['isForceReScan'] = Addon.getSetting('ForceReScan').lower() == 'true'
	if sourceSettings['isForceReScan']: # make user to check force scan manualy (scan won't run automaticaly every time).
		Addon.setSetting('ForceReScan', 'false')
		
	sourceSettings['M3ULastUpdate'] = OPEN_URL(sourceSettings['staticM3UlastUpdateUrl']) # get static channels' last update from server.
	
	if sourceSettings['isForceReScan'] or not os.path.isfile(sourceSettings['localM3ULastUpdateFile']): # compare last update against local file (if exist)
		f = open(sourceSettings['localM3ULastUpdateFile'],'w')
		f.write(sourceSettings['M3ULastUpdate'])
		fileContent = ''
		f.close()
	else:
		f = open(sourceSettings['localM3ULastUpdateFile'],'r')
		fileContent = f.read()
		f.close()
	
	sourceSettings['isNewM3U'] = sourceSettings['M3ULastUpdate'] != fileContent # check if static channels changed
	
	m3uVer = sourceSettings['M3ULastUpdate'] if sourceSettings['isNewM3U'] else fileContent

	sourceSettings['myIP'] = json.load(urllib2.urlopen('http://httpbin.org/ip'))['origin'] # get current IP
	#sourceSettings['myIP'] = urllib2.urlopen('http://ip.42.pl/raw').read()

	if not os.path.isfile(sourceSettings['localIPFile']): # compare with previous IP (if exist)
		f = open(sourceSettings['localIPFile'],'w')
		f.write(sourceSettings['myIP'])
		fileContent = ''
		f.close()
	else:
		f = open(sourceSettings['localIPFile'],'r')
		fileContent = f.read()
		f.close()
	
	sourceSettings['isNewIP'] = sourceSettings['myIP'] != fileContent # check if IP changed
	sourceSettings['FilmonLastUpdate'] = OPEN_URL(sourceSettings['FilmonLastUpdateURL']) # get filmon channels' last update from server.
	
	if sourceSettings['isForceReScan'] or not os.path.isfile(sourceSettings['localFilmonLastUpdateFile']): # compare last update against local file (if exist)
		f = open(sourceSettings['localFilmonLastUpdateFile'],'w')
		f.write(sourceSettings['FilmonLastUpdate'])
		fileContent = ''
		f.close()
	else:
		f = open(sourceSettings['localFilmonLastUpdateFile'],'r')
		fileContent = f.read()
		f.close()
	
	sourceSettings['isFilmonUpdate'] = sourceSettings['FilmonLastUpdate'] != fileContent or sourceSettings['isNewIP'] # check if filmon channels changed
	filmonVer = sourceSettings['FilmonLastUpdate'] if sourceSettings['isFilmonUpdate'] else fileContent
	sourceSettings['maxVer'] = m3uVer if m3uVer > filmonVer else filmonVer
	sourceSettings['iptvAddon'] = iptvAddon
	
	UpdateIPTVSimpleSettings(iptvAddon, sourceSettings) # check and update iptv-simple settings if nesessery
	
	return sourceSettings
	
def RefreshIPTVlinks(sourceSettings):
	iptvAddon = sourceSettings['iptvAddon']
	packageFolder = sourceSettings['packageFolder']
	
	localOldM3Ufile = os.path.join(packageFolder, 'iptv.m3u')
	localFilmonM3Ufile = os.path.join(packageFolder, 'iptv2.m3u') # store filmon's links.
	finalM3Ufilename = os.path.join(packageFolder, 'myM3U.m3u') # The final m3u file. (static + filmon links)
	errorLogFile = os.path.join(packageFolder, 'iptvErr.log') # log errors.

	xbmc.executebuiltin("XBMC.Notification(ISRALIVE, Updating links..., {1}, {2})".format('', 5000 ,icon))

	if sourceSettings['isNewM3U'] or not os.path.isfile(localOldM3Ufile): # if static channels updated or local file is missing
		OldM3U = OPEN_URL(sourceSettings['staticM3Uurl']).replace('\r','')
			
		f = open(localOldM3Ufile,'w')
		f.write(OldM3U)
		f.close()
		f = open(sourceSettings['localM3ULastUpdateFile'],'w')
		f.write(sourceSettings['M3ULastUpdate'])
		f.close()
	else:	# use local static list
		f = open(localOldM3Ufile,'r')
		OldM3U = f.read()
		f.close()
		
	if sourceSettings['isFilmonUpdate'] or not os.path.isfile(localFilmonM3Ufile): # if IP cahnged or filmon channels updated or local file is missing
		fileContent = OPEN_URL(sourceSettings['FilmonChannelsURL']) # load filmon channels to be scan into a list
		channels = json.loads(fileContent)

		isIptvAddonGotham = iptvAddon.getAddonInfo('version')  >= "1.9.3"
		
		M3Ulist, errorLog = myFilmon.MakeM3ULinks(channels, isIptvAddonGotham) # make m3u-links for filmon channels
		
		if M3Ulist == None: # if there is critical error (couldn't load any file) or canceled by user.
			f = open(errorLogFile, 'w')
			f.write(errorLog)
			f.close()
			print errorLog
			dlg = xbmcgui.Dialog()
			dlg.ok('ISRAELIVE', 'Cannot create links.', "See iptvErr.log")
			return
		
		f = open(localFilmonM3Ufile,'w') # store local m3u for filmon channels
		f.write(M3Ulist)
		f.close()
		
		if sourceSettings['isNewIP']:
			f = open(sourceSettings['localIPFile'],'w') # store current IP
			f.write(sourceSettings['myIP'])
			f.close()
		
		f = open(sourceSettings['localFilmonLastUpdateFile'],'w') # store last update of filmon's m3u file
		f.write(sourceSettings['FilmonLastUpdate'])
		f.close()
	else: # use local filmon list
		f = open(localFilmonM3Ufile,'r')
		M3Ulist = f.read()
		f.close()
		errorLog = ''
	
	maxVer = sourceSettings['maxVer']
	iptvVer = "{0}.{1}.{2} - {3}:{4}".format(maxVer[6:8], maxVer[4:6], maxVer[2:4], maxVer[8:10], maxVer[10:12])
	
	f = open(finalM3Ufilename, 'w') # make the finnal m3u list (this file will used in IPTVSimple)
	finalList = MakeFinalM3UList(OldM3U, M3Ulist)
	finalM3Ulist = '#EXTM3U\n\n#EXTINF:-1 tvg-id="IPTVVersion" tvg-name="IPTVVersion",LiveTV V.{0}\nhttp://udp\n'.format(iptvVer)
	for item in finalList:
		finalM3Ulist += "\n{0}\n".format(item["link"])
	f.write(finalM3Ulist)
	f.close()

	f = open(errorLogFile, 'w') # write the error log
	f.write(errorLog)
	f.close()

	if errorLog != '':
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'Links updated.', "Please restart XBMC.", "Some links didn't created - see iptvErr.log")
	else:
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'Links updated.', "Please restart XBMC.")
	if os.path.exists(xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple")):
		DeleteCache()

def MakeFinalM3UList(staticM3U, filmonM3U):
	list = []
	
	matches=re.compile('#([0-9]+)#\n(.*?)\n\n',re.I+re.M+re.U+re.S).findall(staticM3U)
	for index, link in matches:
		item_data = {'index': int(index), 'link': link}
		list.append(item_data)
	
	matches=re.compile('#([0-9]+)#\n(.*?)\n\n',re.I+re.M+re.U+re.S).findall(filmonM3U)
	for index, link in matches:
		item_data = {'index': int(index), 'link': link}
		list.append(item_data)
		
	return sorted(list, key=lambda k: k['index'])
	
def UpdateIPTVSimpleSettings(iptvAddon, sourceSettings):
	iptvSettingsFile = os.path.join(xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple" ).decode("utf-8"), "settings.xml")
	if not os.path.isfile(iptvSettingsFile):
		iptvAddon.setSetting("m3uPath", sourceSettings['IPTVm3uPath']) # make 'settings.xml' in 'userdata/addon_data/pvr.iptvsimple' folder
	
	# get settings.xml into dictionary
	dict = ReadSettings(iptvSettingsFile, True)
		
	isSettingsChanged = False
	# make changes
	if dict["epgPathType"] != sourceSettings["IPTVepgPathType"]:
		dict["epgPathType"] = sourceSettings["IPTVepgPathType"]
		isSettingsChanged = True
	if dict["epgUrl"] != sourceSettings["IPTVepgUrl"]:
		dict["epgUrl"] = sourceSettings["IPTVepgUrl"]
		isSettingsChanged = True
	if dict["logoPathType"] != sourceSettings["IPTVlogoPathType"]:
		dict["logoPathType"] = sourceSettings["IPTVlogoPathType"]
		isSettingsChanged = True
	if dict["logoPath"] != sourceSettings["IPTVlogoPath"]:
		dict["logoPath"] = sourceSettings["IPTVlogoPath"]
		isSettingsChanged = True
	if dict["m3uPathType"] != sourceSettings['IPTVm3uPathType']:
		dict["m3uPathType"] = sourceSettings['IPTVm3uPathType']
		isSettingsChanged = True
	if dict["m3uPath"] != sourceSettings['IPTVm3uPath']:
		dict["m3uPath"] = sourceSettings['IPTVm3uPath']
		isSettingsChanged = True
		
	if not isSettingsChanged:
		return
		
	#make new settings.xml (string)
	xml = "<settings>\n"
	for k, v in dict.iteritems():
		xml += '\t<setting id="{0}" value="{1}" />\n'.format(k, v)
	xml += "</settings>\n"
	
	# write updates back to settings.xml
	f = open(iptvSettingsFile, 'w') 
	f.write(xml)
	f.close()

'''
def UpdateIPTVSimple():
	iptvAddon, sourceSettings = GetSourceSettings()
	if iptvAddon == None:
		return
	
	UpdateIPTVSimpleSettings(iptvAddon, sourceSettings)
	
	dlg = xbmcgui.Dialog()
	dlg.ok('ISRAELIVE', 'IPTV-Simple updated.', "Please restart XBMC.")
'''
			
def DownloadLogosFolder():
	import downloader,extract
	
	iptvAddon, sourceSettings = GetSourceSettings()
	if iptvAddon == None:
		return
		
	logosUrl = sourceSettings["logoBaseUrl"] # Base URL for logos of channels
	logoPath = sourceSettings["IPTVlogoPath"]
	zipFile = os.path.join(sourceSettings["packageFolder"], 'logos.zip')

	dp = xbmcgui.DialogProgress()
	dp.create("ISRAELIVE", "Logo Icons Downloading...", '', 'Please Wait')
	
	if not os.path.exists(sourceSettings["packageFolder"]):
		os.makedirs(sourceSettings["packageFolder"])
	
	try: os.remove(zipFile)
	except:	pass
	
	downloader.download(logosUrl, zipFile, dp)
	
	if not os.path.exists(logoPath):
		os.makedirs(logoPath)
	
	dp.update (0, "", "Extracting Zip Please Wait")
	extract.all(zipFile ,logoPath, dp)
	
	try: os.remove(zipFile)
	except:	pass

	UpdateIPTVSimpleSettings(iptvAddon, sourceSettings) # check and update iptv-simple settings if nesessery
		
	dlg = xbmcgui.Dialog()
	dlg.ok('ISRAELIVE', 'Logo Pack Download Complete')
	
def DeleteCache():
	mypath=xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple" ).decode("utf-8")
	for f in os.listdir(mypath):
		if os.path.isfile(os.path.join(mypath,f)):
			if f.endswith('cache'):
				os.remove(os.path.join(mypath,f))

def ListFromFavourites(channels):
	iptvAddon, sourceSettings = GetSourceSettings()
	if iptvAddon == None:
		return None
	
	isIptvAddonGotham = iptvAddon.getAddonInfo('version')  >= "1.9.3"
	
	packageFolder = sourceSettings['packageFolder']
	if not os.path.exists(packageFolder):
		os.makedirs(packageFolder)
		
	localOldM3Ufile = os.path.join(packageFolder, 'iptv.m3u')
	localFilmonM3Ufile = os.path.join(packageFolder, 'iptv2.m3u') # store filmon's links.
	localIPFile = os.path.join(packageFolder, 'myPublicIP.txt')
	finalM3Ufilename = os.path.join(packageFolder, 'myM3U.m3u') # The final m3u file. (static + filmon links)
	errorLogFile = os.path.join(packageFolder, 'iptvErr.log') # log errors.
	
	FAV=os.path.join(dire, 'favorites.txt')
	try:
		f = open(FAV,'r')
		fileContent = f.read()
		f.close()
		channels = json.loads(fileContent)
	except:
		channels = []
	
	M3Ulist = '#EXTM3U\n'
	FilmonChannelslist = []
	
	i = 1
	for channel in channels:
		i += 1
        url = channel["url"]
        name = channel["name"]
        radio = ' radio="true"' if (channel.has_key("type") and channel["type"].lower() == "audio") else ''

        if url.lower().find('myfilmon') > 0:
			chNum = int(re.compile("url=(.*?)&mode=1",re.I+re.M+re.U+re.S).findall(url)[0])
			data = {"index" : i, "chNum": chNum, "chName": name, "group": "favourites"}
			FilmonChannelslist.append(data)
        else:
			if isIptvAddonGotham:
				M3Ulist += '\n#{0}#\n#EXTINF:-1 tvg-id="{1}" tvg-name="{2}" group-title="{3}" tvg-logo="{4}.png"{5},{6}\n{7}\n'.format(i, name, name.replace(' ','_'), "favourites", name, radio, name, url)
			else:
				M3Ulist += '\n#{0}#\n#EXTINF:-1 tvg-id="{1}" tvg-name="{2}" group-title="{3}" tvg-logo="{4}"{5},{6}\n{7}\n'.format(i, name, name.replace(' ','_'), "favourites", name, radio, name, url)
		
	UpdateIPTVSimpleSettings(iptvAddon, sourceSettings) # check and update iptv-simple settings if nesessery

	if os.path.isfile(M3Ufilename):
		f = open(M3Ufilename,'r')
		fileContent = f.read()
		f.close()
	else:
		fileContent = ""
		
	isNewM3U = fileContent != M3Ulist # check if static channels changed
		
	if isNewM3U:
		f = open(M3Ufilename, 'w')
		f.write("{0}\n".format(M3Ulist))
		f.close()
		
	myIP = json.load(urllib2.urlopen('http://httpbin.org/ip'))['origin'] # get current IP

	if not os.path.isfile(localIPFile): # compare with previous IP (if exist)
		f = open(localIPFile,'w')
		f.write(myIP)
		fileContent = ''
		f.close()
	else:
		f = open(localIPFile,'r')
		fileContent = f.read()
		f.close()
		
	isNewIP = myIP != fileContent # check if IP changed
	
	if os.path.isfile(FilmonChannelsFilename):
		f = open(FilmonChannelsFilename,'r')
		fileContent = f.read()
		f.close()
		channels = json.loads(fileContent)
	else:
		channels = []
		
	isFilmonUpdate = cmp(channels, FilmonChannelslist) != 0
	if isFilmonUpdate:
		with open(FilmonChannelsFilename, 'w') as outfile:
			json.dump(FilmonChannelslist, outfile) 
		outfile.close()	
		
	isFilmonUpdate = isFilmonUpdate or isNewIP # check if filmon channels changed
	
	#dp = xbmcgui.DialogProgress()
	#dp.create("ISRAELIVE", "")
	#dp.update(0)
	
	#M3Ulist, errorLog = myFilmon.MakeM3ULinks(FilmonChannelslist, dp, isIptvAddonGotham) # make m3u-links for filmon channels
	M3Ulist, errorLog = myFilmon.MakeM3ULinks(FilmonChannelslist, isIptvAddonGotham) # make m3u-links for filmon channels
		
	if M3Ulist == None: # if there is critical error (couldn't load any file) or canceled by user.
		f = open(errorLogFile, 'w')
		f.write(errorLog)
		f.close()
		print errorLog
		#dp.update(100)
		#dp.close() 
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'Cannot create links.', "See iptvErr.log")
		#xbmc.executebuiltin("Notification(ISRALIVE, Cannot create all links - see iptvErr.log, 5000, {0})".format(__icon2__))
		return
	
	f = open(localFilmonM3Ufile,'w') # store local m3u for filmon channels
	f.write(M3Ulist)
	f.close()
	
	if sourceSettings['isNewIP']:
		f = open(localIPFile,'w') # store current IP
		f.write(myIP)
		f.close()
		
	f = open(finalM3Ufilename, 'w') # make the finnal m3u list (this file will used in IPTVSimple)
	finalList = MakeFinalM3UList(OldM3U, M3Ulist)
	finalM3Ulist = '#EXTM3U\n'
	for item in finalList:
		finalM3Ulist += "\n{0}\n".format(item["link"])
	f.write(finalM3Ulist)
	f.close()

	f = open(errorLogFile, 'w') # write the error log
	f.write(errorLog)
	f.close()

	if errorLog != '':
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'Links updated.', "Please restart XBMC.", "Some links didn't created - see iptvErr.log")
		#xbmc.executebuiltin("Notification(ISRALIVE, Cannot create all links - see iptvErr.log, 5000, {0})".format(__icon2__))
	else:
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'Links updated.', "Please restart XBMC.")
		#xbmc.executebuiltin("Notification(ISRALIVE, Links updated - Please reset the PVR database., 5000, {0})".format(__icon__))
	if os.path.exists(xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple")):
		DeleteCache()

def OPEN_URL(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    
	response = urllib2.urlopen(req,timeout=100)
	link=response.read()
	response.close()
	return link
	
def ReadSettings(source, fromFile=False):
	tree = ET.parse(source) if fromFile else ET.fromstring(source)
	elements = tree.findall('*')

	dict = {}
	for elem in elements:
		dict[elem.get('id')] = elem.get('value')
	
	return dict