import xbmc, xbmcaddon, xbmcgui, os, sys

Addon = xbmcaddon.Addon()
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')
libDir = os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'lib')
sys.path.insert(0, libDir)
import common, myFilmon

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)

remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")
remoteSettingsUrl = "https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/remoteSettings.txt"
globalGuideFile = os.path.join(user_dataDir, "guide.txt")
checkInterval = 6
	
def sleepFor(timeS):
    while((not xbmc.abortRequested) and (timeS > 0)):
        xbmc.sleep(1000)
        timeS -= 1
		
def CheckUpdates():
	remoteSettings = common.GetUpdatedList(remoteSettingsFile, remoteSettingsUrl)
	if remoteSettings == []:
		return
		
	global checkInterval
	try:
		checkInterval = remoteSettings["checkInterval"] * 3600 # in hours
	except:
		pass
		
	if Addon.getSetting("saveFilmonEPG") == "false":
		return
		
	common.UpdateZipedFile(globalGuideFile, remoteSettings["globalGuide"]["url"])
	
	plxType = int(Addon.getSetting("PlxPlaylist"))
	if plxType == 0:
		package = remoteSettings["packages"]["zip"]
		guideFile = os.path.join(user_dataDir, 'filmonZipGuide.txt')
	elif plxType == 1:
		package = remoteSettings["packages"]["light"]
		guideFile = os.path.join(user_dataDir, 'filmonLightGuide.txt')
	else:
		package = remoteSettings["packages"]["full"]
		guideFile = os.path.join(user_dataDir, 'filmonFullGuide.txt')
	
	isNewGuideFile = common.UpdateZipedFile(guideFile, package["guide"])
	if isNewGuideFile:
		return
		
	print "{0}: Updating filmonGuide localy.".format(AddonName)
	isGuideFileOld = common.isFileOld(guideFile, package["refresh"] * 3600) # 24 hours
	if isGuideFileOld:
		try:
			xbmc.executebuiltin("XBMC.Notification({0}, Making and saving Filmon's guide..., {1}, {2})".format(AddonName, 300000 ,icon))
			myFilmon.MakePLXguide(package["url"], guideFile)
			xbmc.executebuiltin("XBMC.Notification({0}, Filmon's guide saved., {1}, {2})".format(AddonName, 5000 ,icon))
		except:
			xbmc.executebuiltin("XBMC.Notification({0}, Filmon's guide NOT saved!, {1}, {2})".format(AddonName, 5000 ,icon))
		
CheckUpdates()

while (not xbmc.abortRequested):
	sleepFor(checkInterval)
	if (not xbmc.abortRequested):
		CheckUpdates()
	