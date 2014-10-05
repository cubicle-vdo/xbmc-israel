# -*- coding: utf-8 -*-

'''
Created on 30/04/2011

@author: shai
'''
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
# __USERAGENT__ = 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'

from collections import namedtuple

import StorageServer

import urllib, urllib2, re, xbmc, xbmcplugin, xbmcgui, xbmcaddon, os, sys, time, cookielib, xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__language__ = __settings__.getLocalizedString
__cachePeriod__ = __settings__.getSetting("cache")
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__DEBUG__ = __settings__.getSetting("DEBUG") == "true"
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
sys.modules["__main__"].dbg = True
cacheServer = StorageServer.StorageServer("plugin.video.wallaNew.video", __cachePeriod__)  # (Your plugin name, Cache time in hours)


def enum(**enums):
        return type('Enum', (), enums)

def getMatches(url, pattern):
        contentType, page = getData(url)
        matches = re.compile(pattern).findall(page)
        return contentType, matches   

def getParams(arg):
        param = []
        paramstring = arg
        if len(paramstring) >= 2:
            params = arg
            cleanedparams = params.replace('?', '')
            if (params[len(params) - 1] == '/'):
                params = params[0:len(params) - 2]
            pairsofparams = cleanedparams.split('&')
            param = {}
            for i in range(len(pairsofparams)):
                splitparams = {}
                splitparams = pairsofparams[i].split('=')
                if (len(splitparams)) == 2:    
                    param[splitparams[0]] = splitparams[1]
                                
        return param

def translate(arg):
        return __language__(arg)
        
def addDir(contentType, name, url, mode, iconimage='DefaultFolder.png', elementId='', summary='', fanart='',isRealFolder=True):
        try:
           
            u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + name + "&module=" + urllib.quote_plus(elementId)
            liz = xbmcgui.ListItem(clean(contentType, name), iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(clean(contentType, name)), "Plot": urllib.unquote(summary)})
            if not fanart == '':
                liz.setProperty("Fanart_Image", fanart)
               
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isRealFolder)
            if __DEBUG__:
                 
                print "added directory success:" + clean(contentType, name) + " url=" + clean('utf-8',u)
            return ok
        except Exception as e:
            print "WALLA exception in addDir"
            print e
            raise
        

def addLink(contentType, name, url, iconimage='DefaultFolder.png', time='', sub=''):
        liz = xbmcgui.ListItem(clean(contentType, name), iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(clean(contentType, name)), "Duration":time, "Plot": urllib.unquote(sub)})
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
        return ok

def addVideoLink(contentType, name, url, mode, iconimage='DefaultFolder.png', elementId='', sum='',duration='0'):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(str(url)) + "&mode=" + str(mode) + "&name=" + name + "&module=" + urllib.quote_plus(elementId)
        liz = xbmcgui.ListItem(clean(contentType, name), iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(clean(contentType, name)),"Duration":str(duration), "Plot": urllib.unquote(sum)})
        liz.setProperty('IsPlayable', 'true')
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
        return ok
    
def getData(url, period=__cachePeriod__):
        if __DEBUG__:
            print 'url --> ' + url
       
            
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', __USERAGENT__)
            response = urllib2.urlopen(req)
            contentType = response.headers['content-type']
            if __DEBUG__:
                print "WALLA got content type " + contentType
            data = response.read().replace("\n", "").replace("\t", "").replace("\r", "")
           
            response.close()            
            
        except:
            errno, errstr = sys.exc_info()[:2]
            
            xbmc.log('Error in getData: ' + str(errno) + ': ' + str(errstr), xbmc.LOGERROR)
            return 'UTF-8', 'unavailable'
        return contentType, data

def getImageNick(series, siteName,url):
        print url 
        imageName = str(series)
        print imageName
        cacheDir = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images', siteName))
        cachePath = xbmc.translatePath(os.path.join(cacheDir, imageName))
        if not os.path.exists(cachePath):
            # # fetch the image and store it in the cache path
            if not os.path.exists(cacheDir):
                os.makedirs(cacheDir)
            contentType,page = getData(url)
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, "First time loading images please wait...", 5000, __icon__))
            titleMatches = re.compile('class="stripe_title w7b white">\s*(.*?)\s*</h1>\s*<img src="(.*?)"').findall(page)
            if len(titleMatches) == 0:
                # try a different possibility
                titleMatches = re.compile('class="stripe_title w7b white">.*?>(.*?)<.*?src="(.*?)"').findall(page)
            if titleMatches:
                    urllib.urlretrieve(titleMatches[0][1], cachePath)
            
        return cachePath

        
def getImage(imageURL, siteName):
        imageName = getImageName(imageURL)
        cacheDir = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images', siteName))
        cachePath = xbmc.translatePath(os.path.join(cacheDir, imageName))
        if not os.path.exists(cachePath):
            # # fetch the image and store it in the cache path
            if not os.path.exists(cacheDir):
                os.makedirs(cacheDir)
            urllib.urlretrieve(imageURL, cachePath)
        return cachePath
        
def getImageName(imageURL):
        idx = int(imageURL.rfind("/")) + 1
        return imageURL[idx:]

def getCookie(url, cookiename):
        req = urllib2.Request(url)
        req.add_header('User-Agent', __USERAGENT__)
        response = urllib2.urlopen(req)
        for header in response.headers:
            name = response.headers[header]
            if __DEBUG__:
                print 'Cookie --> %s' % (name)
        data = response.read().replace("\n", "").replace("\t", "").replace("\r", "")        
        response.close()
        return data, "ERROR"
        
def getEpisodeList(urlbase, inUrl, pattern, modulename, mode, patternFeatured='', patternmore='class="in_blk p_r"\sstyle=""\shref="(.*?)"'):
    contentType,mainPage = getData(inUrl)
    print inUrl
    if 'nick' in urlbase and  not 'page' in inUrl:
        urlMatch = re.compile('class="w6b.?.*?href="(.*?)">').findall(mainPage)
        print ';;;;' + str( urlMatch[0])
        if (len(urlMatch[0])) > 0:
          inUrl=urlbase+urlMatch[0]
          contentType,mainPage = getData(inUrl)
    print "modulename=" + modulename
    print "inUrl=" + inUrl
    Episode = namedtuple('Episode', ['content', 'title', 'url', 'iconImage', 'time', 'epiDetails'])    
    
    cacheKey = modulename + "_" + inUrl + "_episodes"
    episodes = cacheServer.get(cacheKey)
    
    
    if False:
        episodes = eval(episodes)
        print "Found " + str(len(episodes)) + " episodes in cache"
    
        for episode in episodes:
            addLink(episode.content, episode.title, episode.url, episode.iconImage, episode.time, episode.epiDetails)
               
    else:
        episodes = []
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, "First time loading episodes please wait...", 5000, __icon__))
        # # get all the rest of the episodes
        contentType, mainPage = getData(inUrl)
        if patternFeatured != '':
            urls = re.compile(patternFeatured).findall(mainPage)
            urls += re.compile(pattern).findall(mainPage)
        else:
            urls = re.compile(pattern).findall(mainPage)
        # # for each episode we get the episode page to parse all the info from
        for path in urls:
            contentType, page = getData(urlbase + path + '/@@/video/flv_pl')
            titleMatches = re.compile('<title>(.*?)</title>(.*)<subtitle>(.*?)<').findall(page)
            if (len(titleMatches)) == 1:
                title = titleMatches[0][0]
                images = re.compile('<preview_pic>(.*?)</preview_pic>').findall(page)
                if (len(images)) >= 1:
                    iconImage = images[0]
                details = re.compile('<synopsis>(.*?)</synopsis>').findall(page)
                if (len(details)) > 0:
                    epiDetails = details[0]
                
                timeInSeconds = re.compile('<duration>(.*?)</duration>').findall(page)
                if not timeInSeconds == None and not len(timeInSeconds[0]) <= 0:
                    time = int(timeInSeconds[0]) / 60
                else:
                    time = '00:00'
                #url = 'rtmp://waflaWNE.walla.co.il/ app=vod/ swfvfy=true swfUrl=http://i.walla.co.il/w9/swf/video_swf/vod/walla_vod_player_adt.swf?95 tcurl=rtmp://waflaWNE.walla.co.il/vod/ pageurl=http://walla.co.il/ playpath=' + re.compile('<src>(.*?)</src>').findall(page)[0]
                url='rtmp://waflaWNE.walla.co.il:1935/vod playpath='+ re.compile('<src>(.*?)</src>').findall(page)[0]+' swfUrl=http://i.walla.co.il/w9/swf/video_swf/vod/WallaMediaPlayerAvod.swf?testMode=1&v=436 pageurl='+inUrl
                epi1 = Episode(content=contentType, title=title, url=url, iconImage=iconImage, time=str(time), epiDetails=epiDetails)
                episodes.append(epi1)
                addLink(contentType, title, url, iconImage, str(time), epiDetails)
                
    
        # save to cache
        cacheServer.set(cacheKey, repr(episodes))
    
    nextPage = re.compile(patternmore).findall(mainPage)
    print str (nextPage)
    if (len(nextPage)) > 0:
        addDir('UTF-8', __language__(30001), urlbase + nextPage[0], mode, 'DefaultFolder.png', modulename)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

def convertToUTF(name):
    return clean('utf-8',name)

def cleanCache():
    print "Walla: cleaning cache for all modules "
    cacheServer.delete("%")
    cacheServer.cacheClean(True)
    
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, "Deleting cache for walla modules...", 5000, __icon__))

def clean(contentType, name):
        
    try:
         
        if isinstance(name, str):
         
            if contentType.lower().find('utf-8') == -1: 
            
                name = name.decode('windows-1255', 'replace')
                name = name.encode('utf-8')
        elif isinstance(name, unicode):
            name = name.encode('utf-8')    
 
    except Exception as e:
         print 'Error in clean: '
         print e
         raise e
#     if (name):
#         cleanName = name.replace("&quot;", "\"").replace("&#39;", "'").replace("&nbsp;", " ")
#         return  cleanName
    return name 
