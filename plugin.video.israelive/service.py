import xbmc, xbmcaddon, xbmcgui, os, sys, time;

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)
libDir = os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import myIPTVSimple, common

def sleepFor(timeS):
    while((not xbmc.abortRequested) and (timeS > 0)):
        xbmc.sleep(1000)
        timeS -= 1
		
def CheckUpdates():
	isListsChanged = common.UpdateLists()
	if isListsChanged:
		print "------------> IsraeLive service: Channel-list updated. <---------------"
	
	myIPTVSimple.UpdateLogos()
	
	isIPTVChanged = False
	isEPGChanged = False
	
	if Addon.getSetting("useLiveTV") == "true":
		isIPChanged = myIPTVSimple.isIPChange()
		m3uFileLastUpdate = myIPTVSimple.getM3uFileLastUpdate()
		now = int(time.time())
		isM3uFileNotUpdate = True if (now - m3uFileLastUpdate) > 82800 else False # 23 hours
		if isListsChanged or isIPChanged or myIPTVSimple.isMarkedListsChange() or isM3uFileNotUpdate:
			isIPTVChanged = myIPTVSimple.RefreshIPTVlinks()
			if isIPTVChanged:
				print "-------------> IsraeLive service: IPTV-links updated. <----------------"
			else:
				print "----------> IsraeLive service: error updating IPTV-links. <------------"
		isEPGChanged = myIPTVSimple.RefreshEPG()
		if isEPGChanged:
			print "-------------> IsraeLive service: TV-Guide updated. <-----------------"
	
	if isIPTVChanged or isEPGChanged: 
		#common.OKmsg("IsraeLIVE", "Links updated.", "Please restart XBMC or PVR db.")
		return True
	elif isListsChanged:
		pass
	else: # if nothing changed
		print "--------> IsraeLive service: Everything is up to date. :-) <-----------"
	
	return False

checkInterval = 24 * 3600 # 24 hours

print "---------------------> IsraeLive service Started <---------------------"
print "----------------> IsraeLive service: Scan At Startup <-----------------"

#xbmc.executebuiltin('StopPVRManager')
CheckUpdates()
xbmc.executebuiltin('StartPVRManager')

while (not xbmc.abortRequested):
	sleepFor(checkInterval)
	if (not xbmc.abortRequested):
		print "----------------> IsraeLive service: Schedule scan <-------------------"
		if CheckUpdates():
			xbmc.executebuiltin('StartPVRManager')
	
print "---------------------> IsraeLive service Stoped <----------------------"	