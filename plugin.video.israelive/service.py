import xbmc, xbmcaddon, xbmcgui, os, sys, platform
import repoCheck

repoCheck.UpdateRepo()

Addon = xbmcaddon.Addon()
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')
libDir = os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'lib')
sys.path.insert(0, libDir)
import common

portNum = 65007
try:
	portNum = int(Addon.getSetting("LiveStreamerPort"))
except:
	pass
	
pvrStoped = False
useIPTV = False
if Addon.getSetting("useIPTV") == "true":
	import livestreamersrv, myIPTV
	try:
		livestreamersrv.start(portNum)
		useIPTV = True
		autoIPTV = int(Addon.getSetting("autoIPTV"))
		if autoIPTV == 0 or autoIPTV == 2:
			xbmc.executebuiltin('StopPVRManager')
			pvrStoped = True
	except Exception as ex:
		print ex

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)

remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")
plxFile = os.path.join(user_dataDir, "israelive.plx")
globalGuideFile = os.path.join(user_dataDir, "guide.txt")
filmonGuideFile = os.path.join(user_dataDir, 'filmonGuide.txt')
fullGuideFile = os.path.join(user_dataDir, 'fullGuide.txt')
iptvChannelsFile = os.path.join(user_dataDir, "iptv.m3u")
iptvGuideFile = os.path.join(user_dataDir, "guide.xml")
iptvLogosDir = os.path.join(user_dataDir, "logos")
remoteSettings = common.GetRemoteSettings(updateDefault=True)

checkInterval = 12
	
def sleepFor(timeS):
    while((not xbmc.abortRequested) and (timeS > 0)):
        xbmc.sleep(1000)
        timeS -= 1
		
def CheckUpdates():
	common.CheckNewVersion()
	global remoteSettings
	remoteSettings = common.GetUpdatedList(remoteSettingsFile, "remoteSettings", remoteSettings, forceUpdate=True)
	if remoteSettings == []:
		global pvrStoped
		if pvrStoped:
			xbmc.executebuiltin('StartPVRManager')
		return
		
	global checkInterval
	try:
		checkInterval = remoteSettings["remoteSettings"]["refresh"] * 3600 # in hours
	except:
		pass
		
	refresh = common.GetSubKeyValue(remoteSettings, "plx", "refresh")
	if not refresh is None:
		common.UpdatePlx(plxFile, "plx", remoteSettings, refreshInterval = refresh * 3600)

	if Addon.getSetting("useEPG") == "true":
		refresh = common.GetSubKeyValue(remoteSettings, "globalGuide", "refresh")
		if not refresh is None:
			common.isFileOld(globalGuideFile, refresh * 3600) and common.UpdateZipedFile(globalGuideFile, "globalGuide", remoteSettings)
		
		refresh = common.GetSubKeyValue(remoteSettings, "filmonGuide", "refresh")
		if not refresh is None:
			common.isFileOld(filmonGuideFile, refresh * 3600) and common.UpdateZipedFile(filmonGuideFile, "filmonGuide", remoteSettings)
		
		common.MergeGuides(globalGuideFile, filmonGuideFile, fullGuideFile)
		
		if Addon.getSetting("useIPTV") == "true":
			myIPTV.makeIPTVlist(iptvChannelsFile, portNum)
			myIPTV.MakeChannelsGuide(fullGuideFile, iptvGuideFile)
			myIPTV.RefreshPVR(iptvChannelsFile, iptvGuideFile, iptvLogosDir)
			myIPTV.SaveChannelsLogos(iptvLogosDir)
		
CheckUpdates()

while (not xbmc.abortRequested):
	sleepFor(checkInterval)
	if (not xbmc.abortRequested):
		CheckUpdates()
	
if useIPTV:
	try:
		livestreamersrv.stop(portNum)
	except Exception as ex:
		print ex
