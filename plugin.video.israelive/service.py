import xbmc, xbmcaddon, xbmcgui, os, sys;

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)
libDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'lib')
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
		if isListsChanged or isIPChanged or myIPTVSimple.isMarkedListsChange():
			isIPTVChanged = myIPTVSimple.RefreshIPTVlinks()
			if isIPTVChanged:
				print "-------------> IsraeLive service: IPTV-links updated. <----------------"
			else:
				print "----------> IsraeLive service: error updating IPTV-links. <------------"
		isEPGChanged = myIPTVSimple.RefreshEPG()
		if isEPGChanged:
			print "-------------> IsraeLive service: TV-Guide updated. <-----------------"
	
	if isIPTVChanged or isEPGChanged: 
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'Links updated.', "Please restart XBMC or PVR db.")
	elif isListsChanged:
		pass
	else: # if nothing changed
		print "--------> IsraeLive service: Everything is up to date. :-) <-----------"

checkInterval = 24  # hours

print "---------------------> IsraeLive service Started <---------------------"
print "----------------> IsraeLive service: Scan At Startup <-----------------"

CheckUpdates()

while (not xbmc.abortRequested):
	sleepFor(checkInterval * 3600)
	if (not xbmc.abortRequested):
		print "----------------> IsraeLive service: Schedule scan <-------------------"
		CheckUpdates()
	
print "---------------------> IsraeLive service Stoped <----------------------"	