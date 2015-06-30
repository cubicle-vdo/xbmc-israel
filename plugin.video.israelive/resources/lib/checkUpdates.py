import xbmc, xbmcaddon, os, sys

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
libDir = os.path.join(addonPath, 'resources', 'lib')
sys.path.insert(0, libDir)
import common
common.CheckNewVersion()

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)

remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")
plxFile = os.path.join(user_dataDir, "israelive.plx")
fullGuideFile = os.path.join(user_dataDir, 'fullGuide.txt')
iptvChannelsFile = os.path.join(user_dataDir, "iptv.m3u")
iptvGuideFile = os.path.join(user_dataDir, "guide.xml")
iptvLogosDir = os.path.join(user_dataDir, "logos")
remoteSettings = common.GetRemoteSettings()
remoteSettings = common.GetUpdatedList(remoteSettingsFile, "remoteSettings", remoteSettings, forceUpdate=True)
if remoteSettings == []:
	xbmc.executebuiltin('StartPVRManager')
else:
	refresh = common.GetSubKeyValue(remoteSettings, "plx", "refresh")
	if not refresh is None:
		common.UpdatePlx(plxFile, "plx", remoteSettings, refreshInterval = refresh * 3600)

	if Addon.getSetting("useEPG") == "true":
		refresh = common.GetSubKeyValue(remoteSettings, "fullGuide", "refresh")
		isGuideUpdated = False
		if not refresh is None and common.isFileOld(fullGuideFile, refresh * 3600) and common.UpdateZipedFile(fullGuideFile, "fullGuide", remoteSettings):
			isGuideUpdated = True
			epg = common.ReadList(fullGuideFile)
			fullCategoriesList = []
			selectedCategoriesList = []
			categoriesList = []
			
			iptvList = Addon.getSetting("iptvList")
			if iptvList == "0": # Favourites
				categoriesList = [{"id": "Favourites"}]
			elif iptvList == "1": # No filter 
				categoriesList = fullCategoriesList = common.ReadList(os.path.join(user_dataDir, "lists", "categories.list"))
			elif iptvList == "2": # Selected categories
				categoriesList = selectedCategoriesList = common.ReadList(os.path.join(user_dataDir, "lists", "selectedCategories.list"))
			
			common.MakeCatGuides(categoriesList, epg)
			
		if Addon.getSetting("useIPTV") == "true":
			import myIPTV
			myIPTV.makeIPTVlist(iptvChannelsFile)
			myIPTV.MakeChannelsGuide(fullGuideFile, iptvGuideFile)
			myIPTV.RefreshPVR(iptvChannelsFile, iptvGuideFile, iptvLogosDir)
			
		if isGuideUpdated:
			if fullCategoriesList == []:
				fullCategoriesList =  common.ReadList(os.path.join(user_dataDir, "lists", "categories.list"))
			if iptvList == "0": # Favourites
				categoriesList = fullCategoriesList
			elif iptvList == "1": # No filter 
				categoriesList = [{"id": "Favourites"}]
			elif iptvList == "2": # Selected categories
				categoriesList = common.GetUnSelectedList(fullCategoriesList, selectedCategoriesList)
				categoriesList.append({"id": "Favourites"})
				
			common.MakeCatGuides(categoriesList, epg)
			
		if Addon.getSetting("useIPTV") == "true":
			myIPTV.SaveChannelsLogos(iptvLogosDir)

	checkInterval = 720 # 12 hours = 720 minutes
	try:
		checkInterval = remoteSettings["remoteSettings"]["refresh"] * 60 # hours to minutes
	except:
		pass
	
xbmc.executebuiltin("XBMC.AlarmClock({0},XBMC.RunScript({1}),{2},silent)".format(AddonName, os.path.join(libDir, "checkUpdates.py"), checkInterval))