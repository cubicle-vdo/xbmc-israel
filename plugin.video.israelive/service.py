import xbmc, xbmcaddon, os, sys;

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)
libDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import myIPTVSimple, common

def sleepFor(timeS):
    while((not xbmc.abortRequested) and (timeS > 0)):
        xbmc.sleep(1000)
        timeS -= 1
		
def RefreshIPTVlinks():
	nothingChanged = True
	if common.UpdateLists():
		print "------------> IsraeLive service: Channel-list updated. <---------------"
		nothingChanged = False
	if useLiveTV and (nothingChanged == False or myIPTVSimple.isIPTVChange()):
		myIPTVSimple.RefreshIPTVlinks()
		print "-------------> IsraeLive service: IPTV-links updated. <----------------"
		nothingChanged = False
	if nothingChanged: # if nothing changed
		print "--------> IsraeLive service: Everything is up to date. :-) <-----------"

useLiveTV = Addon.getSetting("useLiveTV") == "true"
checkInterval = 24 #hours

print "---------------------> IsraeLive service Started <---------------------"
print "----------------> IsraeLive service: Scan At Startup <-----------------"
RefreshIPTVlinks()

while (not xbmc.abortRequested):
	sleepFor(checkInterval * 3600)
	if (not xbmc.abortRequested):
		print "----------------> IsraeLive service: Schedule scan <-------------------"
		RefreshIPTVlinks()
	
print "---------------------> IsraeLive service Stoped <----------------------"	