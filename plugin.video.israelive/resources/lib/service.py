import xbmc, xbmcaddon, common

Addon = xbmcaddon.Addon()
ver = xbmc.__version__.split('.')
kodi17 = True if int(ver[0]) > 2 or int(ver[0]) == 2 and int(ver[1]) > 24 else False
		
if not kodi17 and common.getUseIPTV() and common.getAutoIPTV() and Addon.getSetting("autoPVR") == "true" and  Addon.getSetting("autoStopPVR") == "true":
	xbmc.executebuiltin('StopPVRManager')

xbmc.executebuiltin("XBMC.RunPlugin(plugin://plugin.video.israelive/default.py?mode=100&url=checkUpdates)")
xbmc.executebuiltin("XBMC.AlarmClock({0},XBMC.RunPlugin(plugin://plugin.video.israelive/default.py?mode=101&url=checkUpdates),{1},silent)".format("IsraeLiveM3U", 360))