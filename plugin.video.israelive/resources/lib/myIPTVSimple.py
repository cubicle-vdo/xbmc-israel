# -*- coding: utf-8 -*-
import urllib2, sys, re, xbmcgui, xbmcaddon, xbmc, os, json, random
import xml.etree.ElementTree as ET
import common, myFilmon

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)
icon = Addon.getAddonInfo('icon')

addon_data_dir = os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)

def GetIptvAddon():
	iptvAddon = None
	
	if os.path.exists(xbmc.translatePath("special://home/addons/").decode("utf-8") + 'pvr.iptvsimple') or os.path.exists(xbmc.translatePath("special://xbmc/addons/").decode("utf-8") + 'pvr.iptvsimple'):
		try:
			iptvAddon = xbmcaddon.Addon("pvr.iptvsimple")
		except:
			print "---- IsraeLive ----\nIPTVSimple addon is disable."
			msg1 = "PVR IPTVSimple is Disable."
			msg2 = "Please enable IPTVSimple addon."
	else:	
		import platform
		osType = platform.system()
		osVer = platform.release()
		xbmcVer = xbmc.getInfoLabel( "System.BuildVersion" )[:2]
		print "---- IsraeLive ----\nosType: {0}\nosVer: {1}\nxbmcVer: {2}".format(osType, osVer, xbmcVer)
		msg1 = "PVR IPTVSimple is NOT installed on your machine."
		msg2 = "Please install XBMC version that include IPTVSimple in it."
	
	if iptvAddon == None:
		common.OKmsg("IsraeLIVE", msg1, msg2)
		
	return iptvAddon

def isIPChange():
	newIP = json.load(urllib2.urlopen('http://httpbin.org/ip'))['origin'] # get current IP
	#sourceSettings['myIP'] = urllib2.urlopen('http://ip.42.pl/raw').read()
	oldIPfile = os.path.join(addon_data_dir, 'myPublicIP.txt')
	
	if os.path.isfile(oldIPfile): # compare with previous IP (if exist)
		f = open(oldIPfile,'r')
		oldIP = f.read()
		f.close()
	else:
		oldIP = ''
	
	isIPChanged = newIP != oldIP # check if IP changed
	
	if isIPChanged: 
		f = open(oldIPfile, 'w')
		f.write(newIP)
		f.close()
	
	return isIPChanged
	
def isMarkedListsChange():
	markedListsFilename = os.path.join(addon_data_dir, "lists", "markedLists.txt") 
	oldList = common.ReadList(markedListsFilename)
	newList = common.GetMarkedLists()
	#oldList = [x.encode('UTF8') for x in oldList]
	return cmp(oldList, newList) != 0

def RefreshIPTVlinks():
	iptvAddon = GetIptvAddon()
	if iptvAddon == None:
		return False

	xbmc.executebuiltin("XBMC.Notification(ISRALIVE, Updating links..., {0}, {1})".format(300000 ,icon))

	markedLists = common.GetMarkedLists()
	markedListsFilename = os.path.join(addon_data_dir, "lists", "markedLists.txt") 
	
	with open(markedListsFilename, 'w') as outfile:
		json.dump(markedLists, outfile) 
	outfile.close()
	
	isIptvAddonGotham = iptvAddon.getAddonInfo('version')  >= "1.9.3"
	finalList = MakeFinalList(markedLists)
	finalM3Ulist = MakeM3U(finalList, isIptvAddonGotham)
	
	if Addon.getSetting("useM3uPath") == "true":
		try:
			f = open(Addon.getSetting("m3uPath"),'r')
			lines = f.readlines()
			f.close()
			
			for line in lines:
				if line.upper().find('#EXTM3U') == -1:
					finalM3Ulist += "{0}".format(line)
				else:
					finalM3Ulist += "\n"
		except:
			pass
			
	if Addon.getSetting("useM3uUrl") == "true":	
		try:
			f = open(Addon.getSetting("m3uPath"),'r')
			lines = common.OpenURL(Addon.getSetting("m3uUrl")).replace('\r','').split('\n')

			for line in lines:
				if line.upper().find('#EXTM3U') == -1:
					finalM3Ulist += "{0}\n".format(line)
		except:
			pass
			
	finalM3Ufilename = os.path.join(addon_data_dir, 'iptv.m3u') # The final m3u file. (static + filmon links)
	f = open(finalM3Ufilename, 'w') # make the finnal m3u list (this file will used in IPTVSimple)
	f.write(finalM3Ulist)
	f.close()

	if os.path.exists(os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), "pvr.iptvsimple")):
		DeleteCache()
		
	UpdateIPTVSimpleSettings(iptvAddon)
	xbmc.executebuiltin("XBMC.Notification(ISRALIVE, Update links is done., {0}, {1})".format(2000 ,icon))
	return True

def UpdateIPTVSimpleSettings(iptvAddon = None):
	if iptvAddon == None:
		iptvAddon = GetIptvAddon()
		if iptvAddon == None:
			return 
			
			
	iptvSettingsFile = os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), "pvr.iptvsimple", "settings.xml")
	if not os.path.isfile(iptvSettingsFile):
		iptvAddon.setSetting("epgPathType", "1") # make 'settings.xml' in 'userdata/addon_data/pvr.iptvsimple' folder
	
	# get settings.xml into dictionary
	dict = ReadSettings(iptvSettingsFile, True)
		
	isSettingsChanged = False
	# make changes
	if dict.has_key("epgPathType") and dict["epgPathType"] != "0":
		dict["epgPathType"] = "0"
		isSettingsChanged = True
	if dict.has_key("epgPath") and dict["epgPath"] != os.path.join(addon_data_dir, 'guide.xml'):
		dict["epgPath"] = os.path.join(addon_data_dir, 'guide.xml')
		isSettingsChanged = True
	#if dict.has_key("epgUrl") and dict["epgUrl"] != "http://thewiz.info/XBMC/_STATIC/guide.xml":
	#	dict["epgUrl"] = "http://thewiz.info/XBMC/_STATIC/guide.xml"
	#	isSettingsChanged = True
	if dict.has_key("logoPathType") and dict["logoPathType"] != "0":
		dict["logoPathType"] = "0"
		isSettingsChanged = True
	if dict.has_key("logoPath") and dict["logoPath"] != os.path.join(addon_data_dir, 'logos'):
		dict["logoPath"] = os.path.join(addon_data_dir, 'logos')
		isSettingsChanged = True
	if dict.has_key("m3uPathType") and dict["m3uPathType"] != "0":
		dict["m3uPathType"] = "0"
		isSettingsChanged = True
	if dict.has_key("m3uPath") and dict["m3uPath"] != os.path.join(addon_data_dir, 'iptv.m3u'):
		dict["m3uPath"] = os.path.join(addon_data_dir, 'iptv.m3u')
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

def MakeFinalList(markedLists):	
	fullList = []
	for name in markedLists:
		list = common.ReadChannelsList(name, forceUpdate=True)
		fullList += list

	return fullList
	
def MakeM3U(list, isIptvAddonGotham):
	randList =  [{ "index": list.index(item), "channel": item} for item in list]
	random.seed()
	random.shuffle(randList)
	headers = None
	for item in randList:
		if item["channel"]["type"] == "filmon":
			headers, streamUrl = myFilmon.GetStreamUrl(int(item["channel"]["url"]), headers)
			if headers:
				list[item["index"]]["url"] = streamUrl
			continue

	M3Ulist = "#EXTM3U\n"
	for item in list:
		tvg_name = item['tvg_id'].replace(' ','_')
		tvg_logo = item['logo']
		if isIptvAddonGotham:
			tvg_logo += ".png"
		radio = ' radio="true"' if item['type'].lower() == "audio" else ''
		M3Ulist += '\n#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" group-title="{2}" tvg-logo="{3}"{4},{5}\n{6}\n'.format(item['tvg_id'], tvg_name, item['group_title'].encode("utf-8"), tvg_logo, radio, item['display_name'].encode("utf-8"), item['url'].encode("utf-8"))
	return M3Ulist
		
def RefreshEPG():
	epgLastETag = os.path.join(addon_data_dir, 'epgLastETag.txt')
	if os.path.isfile(epgLastETag):
		f = open(epgLastETag,'r')
		fileContent = f.read()
		f.close()
	else:
		fileContent = ""
		
	URL = "http://thewiz.info/XBMC/_STATIC/guide.xml"
	req = urllib2.Request(URL)
	url_handle = urllib2.urlopen(req)
	headers = url_handle.info()
	etag = headers.getheader("ETag")
	#last_modified = headers.getheader("Last-Modified") 
	
	isNewEPG = fileContent != etag
	if isNewEPG:
		f = open(epgLastETag, 'w')
		f.write(etag)
		f.close()
		
		try:
			urlContent = common.OpenURL(URL).replace('\r','')
		
			epgFile = os.path.join(addon_data_dir, 'guide.xml')
			f = open(epgFile, 'w')
			f.write(urlContent)
			f.close()
		except:
			print "Can't update guide."
	
	UpdateIPTVSimpleSettings()
	return isNewEPG

def UpdateLogos():
	markedLists = common.GetMarkedLists()
	finalList = MakeFinalList(markedLists)
	common.updateLogos(finalList)

def DeleteCache():
	mypath=os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), "pvr.iptvsimple")
	for f in os.listdir(mypath):
		if os.path.isfile(os.path.join(mypath,f)):
			if f.endswith('cache'):
				os.remove(os.path.join(mypath,f))

def ReadSettings(source, fromFile=False):
	tree = ET.parse(source) if fromFile else ET.fromstring(source)
	elements = tree.findall('*')

	dict = {}
	for elem in elements:
		dict[elem.get('id')] = elem.get('value')
	
	return dict
	
def getM3uFileLastUpdate():
	m3uFile = os.path.join(addon_data_dir, 'iptv.m3u')
	lastUpdate = 0 if not os.path.isfile(m3uFile) else int(os.path.getmtime(m3uFile))
	return lastUpdate
