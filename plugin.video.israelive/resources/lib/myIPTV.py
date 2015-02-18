# -*- coding: utf-8 -*-
import urllib, re, os, time, datetime, hashlib
import xbmc, xbmcaddon
import xml.etree.ElementTree as ET
import common, myResolver

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
localizedString = Addon.getLocalizedString

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")

def makeIPTVlist(iptvFile, portNum):
	#satElitKey = None
	iptvList = '#EXTM3U\n'
	
	channelsList = GetIptvChannels()
	for item in channelsList:
		try:
			url = item['url']
			tvg_id = item['name']
			view_name = item['name']
			
			if url.find('plugin.video.israelive') > 0:
				urlParams = url[url.find('?'):]
				url = "http://localhost:{0}/{1}".format(portNum, urlParams)
			elif url.find('plugin.video.f4mTester') > 0:
				url = "http://localhost:{0}/{1}".format(portNum, url[url.find('?'):])
			elif url.find('www.youtube.com') > 0:
				url = "http://localhost:{0}/?url={1}".format(portNum, url)
			elif url.find('?mode=2') > 0 or url.find('?mode=5') > 0 or url.find('?mode=6') > 0:
				url = "http://localhost:{0}/?url={1}".format(portNum, url.replace('?', '&'))
			elif url.find('?mode=3') > 0:
				url = "http://localhost:{0}/?url={1}".format(portNum, url[:url.find('?mode')])
			elif url.find('?mode=4') > 0:
				url = myResolver.GetLivestreamTvFullLink(url[:url.find('?mode')])
				if url == "down":
					view_name += " (down)"
			#elif url.find('?mode=5') > 0:
			#	if satElitKey is None:
			#		satElitKey = myResolver.GetSatElitKeyOnly()
			#	url = myResolver.GetSatElitFullLink(url[:url.find('?mode')], satElitKey)
			elif url.find('?mode=7') > 0:
				url = myResolver.GetAatwFullLink(url[:url.find('?mode')])
				
			tvg_name = item['name'].replace(' ','_')
			tvg_logo = GetLogoFileName(item)
			radio = ' radio="true"' if item['type'].lower() == "audio" else ''
			group = ' group-title="{0}"'.format(item['group']) if item.has_key('group') else ''
			iptvList += '\n#EXTINF:-1 tvg-id="{0}" tvg-name="{1}"{2} tvg-logo="{3}"{4},{5}\n{6}\n'.format(tvg_id, tvg_name, group, tvg_logo, radio, view_name, url)
		except Exception as e:
			print e

	f = open(iptvFile, 'w')
	f.write(iptvList)
	f.close()
	
def GetLogoFileName(item):
	if item.has_key('image') and item['image'] is not None and item['image'] != "":
		ext = item['image'][item['image'].rfind('.')+1:]
		i = ext.rfind('?')
		if i > 0: 
			ext = ext[:ext.rfind('?')]
		if len(ext) > 4:
			ext = "png"
		tvg_logo = hashlib.md5(item['image'].strip()).hexdigest()
		logoFile = "{0}.{1}".format(tvg_logo, ext)
	else:
		logoFile = ""
		
	return logoFile

def EscapeXML(str):
	return str.replace("<", "&lt;").replace(">", "&gt;")
	
def GetTZ():
	ts = time.time()
	delta = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts))
	if delta > datetime.timedelta(0):
		return "+{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
	else:
		delta = -delta
		return "-{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
	
def MakeChannelsGuide(fullGuideFile, iptvGuideFile):
	FullGuideList = GetIptvGuide()
	if len(FullGuideList) == 0:
		return
		
	tz = GetTZ()
	
	channelsList = ""
	programmeList = ""
	for channel in FullGuideList:
		chName = channel["channel"].encode("utf-8")
		channelsList += "\t<channel id=\"{0}\">\n\t\t<display-name>{0}</display-name>\n\t</channel>\n".format(chName)

		for programme in channel["tvGuide"]:
			start = time.localtime(programme["start"])
			end = time.localtime(programme["end"])
			name = EscapeXML(programme["name"].encode("utf-8")) if programme["name"] != None else ""
			description = EscapeXML(programme["description"].encode("utf-8")) if programme["description"] != None else ""
			programmeList += "\t<programme start=\"{0} {5}\" stop=\"{1} {5}\" channel=\"{2}\">\n\t\t<title>{3}</title>\n\t\t<desc>{4}</desc>\n\t</programme>\n".format(time.strftime("%Y%m%d%H%M%S", start), time.strftime("%Y%m%d%H%M%S", end), chName, name, description, tz)

	xmlList = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<tv>\n{0}{1}</tv>".format(channelsList, programmeList)
	f = open(iptvGuideFile, 'w')
	f.write(xmlList)
	f.close()
	
def SaveChannelsLogos(logosDir):
	if not os.path.exists(logosDir):
		os.makedirs(logosDir)
		
	newFilesList = []
	channelsList = GetIptvChannels()
	
	for channel in channelsList:
		try:
			logoFile = GetLogoFileName(channel)
			if logoFile != "":
				newFilesList.append(logoFile)
				logoFile = format(os.path.join(logosDir, logoFile))
				if not os.path.isfile(logoFile):
					#print "---------\n{0}\n{1}".format(channel['name'], channel['image'])
					urllib.urlretrieve(channel['image'], logoFile)
		except Exception as e:
			print e
	
	for the_file in os.listdir(logosDir):
		file_path = os.path.join(logosDir, the_file)
		try:
			if os.path.isfile(file_path) and the_file not in newFilesList:
				os.unlink(file_path)
		except Exception as e:
			print e

def GetIptvAddon():
	iptvAddon = None
	
	if xbmc.getCondVisibility("System.HasAddon(pvr.iptvsimple)"):
		try:
			iptvAddon = xbmcaddon.Addon("pvr.iptvsimple")
		except:
			pass

	if iptvAddon is None:
		import platform
		osType = platform.system()
		osVer = platform.release()
		xbmcVer = xbmc.getInfoLabel( "System.BuildVersion" )[:2]
		print "---- {0} ----\nIPTVSimple addon is disable.".format(AddonName)
		print "---- {0} ----\nosType: {1}\nosVer: {2}\nxbmcVer: {3}".format(AddonName, osType, osVer, xbmcVer)
		msg1 = "PVR IPTV Simple Client is Disable."
		msg2 = "Please enable PVR IPTV Simple Client addon."
		common.OKmsg(AddonName, msg1, msg2)
		
	return iptvAddon
	
def UpdateIPTVSimpleSettings(m3uPath, epgPath, logoPath):
	iptvSettingsFile = os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), "pvr.iptvsimple", "settings.xml")
	if not os.path.isfile(iptvSettingsFile):
		iptvAddon = GetIptvAddon()
		if iptvAddon is None:
			return False
		iptvAddon.setSetting("epgPathType", "0") # make 'settings.xml' in 'userdata/addon_data/pvr.iptvsimple' folder
	
	# get settings.xml into dictionary
	dict = ReadSettings(iptvSettingsFile, fromFile=True)
		
	isSettingsChanged = False
	# make changes
	if dict.has_key("epgPathType") and dict["epgPathType"] != "0":
		dict["epgPathType"] = "0"
		isSettingsChanged = True
	if dict.has_key("epgPath") and dict["epgPath"] != epgPath:
		dict["epgPath"] = epgPath
		isSettingsChanged = True
	if dict.has_key("logoPathType") and dict["logoPathType"] != "0":
		dict["logoPathType"] = "0"
		isSettingsChanged = True
	if dict.has_key("logoPath") and dict["logoPath"] != logoPath:
		dict["logoPath"] = logoPath
		isSettingsChanged = True
	if dict.has_key("m3uPathType") and dict["m3uPathType"] != "0":
		dict["m3uPathType"] = "0"
		isSettingsChanged = True
	if dict.has_key("m3uPath") and dict["m3uPath"] != m3uPath:
		dict["m3uPath"] = m3uPath
		isSettingsChanged = True
		
	if not isSettingsChanged:
		return True
		
	#make new settings.xml (string)
	xml = "<settings>\n"
	for k, v in dict.iteritems():
		xml += '\t<setting id="{0}" value="{1}" />\n'.format(k, v)
	xml += "</settings>\n"
	
	# write updates back to settings.xml
	f = open(iptvSettingsFile, 'w') 
	f.write(xml)
	f.close()
	return True
	
def ReadSettings(source, fromFile=False):
	try:
		tree = ET.parse(source) if fromFile else ET.fromstring(source)
		elements = tree.findall('*')

		dict = {}
		for elem in elements:
			dict[elem.get('id')] = elem.get('value')
	except:
		dict = None

	return dict
		
def RefreshPVR(m3uPath, epgPath, logoPath, autoIPTV=2):
	if autoIPTV == 0:
		Addon.setSetting("autoIPTV", "0")
	else:
		autoIPTV = int(Addon.getSetting("autoIPTV"))
		
	if autoIPTV == 2 or autoIPTV == 3:
		autoIPTV = common.GetMenuSelected(localizedString(30306).encode('utf-8'), [localizedString(30001).encode('utf-8'), localizedString(30002).encode('utf-8'), localizedString(30003).encode('utf-8'), localizedString(30004).encode('utf-8')])
		if autoIPTV == -1:
			autoIPTV = 3
		else:
			Addon.setSetting("autoIPTV", str(autoIPTV))
	
	if autoIPTV == 0 or autoIPTV == 2:
		UpdateIPTVSimpleSettings(m3uPath, epgPath, logoPath)
		xbmc.executebuiltin('StartPVRManager')
		
def GetCategories():
	iptvList = int(Addon.getSetting("iptvList"))
	if iptvList == 0:
		categories = [{"id": "Favourites"}]
	elif iptvList == 1:
		categories = common.GetChannels('categories')
	elif iptvList == 2:
		categories = common.GetChannels('selectedCategories')
	return categories
		
def GetIptvChannels():
	allCategories = common.GetChannels('categories')
	categories = GetCategories()
	channelsList = []
	for category in categories:
		if category.has_key("type") and category["type"] == "ignore":
			continue
		channels = common.GetChannels(category["id"]) if category["id"] != "Favourites" else common.ReadList(os.path.join(user_dataDir, 'favorites.txt'))
		for channel in channels:
			if channel["type"] == 'video' or channel["type"] == 'audio':
				try:
					channelName = channel['name'].encode("utf-8").replace("[COLOR yellow][B]", "").replace("[/B][/COLOR]", "")
					
					if category["id"] == "Favourites":
						gp = [x["name"] for x in allCategories if x["id"] == channel.get("group", "")]
						groupName = gp[0] if len(gp) > 0 else 'Favourites'
					else:
						groupName = category['name']
							
					data = {'name': channelName, 'url': channel['url'], 'image': channel['image'], 'type': channel['type'], 'group': groupName.encode("utf-8")}
					channelsList.append(data)
				except Exception, e:
					pass
					
	return channelsList
	
def GetIptvGuide():
	categories = GetCategories()
	epg = []
	for category in categories:
		channels = common.GetGuide(category["id"])		
		for channel in channels:
			try:
				if not any(d.get('channel', '').encode('utf-8') == channel["channel"].encode("utf-8") for d in epg):
					epg.append(channel)
			except Exception, e:
				pass
					
	return epg
