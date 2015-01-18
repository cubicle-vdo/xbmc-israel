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
	
useIPTV = False
if Addon.getSetting("useIPTV") == "true":
	import livestreamersrv, myIPTV
	try:
		livestreamersrv.start(portNum)
		useIPTV = True
	except Exception as ex:
		print ex

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)

remoteSettingsUrl = common.GetRemoteSettingsUrl()
remoteSettingsFile = os.path.join(user_dataDir, "remoteSettings.txt")
plxFile = os.path.join(user_dataDir, "israelive.plx")
globalGuideFile = os.path.join(user_dataDir, "guide.txt")
filmonGuideFile = os.path.join(user_dataDir, 'filmonGuide.txt')
fullGuideFile = os.path.join(user_dataDir, 'fullGuide.txt')
iptvChannelsFile = os.path.join(user_dataDir, "iptv.m3u")
iptvGuideFile = os.path.join(user_dataDir, "guide.xml")
iptvLogosDir = os.path.join(user_dataDir, "logos")

checkInterval = 12
	
def sleepFor(timeS):
    while((not xbmc.abortRequested) and (timeS > 0)):
        xbmc.sleep(1000)
        timeS -= 1
		
def CheckUpdates():
	common.CheckNewVersion()
	remoteSettings = common.GetUpdatedList(remoteSettingsFile, remoteSettingsUrl)
	if remoteSettings == []:
		return
		
	global checkInterval
	try:
		checkInterval = remoteSettings["checkInterval"] * 3600 # in hours
	except:
		pass
		
	isPlxUpdated = False
	if common.UpdatePlx(remoteSettings["plxUrl"], plxFile, refreshInterval=remoteSettings["plxRefresh"] * 3600):
		isPlxUpdated = True

	if Addon.getSetting("useEPG") == "true":
		isGuideUpdated = False
		if common.isFileOld(globalGuideFile, remoteSettings["globalGuideRefresh"] * 3600) and common.UpdateZipedFile(globalGuideFile, remoteSettings["globalGuideUrl"]):
			isGuideUpdated = True
		if common.isFileOld(filmonGuideFile, remoteSettings["filmonGuideRefresh"] * 3600) and common.UpdateZipedFile(filmonGuideFile, remoteSettings["filmonGuideUrl"]):
			isGuideUpdated = True
		
		if isGuideUpdated:
			common.MergeGuides(globalGuideFile, filmonGuideFile, fullGuideFile)
		if Addon.getSetting("useIPTV") == "true":
			#if isPlxUpdated:
			#	myIPTV.makeIPTVlist(iptvChannelsFile, portNum)
			myIPTV.makeIPTVlist(iptvChannelsFile, portNum)
			if isGuideUpdated:
				myIPTV.MakeChannelsGuide(fullGuideFile, iptvGuideFile)
			#if isPlxUpdated or isGuideUpdated:
			#	myIPTV.RefreshPVR(iptvChannelsFile, iptvGuideFile, iptvLogosDir)
			myIPTV.RefreshPVR(iptvChannelsFile, iptvGuideFile, iptvLogosDir)
		
	if isPlxUpdated:
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
