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
remoteSettingsUrl = Addon.getSetting("remoteSettingsUrl")
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
		
	package = remoteSettings["packages"]["full"]
	
	common.UpdatePlx(package["url"], "wow", refreshInterval=package["plxRefresh"] * 3600) # in hours
	
	if Addon.getSetting("useEPG") == "false":
		return
		
	if common.isFileOld(globalGuideFile, remoteSettings["globalGuide"]["refresh"] * 3600) : # in hours
		common.UpdateZipedFile(globalGuideFile, remoteSettings["globalGuide"]["url"])

	filmonGuideFile = os.path.join(user_dataDir, 'filmonFullGuide.txt')
	if common.isFileOld(filmonGuideFile, package["refresh"] * 3600): # in hours
		common.UpdateZipedFile(filmonGuideFile, package["guide"])
		
CheckUpdates()

while (not xbmc.abortRequested):
	sleepFor(checkInterval)
	if (not xbmc.abortRequested):
		CheckUpdates()
	