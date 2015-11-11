import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
import xbmc, xbmcaddon
from proxy import HTTP, ProxyService, PROXY_PORT

__settings__ = xbmcaddon.Addon(id='plugin.video.sdarot.tv')

class ProxyMonitor(xbmc.Monitor):
    def __init__(self):
        xbmc.Monitor.__init__(self)
        self.proxy = None
        
    def start_proxy(self):
        if self.proxy is None:
            self.proxy = ProxyService(HTTP("127.0.0.1", PROXY_PORT))
            self.proxy.start()
        
    def close_proxy(self):
        if self.proxy is not None:
            self.proxy.stop()
            self.proxy = None

    def onSettingsChanged(self):
        use_proxy = __settings__.getSetting("use_proxy") == "true"
        if use_proxy:
            self.start_proxy()
        else:
            self.close_proxy()
            
if __name__ == '__main__':
    monitor = ProxyMonitor()
    monitor.onSettingsChanged()
    monitor.waitForAbort()  
    print 'Sdarot: closing service'
    monitor.close_proxy()
    