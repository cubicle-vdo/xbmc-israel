import xbmc, xbmcaddon, common

Addon = xbmcaddon.Addon()

if common.getUseIPTV() and common.getAutoIPTV() and Addon.getSetting("autoPVR") == "true" and  Addon.getSetting("autoStopPVR") == "true":
	xbmc.executebuiltin('StopPVRManager')

xbmc.executebuiltin("XBMC.RunPlugin(plugin://plugin.video.israelive/default.py?mode=100&url=checkUpdates)")
xbmc.executebuiltin("XBMC.AlarmClock({0},XBMC.RunPlugin(plugin://plugin.video.israelive/default.py?mode=101&url=checkUpdates),{1},silent)".format("IsraeLiveM3U", 360))