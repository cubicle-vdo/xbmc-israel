import xbmc, xbmcaddon
import socket
from livestreamerXBMCLocalProxy import ThreadedHTTPServer, MyHandler

try:
	AddonID = "plugin.video.israelive"
	Addon = xbmcaddon.Addon(AddonID)
	hostName = '127.0.0.1'
	isIsraeLiveON = True
except:
	isIsraeLiveON = False

if isIsraeLiveON and Addon.getSetting("useIPTV") == "true":
	socket.setdefaulttimeout(10)
	try:
		portNum = int(Addon.getSetting("LiveStreamerPort"))
	except:
		portNum = 65007
	proxy = ThreadedHTTPServer((hostName, portNum), MyHandler)
	xbmc.log("Livestreamer: Server Starts - {0} on port {1}".format(hostName, portNum), 2)
	if int(xbmc.__version__.split('.')[1]) < 19:
		while not xbmc.abortRequested:
			proxy.handle_request()
			xbmc.sleep(1000)
	else:
		monitor = xbmc.Monitor()
		while not monitor.abortRequested():
			proxy.handle_request()
			if monitor.waitForAbort(1):
				break
	proxy.server_close()
	xbmc.log("Livestreamer: Server Stops - {0} on port {1}".format(hostName, portNum), 2)
