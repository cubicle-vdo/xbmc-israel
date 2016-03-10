# -*- coding: utf-8 -*-
import urllib, re, os, shutil
import xbmc, xbmcaddon
import xml.etree.ElementTree as ET
import time, datetime
isDateutil = False
try:
	from dateutil import tz
	isDateutil = True
except:
	pass
import common

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
localizedString = Addon.getLocalizedString

try:
	import myResolver
except:
	import sys
	if common.InstallAddon('script.module.israeliveresolver'):
		common.OKmsg(localizedString(30236).encode('utf-8'), localizedString(30201).encode('utf-8'))
	else:
		common.OKmsg(localizedString(30237).encode('utf-8'), localizedString(30238).encode('utf-8'))
	sys.exit()
		
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")

def makeIPTVlist(iptvFile):
	first21 = True
	iptvList = '#EXTM3U\n'
	
	channelsList = GetIptvChannels()
	portNum = common.GetLivestreamerPort()
		
	for item in channelsList:
		try:
			url = item['url']
			tvg_id = item['name']
			view_name = item['name']
			if url.find('plugin.video.f4mTester') > 0:
				url = "http://localhost:{0}/{1}".format(portNum, url[url.find('?'):])
			elif url.find('www.youtube.com') > 0 or url == "BB":
				url = "http://localhost:{0}/?url={1}".format(portNum, url)
			else:
				matches = re.compile('^(.*?)[\?|&]mode=(\-?[0-9]+)(.*?)$', re.I+re.M+re.U+re.S).findall(url)
				if len(matches) > 0:
					url = matches[0][0]
					mode = matches[0][1]
					if len(matches[0]) > 2:
						url += matches[0][2]
					if mode == '1':
						url = "http://localhost:{0}/{1}&mode={2}".format(portNum, url[url.find('?'):], mode)
					elif mode == '3':
						url = "http://localhost:{0}/?url={1}".format(portNum, url)
					elif mode == '-3' or mode == '0' or mode == '7' or mode == '16' or mode == '20' or mode == '21' or mode == '22' or mode == '23' or mode == '24' or mode == '25' or mode == '27':
						if mode == '21':
							if first21:
								first21 = False
							else:
								url += ";s"
						url = myResolver.Resolve(url, mode)
						if url is None or url == "down":
							continue
					elif mode == '10' or mode == '13':
						continue
					else:
						url = "http://localhost:{0}/?url={1}&mode={2}".format(portNum, url.replace('?', '&'), mode)

			tvg_name = item['name'].replace(' ','_')
			tvg_logo = common.GetLogoFileName(item)
			radio = ' radio="true"' if item['type'].lower() == "audio" else ''
			group = ' group-title="{0}"'.format(item['group']) if item.has_key('group') else ''
			iptvList += '\n#EXTINF:-1 tvg-id="{0}" tvg-name="{1}"{2} tvg-logo="{3}"{4},{5}\n{6}\n'.format(tvg_id, tvg_name, group, tvg_logo, radio, view_name, url)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)

	f = open(iptvFile, 'w')
	f.write(iptvList)
	f.close()
	
def EscapeXML(str):
	return str.replace('&', '&amp;').replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")
	
def UnEscapeXML(str):
	return str.replace('&amp;', '&').replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'")
	
def GetTZtime(timestamp):
	timeStr = ""
	if isDateutil:
		from_zone = tz.tzutc()
		to_zone = tz.tzlocal()
		utc = datetime.datetime.utcfromtimestamp(timestamp)
		utc = utc.replace(tzinfo=from_zone)
		local_time = utc.astimezone(to_zone)
		timeStr = local_time.strftime('%Y%m%d%H%M%S %z')
	else:
		ts = time.time()
		delta = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts))
		hrs = "+0000"
		if delta > datetime.timedelta(0):
			hrs = "+{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
		else:
			delta = -delta
			hrs = "-{0:02d}{1:02d}".format(delta.seconds//3600, (delta.seconds//60)%60)
		timeStr = "{0} {1}".format(time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp)), hrs)
	return timeStr
	
def MakeChannelsGuide(fullGuideFile, iptvGuideFile):
	FullGuideList = GetIptvGuide()
	if len(FullGuideList) == 0:
		return

	channelsList = ""
	programmeList = ""
	for channel in FullGuideList:
		chName = channel["channel"].encode("utf-8")
		channelsList += "\t<channel id=\"{0}\">\n\t\t<display-name>{0}</display-name>\n\t</channel>\n".format(chName)
		for programme in channel["tvGuide"]:
			start = GetTZtime(programme["start"])
			end = GetTZtime(programme["end"])
			name = EscapeXML(programme["name"].encode("utf-8")) if programme["name"] != None else ""
			description = EscapeXML(programme["description"].encode("utf-8")) if programme["description"] != None else ""
			programmeList += "\t<programme start=\"{0}\" stop=\"{1}\" channel=\"{2}\">\n\t\t<title>{3}</title>\n\t\t<desc>{4}</desc>\n\t</programme>\n".format(start, end, chName, name, description)
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
			logoFile = common.GetLogoFileName(channel)
			if logoFile != "":
				newFilesList.append(logoFile)
				logoFile = os.path.join(logosDir, logoFile)
				if not os.path.isfile(logoFile):
					logo = channel['image']
					if logo.startswith('http'):
						urllib.urlretrieve(logo, logoFile)
					else:
						shutil.copyfile(logo, logoFile)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)
	
	for the_file in os.listdir(logosDir):
		file_path = os.path.join(logosDir, the_file)
		try:
			if os.path.isfile(file_path) and the_file not in newFilesList:
				os.unlink(file_path)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)

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
		xbmc.log("---- {0} ----\nIPTVSimple addon is disable.".format(AddonName), 2)
		xbmc.log("---- {0} ----\nosType: {1}\nosVer: {2}\nxbmcVer: {3}".format(AddonName, osType, osVer, xbmcVer), 2)
		msg1 = "PVR IPTV Simple Client is Disable."
		msg2 = "Please enable PVR IPTV Simple Client addon."
		common.OKmsg(AddonName, msg1, msg2)
		
	return iptvAddon
	
def UpdateIPTVSimpleSettings(m3uPath, epgPath, logoPath):
	iptvSettingsFile = os.path.join(xbmc.translatePath("special://profile").decode("utf-8"), "addon_data", "pvr.iptvsimple", "settings.xml")
	if not os.path.isfile(iptvSettingsFile):
		iptvAddon = GetIptvAddon()
		if iptvAddon is None:
			return False
		iptvAddon.setSetting("epgPathType", "0") # make 'settings.xml' in 'userdata/addon_data/pvr.iptvsimple' folder
	
	# get settings.xml into dictionary
	dict = ReadSettings(iptvSettingsFile, fromFile=True)
	if dict is None:
		msg1 = "Oops."
		msg2 = "Can't update IPTVSimple settings."
		common.OKmsg(AddonName, msg1, msg2)
		return False
		
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
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		dict = None

	return dict
		
def RefreshPVR(m3uPath, epgPath, logoPath, forceUpdate=False):
	if common.getAutoIPTV() or forceUpdate:
		UpdateIPTVSimpleSettings(m3uPath, epgPath, logoPath)
		if Addon.getSetting("autoPVR") == "true":
			xbmc.executebuiltin('StopPVRManager')
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
