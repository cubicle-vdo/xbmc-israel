# -*- coding: utf-8 -*-
import urllib, re, os, time, datetime
import xbmc, xbmcaddon
import xml.etree.ElementTree as ET
import common

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")

flattenList = []

def plx2channels(file, group=None):
	list = []
	try:
		f = open(file,'r')
		data = f.read()
		f.close()
		
		matches = re.compile('^type(.*?)#$',re.I+re.M+re.U+re.S).findall(data)
		for match in matches:
			item=re.compile('^(.*?)=(.*?)$',re.I+re.M+re.U+re.S).findall("type{0}".format(match))
			item_data = {}
			for field, value in item:
				item_data[field.strip().lower()] = value.strip()
			if not item_data.has_key("type") or (item_data["type"]=='playlist' and item_data['name'].find('Scripts section') >= 0) or item_data['url'] == '' or item_data['url'].find('teled')>=0:
				continue

			if group is not None:
				item_data['group'] = group
			
			list.append(item_data)
			
	except Exception as e:
		print e
		pass
		
	return list

def flatten(listsDir, list):
	global flattenList
	for item in list:
		if item['type'] != 'playlist':
			flattenList.append(item)
		else:
			plxFile = os.path.join(listsDir, "{0}.plx".format(item['name'].replace(" ", "_")))
			if not os.path.isfile(plxFile):
				common.UpdatePlx(item['url'], item['name'], includeSubPlx=False)
			list2 = plx2channels(plxFile, item['name'])
			flatten(listsDir, list2)
	return flattenList
			
def makeIPTVlist(listsDir, mainPlxFile, groupName, iptvFile):
	list = plx2channels(os.path.join(listsDir, mainPlxFile), groupName)
	list = flatten(listsDir, list)

	changeLog = ""
	#M3Ulist = '#EXTM3U\n'
	iptvList = '#EXTM3U\n'

	for item in list:
		url = item['url']
		tvg_id = item['name']
		
		if url.find('plugin.video.israelive') > 0:
			urlParams = url[url.find('?'):]
			url = "http://localhost:88/{0}".format(urlParams)
			tvg_id = "fil-{0}".format(urlParams[5:urlParams.find('&')])
		elif url.find('plugin.video.f4mTester') > 0:
			url = "http://localhost:88/{0}".format(url[url.find('?'):])
		elif url.find('plugin.video.youtube') > 0:
			url = "http://localhost:88/?url=http://youtu.be/{0}".format(url[url.rfind('=') + 1:])
		tvg_name = item['name'].replace(' ','_')
		view_name = item['name']
			
		tvg_logo = tvg_name.replace('_',' ')
		radio = ' radio="true"' if item['type'].lower() == "audio" else ''
		#M3Ulist += '\n#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" group-title="{2}" tvg-logo="{3}"{4},{5}\n{6}\n'.format(tvg_id, tvg_name, item['group'], tvg_logo, radio, view_name, url)
		iptvList += '\n#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" group-title="{2}" tvg-logo="{3}.png"{4},{5}\n{6}\n'.format(tvg_id, tvg_name, item['group'], tvg_logo, radio, view_name, url)

	f = open(iptvFile, 'w')
	f.write("{0}\n".format(iptvList))
	f.close()
	
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
	
def MakeChannelsGuide(guideFile, guideUrl, filmonGuideFile, filmonGuideUrl, xmlFile):
	guideList = common.ReadList(guideFile)
	if len(guideList) == 0:
		common.UpdateZipedFile(guideFile, guideUrl)
		guideList = common.ReadList(guideFile)
	filmonGuideList = common.ReadList(filmonGuideFile)
	if len(filmonGuideList) == 0:
		common.UpdateZipedFile(filmonGuideFile, filmonGuideUrl)
		filmonGuideList = common.ReadList(filmonGuideFile)

	FullGuideList = guideList + filmonGuideList
	if len(FullGuideList) == 0:
		return
		
	tz = GetTZ()
	
	channelsList = ""
	programmeList = ""
	for channel in FullGuideList:
		if type(channel["channel"]) is int:
			chName = "fil-{0}".format(channel["channel"])
		else:
			item = re.compile('^\[COLOR yellow\]\[B\](.*?)\[/B\]\[/COLOR\]$',re.I+re.M+re.U+re.S).findall(channel["channel"].encode("utf-8"))
			chName = item[0] if item != [] else None
		channelsList += "\t<channel id=\"{0}\">\n\t\t<display-name>{0}</display-name>\n\t</channel>\n".format(chName)

		for programme in channel["tvGuide"]:
			start = time.localtime(programme["start"])
			end = time.localtime(programme["end"])
			name = EscapeXML(programme["name"].encode("utf-8")) if programme["name"] != None else ""
			description = EscapeXML(programme["description"].encode("utf-8")) if programme["description"] != None else ""
			programmeList += "\t<programme start=\"{0} {5}\" stop=\"{1} {5}\" channel=\"{2}\">\n\t\t<title>{3}</title>\n\t\t<desc>{4}</desc>\n\t</programme>\n".format(time.strftime("%Y%m%d%H%M%S", start), time.strftime("%Y%m%d%H%M%S", end), chName, name, description, tz)

	xmlList = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<tv>\n{0}{1}</tv>".format(channelsList, programmeList)
	f = open(xmlFile, 'w')
	f.write(xmlList)
	f.close()
	
def SaveChannelsLogos(listsDir, mainPlxFile, groupName, logosDir):
	if not os.path.exists(logosDir):
		os.makedirs(logosDir)
		
	list = plx2channels(os.path.join(listsDir, mainPlxFile), groupName)
	list = flatten(listsDir, list)
	
	for item in flattenList:
		try:
			tvg_logo = item['name'].replace('_',' ')
			if item.has_key('thumb') and item['thumb'] is not None and item['thumb'] != "":
				logoFile = "{0}\\{1}.png".format(logosDir, tvg_logo)
				if not os.path.isfile(logoFile):
					urllib.urlretrieve(item['thumb'], logoFile)
		except Exception as e:
			print e
			pass
			
def GetIptvAddon():
	iptvAddon = None
	
	if os.path.exists(xbmc.translatePath("special://home/addons/").decode("utf-8") + 'pvr.iptvsimple') or os.path.exists(xbmc.translatePath("special://xbmc/addons/").decode("utf-8") + 'pvr.iptvsimple'):
		try:
			iptvAddon = xbmcaddon.Addon("pvr.iptvsimple")
		except:
			print "---- {0} ----\nIPTVSimple addon is disable.".format(AddonName)
			msg1 = "PVR IPTVSimple is Disable."
			msg2 = "Please enable IPTVSimple addon."
	else:	
		import platform
		osType = platform.system()
		osVer = platform.release()
		xbmcVer = xbmc.getInfoLabel( "System.BuildVersion" )[:2]
		print "---- {0} ----\nosType: {1}\nosVer: {2}\nxbmcVer: {3}".format(AddonName, osType, osVer, xbmcVer)
		msg1 = "PVR IPTVSimple is NOT installed on your machine."
		msg2 = "Please install XBMC version that include IPTVSimple in it."
	
	if iptvAddon is None:
		common.OKmsg(AddonName, msg1, msg2)
		
	return iptvAddon
	
def UpdateIPTVSimpleSettings(m3uPath, epgPath, logoPath):
	iptvSettingsFile = os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), "pvr.iptvsimple", "settings.xml")
	if not os.path.isfile(iptvSettingsFile):
		iptvAddon = GetIptvAddon()
		if iptvAddon is None:
			return
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
	
def IsIPTVuseIsraelive(israeliveM3U):
	iptvAddon = GetIptvAddon()
	if iptvAddon is None:
		return False
	return iptvAddon.getSetting("m3uPath") == israeliveM3U and iptvAddon.getSetting("m3uPathType") == "0"