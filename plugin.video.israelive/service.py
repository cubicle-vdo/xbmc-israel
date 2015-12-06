import xbmc, xbmcaddon, os

Addon = xbmcaddon.Addon()
libDir = os.path.join(xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8"), 'resources', 'lib')
sys.path.insert(0, libDir)
import common

if Addon.getSetting("useIPTV") == "true":
	autoIPTV = int(Addon.getSetting("autoIPTV"))
	autoPVR = Addon.getSetting("autoPVR") == "true"
	autoStopPVR = Addon.getSetting("autoStopPVR") == "true"
	if (autoIPTV == 0 or autoIPTV == 2) and autoPVR and autoStopPVR:
		xbmc.executebuiltin('StopPVRManager')
	portNum = common.GetLivestreamerPort()
	try:
		import livestreamersrv
		livestreamersrv.start(portNum)
	except Exception as ex:
		print ex

xbmc.executebuiltin("XBMC.RunPlugin(plugin://plugin.video.israelive/default.py?mode=100&url=checkUpdates)")
xbmc.executebuiltin("XBMC.AlarmClock({0},XBMC.RunPlugin(plugin://plugin.video.israelive/default.py?mode=101&url=checkUpdates),{1},silent)".format("IsraeLiveM3U", 360))