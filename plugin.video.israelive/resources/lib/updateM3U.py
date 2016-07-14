import xbmc, xbmcaddon, os, sys

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
libDir = os.path.join(addonPath, 'resources', 'lib')
sys.path.insert(0, libDir)
import myIPTV, common

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)
iptvChannelsFile = os.path.join(user_dataDir, "iptv.m3u")
iptvGuideFile = os.path.join(user_dataDir, "guide.xml")
iptvLogosDir = os.path.join(user_dataDir, "logos")

def Update():
	if common.getUseIPTV():
		myIPTV.makeIPTVlist(iptvChannelsFile)
		myIPTV.RefreshPVR(iptvChannelsFile, iptvGuideFile, iptvLogosDir)
		if myIPTV.GetIptvType() < 2:
			myIPTV.SaveChannelsLogos(iptvLogosDir)
	xbmc.executebuiltin("XBMC.AlarmClock({0},XBMC.RunPlugin(plugin://plugin.video.israelive/default.py?mode=101&url=checkUpdates),{1},silent)".format("IsraeLiveM3U", 720))