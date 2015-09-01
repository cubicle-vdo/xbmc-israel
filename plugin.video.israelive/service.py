import xbmc, xbmcaddon, os

Addon = xbmcaddon.Addon()
libDir = os.path.join(xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8"), 'resources', 'lib')
sys.path.insert(0, libDir)
import common
xbmc.executebuiltin("XBMC.RunScript({0})".format(os.path.join(libDir, "repoCheck.py")), True)

if Addon.getSetting("useIPTV") == "true":
	autoIPTV = int(Addon.getSetting("autoIPTV"))
	autoPVR = Addon.getSetting("autoPVR") == "true"
	autoStopPVR = Addon.getSetting("autoStopPVR") == "true"
	if (autoIPTV == 0 or autoIPTV == 2) and autoPVR and autoStopPVR:
		xbmc.executebuiltin('StopPVRManager')
	portNum = common.GetLivestreamerPort()
	try:
		xbmc.executebuiltin("XBMC.RunScript({0},{1})".format(os.path.join(libDir, "livestreamersrv.py"), portNum), True)
	except Exception as ex:
		print ex

xbmc.executebuiltin("XBMC.RunScript({0})".format(os.path.join(libDir, "checkUpdates.py")))
xbmc.executebuiltin("XBMC.AlarmClock({0},XBMC.RunScript({1}),{2},silent)".format("IsraeLiveM3U", os.path.join(libDir, "updateM3U.py"), 360))