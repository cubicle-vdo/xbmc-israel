import xbmc, xbmcaddon, xbmcgui, os, sys, platform

Addon = xbmcaddon.Addon()
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')
libDir = os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'lib')
sys.path.insert(0, libDir)
import common, myFilmon

portNum = 65007
try:
	portNum = int(Addon.getSetting("LiveStreamerPort"))
except:
	pass
	
useIPTV = False
if Addon.getSetting("useIPTV") == "true":# and platform.system().lower() == "windows":
	import livestreamersrv, myIPTV
	livestreamersrv.start(portNum)
	useIPTV = True

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)

remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")
remoteSettingsUrl = Addon.getSetting("remoteSettingsUrl")
globalGuideFile = os.path.join(user_dataDir, "guide.txt")
filmonGuideFile = os.path.join(user_dataDir, 'filmonFullGuide.txt')
checkInterval = 12
	
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
		
	#useIPTV = True if Addon.getSetting("useIPTV") == "true" and platform.system().lower() == "windows" else False
	useIPTV = True if Addon.getSetting("useIPTV") == "true" else False

	package = remoteSettings["packages"]["full"]
	
	if common.UpdatePlx(package["url"], "wow", refreshInterval=package["plxRefresh"] * 3600) and useIPTV:
		myIPTV.makeIPTVlist(listsDir, "wow.plx", "Main", os.path.join(user_dataDir, "iptv.m3u"))
		
	if Addon.getSetting("useEPG") == "false":
		return
		
	isGuideUpdated = False
	if common.isFileOld(globalGuideFile, remoteSettings["globalGuide"]["refresh"] * 3600) and common.UpdateZipedFile(globalGuideFile, remoteSettings["globalGuide"]["url"]):
		isGuideUpdated = True

	if common.isFileOld(filmonGuideFile, package["refresh"] * 3600) and common.UpdateZipedFile(filmonGuideFile, package["guide"]):
		isGuideUpdated = True
		
	if isGuideUpdated and useIPTV:
		myIPTV.MakeChannelsGuide(globalGuideFile, remoteSettings["globalGuide"]["url"], filmonGuideFile, package["guide"], os.path.join(user_dataDir, "guide.xml"))
		myIPTV.RefreshPVR(os.path.join(user_dataDir, "iptv.m3u"), os.path.join(user_dataDir, "guide.xml"), os.path.join(user_dataDir, "logos"))
		
CheckUpdates()

while (not xbmc.abortRequested):
	sleepFor(checkInterval)
	if (not xbmc.abortRequested):
		CheckUpdates()
	