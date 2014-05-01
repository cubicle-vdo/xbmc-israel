import xbmc, xbmcaddon, xbmcgui, os, sys;

AddonID = 'plugin.video.israelive'
israeliveAddon = xbmcaddon.Addon(AddonID)
libDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import myIPTVSimple

def sleepFor(timeS):
    while((not xbmc.abortRequested) and (timeS > 0)):
        xbmc.sleep(1000)
        timeS -= 1
		
def RefreshIPTVlinks():
	sourceSettings = myIPTVSimple.CheckIPTVupdates()
	if sourceSettings != None:
		if sourceSettings['isFilmonUpdate'] or sourceSettings['isNewM3U']: 
			myIPTVSimple.RefreshIPTVlinks(sourceSettings)
			print "--------------> IsraeLive service: Update finnished. <-----------------"
		else: # if nothing changed
			print "--------> IsraeLive service: Everything is up to date. :-) <-----------"

runAtStartup = israeliveAddon.getSetting("runAtStartup") == "true"
checkInterval = int(israeliveAddon.getSetting("checkInterval"))

if not runAtStartup and checkInterval <= 0:
	sys.exit()

print "---------------------> IsraeLive service Started <---------------------"

if runAtStartup:
	print "----------------> IsraeLive service: Scan At Startup <-----------------"
	RefreshIPTVlinks()

if checkInterval <= 0:
	print "--------------> IsraeLive service: No schedule scans <-----------------"
	print "---------------------> IsraeLive service Stoped <----------------------"
	sys.exit()

while (not xbmc.abortRequested):
	sleepFor(checkInterval * 3600)
	if (not xbmc.abortRequested):
		print "----------------> IsraeLive service: Schedule scan <-------------------"
		RefreshIPTVlinks()
	
print "---------------------> IsraeLive service Stoped <----------------------"	