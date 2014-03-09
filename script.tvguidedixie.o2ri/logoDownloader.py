import urllib,dxmnew,xbmc,xbmcgui,xbmcaddon
ADDON     = xbmcaddon.Addon(id = 'script.tvguidedixie.o2ri')
dialog = xbmcgui.DialogProgress()
dialog.create('Please Wait.', 'Default Logo Pack Downloading...')
dialog.update(0)
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
Path=os.path.join(datapath,'extras')
try: os.makedirs(Path)
except: pass
Url = 'https://dl.dropboxusercontent.com/u/5461675/logos.zip'
LocalName = 'logos.zip'
LocalFile = xbmc.translatePath(os.path.join(Path, LocalName))
dialog.update(33)
try: urllib.urlretrieve(Url,LocalFile)
except:xbmc.executebuiltin("XBMC.Notification(TV Guide Dixie,Logo download failed,3000)")
dialog.update(66)
if os.path.isfile(LocalFile):
    extractFolder = Path
    pluginsrc =  xbmc.translatePath(os.path.join(extractFolder))
    dxmnew.unzipAndMove(LocalFile,extractFolder,pluginsrc)
    dialog.update(100)
    dialog.close()
    ok = xbmcgui.Dialog()
    ok.ok('TV Guide Dixie', 'Logo Pack Download Complete')
try:os.remove(LocalFile)
except:pass
