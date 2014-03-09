
import xbmc
import xbmcaddon
import xbmcgui


def CheckIdle(maxIdle):
    idle = xbmc.getGlobalIdleTime()
    if idle < maxIdle:
        return

    delay = 60
    count = delay
    dp = xbmcgui.DialogProgress()
    dp.create("TV Guide Dixie","Streaming will automatically quit in %d seconds" % count, "Press Cancel to contine viewing")
    dp.update(0)
              
    while xbmc.Player().isPlaying() and count > 0 and not dp.iscanceled():
        xbmc.sleep(1000)
        count -= 1
        perc = int(((delay - count) / float(delay)) * 100)
        if count > 1:
            dp.update(perc,"Streaming will automatically quit in %d seconds" % count, "Press Cancel to contine viewing")
        else:
            dp.update(perc,"Streaming will automatically quit in %d second" % count, "Press Cancel to contine viewing")            

    if not dp.iscanceled():
        xbmc.Player().stop()


def play(url, windowed):
    ADDON = xbmcaddon.Addon(id = 'script.tvguidedixie.o2ri')
    maxIdle = int(ADDON.getSetting('idle')) * 60 * 60
    if not checkForAlternateStreaming(url):
        xbmc.Player().play(item = url, windowed = windowed)
        print '****** Attempt 1 ******'
        print url
        xbmc.sleep(100)
        if not xbmc.Player().isPlaying():
            xbmc.executebuiltin('XBMC.RunPlugin(%s)' % url)
            print '****** Attempt 2 ******'
            print url

    xbmc.sleep(1000)
    while xbmc.Player().isPlaying():
        xbmc.sleep(5000)
        CheckIdle(maxIdle)


def checkForAlternateStreaming(url):
    if "plugin.video.ntv" in url:
        print '****** Alternate NTV ******'
        print url
        return alternateStream(url)

    if 'plugin.video.expattv' in url:
        print '****** Alternate  ExPat ******'
        print url
        return alternateStream(url)

    if 'plugin.video.filmon' in url:
        print '****** Alternate  FilmOn ******'
        print url
        return alternateStream(url)

    if 'plugin.video.notfilmon' in url:
        print '****** Alternate NotFilmOn ******'
        print url
        return alternateStream(url)
        
    if 'plugin.video.itv' in url:
        print '****** Alternate ITV ******'
        print url
        return alternateStream(url)
        
    if 'plugin.video.iplayer' in url:
        print '****** Alternate iPlayer ******'
        print url
        return alternateStream(url)
        
    if 'plugin.video.musicvideojukebox' in url:
        print '****** Alternate JukeBox ******'
        print url
        return alternateStream(url)
        
    if 'plugin.video.muzu.tv' in url:
        print '****** Alternate Muzu ******'
        print url
        return alternateStream(url)
        
    if 'plugin.audio.ramfm' in url:
        print '****** Alternate RAM FM ******'
        print url
        return alternateStream(url)
        
    if 'plugin.video.movie25' in url:
        print '****** Alternate MashUp ******'
        print url
        return alternateStream(url)
        
    return False

def alternateStream(url):
    xbmc.executebuiltin('XBMC.RunPlugin(%s)' % url)
    
    retries = 10
    while retries > 0 and not xbmc.Player().isPlaying():
        retries -= 1
        xbmc.sleep(1000)
        
    print '****** Alternate Method ******'
    print url
    return True



if __name__ == '__main__': 
    play(sys.argv[1], sys.argv[2] == 1)


# expattv
# static.filmon.com
# notfilmon
# plugin.video.iplayer
# plugin.video.itv
# plugin.video.youtube
# plugin.video.musicvideojukebox
# plugin.video.muzu.tv
# plugin.audio.ramfm
# plugin.video.tgun
# plugin.video.movie25