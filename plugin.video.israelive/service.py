import xbmc, xbmcaddon, xbmcgui, os, sys

Addon = xbmcaddon.Addon()
libDir = os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'lib')
sys.path.insert(0, libDir)
import common, myFilmon

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)

plxListFile = os.path.join(user_dataDir, 'plxList.txt')
plxListFileUrl = "https://dl.dropboxusercontent.com/u/26001898/XBMC/israelive/plxList.txt"
	
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')
	
def sleepFor(timeS):
    while((not xbmc.abortRequested) and (timeS > 0)):
        xbmc.sleep(1000)
        timeS -= 1
		
def CheckUpdates():
	if Addon.getSetting("saveFilmonEPG") == "false":
		return
		
	plxType = int(Addon.getSetting("PlxPlaylist"))
	if plxType == 0:
		PlxPlaylist = "zip"
		guideFile = os.path.join(user_dataDir, 'filmonZipGuide.txt')
	elif plxType == 1:
		PlxPlaylist = "light"
		guideFile = os.path.join(user_dataDir, 'filmonLightGuide.txt')
	else:
		PlxPlaylist = "full"
		guideFile = os.path.join(user_dataDir, 'filmonFullGuide.txt')
	
	plxList = common.ReadPlxList(plxListFile, plxListFileUrl)
					
	isNewGuideFile = common.UpdateFile(guideFile, plxList[PlxPlaylist]["guide"])
	if isNewGuideFile:
		return
		
	print "{0}: Updating filmonGuide localy.".format(AddonName)
	isGuideFileOld = common.isFileOld(guideFile, 24 * 3600) # 24 hours
	if isGuideFileOld:
		try:
			xbmc.executebuiltin("XBMC.Notification({0}, Making and saving Filmon's guide..., {1}, {2})".format(AddonName, 300000 ,icon))
			myFilmon.MakePLXguide(plxList[PlxPlaylist]["url"], guideFile)
			xbmc.executebuiltin("XBMC.Notification({0}, Filmon's guide saved., {1}, {2})".format(AddonName, 5000 ,icon))
		except:
			xbmc.executebuiltin("XBMC.Notification({0}, Filmon's guide NOT saved!, {1}, {2})".format(AddonName, 5000 ,icon))
		
	
#if Addon.getSetting("saveFilmonEPG") == "false":
#	sys.exit()
	
checkInterval = 4 * 3600 # 4 hours
CheckUpdates()

while (not xbmc.abortRequested):
	sleepFor(checkInterval)
	if (not xbmc.abortRequested):
		CheckUpdates()
	