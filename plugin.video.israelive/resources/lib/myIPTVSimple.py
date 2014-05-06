# -*- coding: utf-8 -*-
import urllib2, sys, re, xbmcgui, xbmcaddon, xbmc, os, json
import xml.etree.ElementTree as ET

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)

addon_data_dir=os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)
icon = Addon.getAddonInfo('icon')
	
def GetIptvAddon():
	import platform
	
	if os.path.exists(xbmc.translatePath("special://home/addons/") + 'pvr.iptvsimple') or os.path.exists(xbmc.translatePath("special://xbmc/addons/") + 'pvr.iptvsimple'):
		return xbmcaddon.Addon("pvr.iptvsimple")
	else:	
		osType = platform.system()
		osVer = platform.release()
		xbmcVer = xbmc.getInfoLabel( "System.BuildVersion" )[:2]
		print "---- IsraeLive ----\nosType: {0}\nosVer: {1}\nxbmcVer: {2}".format(osType, osVer, xbmcVer)
		msg1 = "PVR IPTVSimple is NOT installed on your machine."
		msg2 = "Please install XBMC version that include IPTVSimple in it."
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', msg1, msg2)
		return None

def isIPTVChange():
	markedListsFilename = os.path.join(xbmc.translatePath("special://userdata/addon_data"), AddonID, "lists", "markedLists.txt") 
	oldList = ReadList(markedListsFilename)
	newList = GetMarkedLists()
	#oldList = [x.encode('UTF8') for x in oldList]
	return cmp(oldList, newList) != 0

def RefreshIPTVlinks():
	iptvAddon = GetIptvAddon()
	if iptvAddon == None:
		return None

	#xbmc.executebuiltin("XBMC.Notification(ISRALIVE, Updating links..., {1}, {2})".format('', 10000 ,icon))

	markedLists = GetMarkedLists()
	markedListsFilename = os.path.join(xbmc.translatePath("special://userdata/addon_data"), AddonID, "lists", "markedLists.txt") 
	
	with open(markedListsFilename, 'w') as outfile:
		json.dump(markedLists, outfile) 
	outfile.close()
	
	isIptvAddonGotham = iptvAddon.getAddonInfo('version')  >= "1.9.3"
	finalList = MakeFinalList(markedLists)
	finalM3Ulist = MakeM3U(finalList, isIptvAddonGotham)
	finalM3Ufilename = os.path.join(addon_data_dir, 'iptv.m3u') # The final m3u file. (static + filmon links)
	f = open(finalM3Ufilename, 'w') # make the finnal m3u list (this file will used in IPTVSimple)
	f.write(finalM3Ulist)
	f.close()

	dlg = xbmcgui.Dialog()
	dlg.ok('ISRAELIVE', 'Links updated.', "Please restart XBMC or PVR db.")
	
	if os.path.exists(xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple")):
		DeleteCache()
		
	UpdateIPTVSimpleSettings(iptvAddon)

def UpdateIPTVSimpleSettings(iptvAddon):
	iptvSettingsFile = os.path.join(xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple" ).decode("utf-8"), "settings.xml")
	if not os.path.isfile(iptvSettingsFile):
		iptvAddon.setSetting("epgPathType", "1") # make 'settings.xml' in 'userdata/addon_data/pvr.iptvsimple' folder
	
	# get settings.xml into dictionary
	dict = ReadSettings(iptvSettingsFile, True)
		
	isSettingsChanged = False
	# make changes
	if dict.has_key("epgPathType") and dict["epgPathType"] != "1":
		dict["epgPathType"] = "1"
		isSettingsChanged = True
	if dict.has_key("epgUrl") and dict["epgUrl"] != "http://thewiz.info/XBMC/_STATIC/guide.xml":
		dict["epgUrl"] = "http://thewiz.info/XBMC/_STATIC/guide.xml"
		isSettingsChanged = True
	if dict.has_key("logoPathType") and dict["logoPathType"] != "0":
		dict["logoPathType"] = "0"
		isSettingsChanged = True
	if dict.has_key("logoPath") and dict["logoPath"] != os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'logos'):
		dict["logoPath"] = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'logos')
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

def GetMarkedLists():
	list = ["israel"]
	if (Addon.getSetting('radio').lower() == 'true'):
		list = ["radio"] + list
	if (Addon.getSetting('french').lower() == 'true'):
		list += ["france"]
	if (Addon.getSetting('russian').lower() == 'true'):
		list += ["russia"]
	return list 
	
def MakeFinalList(markedLists):	
	listsFile = os.path.join(xbmc.translatePath("special://userdata/addon_data"), AddonID, "lists", "lists.list")
	fullList = ReadList(listsFile)

	list = []
	for name in markedLists:
		list += fullList[name]

	return list
	
def ReadList(fileName):
	try:
		f = open(fileName,'r')
		fileContent = f.read()
		f.close()
		content = json.loads(fileContent)
	except:
		content = []

	return content
	
def MakeM3U(list, isIptvAddonGotham):
	M3Ulist = "#EXTM3U\n"
	for item in list:
		tvg_name = item['tvg_id'].replace(' ','_')
		tvg_logo = item['tvg_id']
		if isIptvAddonGotham:
			tvg_logo += ".png"
		radio = ' radio="true"' if item['type'].lower() == "audio" else ''
		M3Ulist += '\n#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" group-title="{2}" tvg-logo="{3}"{4},{5}\n{6}\n'.format(item['tvg_id'], tvg_name, item['group_title'], tvg_logo, radio, item['display_name'].encode("utf-8"), item['url'].encode("utf-8"))
	return M3Ulist
		
def DeleteCache():
	mypath=xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple" ).decode("utf-8")
	for f in os.listdir(mypath):
		if os.path.isfile(os.path.join(mypath,f)):
			if f.endswith('cache'):
				os.remove(os.path.join(mypath,f))

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