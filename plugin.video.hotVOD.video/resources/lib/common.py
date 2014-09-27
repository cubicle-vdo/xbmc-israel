# -*- coding: utf-8 -*-

'''
Created on 30/04/2011

@author: shai
'''
__USERAGENT__ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'



import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os,sys,time

__settings__ = xbmcaddon.Addon(id='plugin.video.hotVOD.video')
__cachePeriod__ = __settings__.getSetting("cache")
__PLUGIN_PATH__ = __settings__.getAddonInfo('path').decode("utf-8")
__DEBUG__ = __settings__.getSetting("DEBUG") == "true"

cacheImgDir = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images'))
if not os.path.exists(cacheImgDir):
	os.makedirs(cacheImgDir)
cachePageDir = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'pages'))
if not os.path.exists(cachePageDir):
	os.makedirs(cachePageDir)

def enum(**enums):
        return type('Enum', (), enums)

def getMatches(url, pattern):
        page = getData(url)
        matches=re.compile(pattern).findall(page)
        return matches   

def getParams(arg):
        param=[]
        paramstring=arg
        if len(paramstring)>=2:
            params=arg
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:    
                    param[splitparams[0]]=splitparams[1]
                                
        return param
    
def addDir(name, url, mode, iconimage='DefaultFolder.png', elementId=None, summary='', fanart=''):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + name
        if not elementId == None and not elementId == '':
            u += "&module=" + urllib.quote_plus(elementId)
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(name), "Plot": urllib.unquote(summary)})
        if not fanart == '':
            liz.setProperty("Fanart_Image", fanart)
        if mode==6:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
            
        else:
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok

def addVideoLink(name, url, mode, iconimage='DefaultFolder.png', summary = ''):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + name
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(name), "Plot": urllib.unquote(summary)})    
        liz.setProperty('IsPlayable', 'true')
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
        return ok
    
def addLink(name, url, iconimage='DefaultFolder.png', sub=''):
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(name), "Plot": urllib.unquote(sub)})
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
        return ok

    
def getData(url, timeout=__cachePeriod__, name=''):
        if __DEBUG__:
            print 'url --> ' + url
            print 'name --> ' + name
        if timeout > 0:
            if name == '':
                cachePath = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'pages', urllib.quote(url,"")))
            else:
                cachePath = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'pages', name))
            if (os.path.exists(cachePath) and (time.time()-os.path.getmtime(cachePath))/60/60 <= float(timeout)):
                f = open(cachePath, 'r')
                ret = f.read()
                f.close()
                if __DEBUG__:
                    print 'returned data from cache'
                return ret
        try:     
            req = urllib2.Request(url)
            req.add_header('User-Agent', __USERAGENT__)        
            response = urllib2.urlopen(req)
            data = response.read().replace("\n","").replace("\t","").replace("\r","")
            response.close()
            if timeout > 0:
                f = open(cachePath, 'wb')
                f.write(data)
                f.close()
            if __DEBUG__:
                print data
            return data
        except:
            if __DEBUG__:
                errno, errstr = sys.exc_info()[:2]
                print 'Error in getData: ' + str(errno) + ": " + str(errstr)
            xbmc.log('Error in getData: Unable to save cache', xbmc.LOGERROR)
            return 'unavailable'

def getImage(imageURL, siteName):
        imageName = getImageName(imageURL)
        cacheDir = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images', siteName))
        cachePath = xbmc.translatePath(os.path.join(cacheDir, imageName))
        if not os.path.exists(cachePath):
            ## fetch the image and store it in the cache path
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
        cooks = response.headers["set-cookie"].split(";")
        for x in cooks:
            y = x.split("=")
            if (y[0] == cookiename):
                return y[1]
        response.close()
        return "ERROR"

  
def getRealVideoLink(videoId):
        page = getData("http://10tv.nana10.co.il/Video/?VideoID=" + videoId, 744)
        ret = re.compile('var sCmsVideoURL.*?"(.*?)"').findall(page)
        if (len(ret) == 0 or (len(ret) > 0 and len(ret[0]) == 0)):
            ret = re.compile('var VideoLinkHQ.*?"(.*?)"').findall(page)
            if (len(ret) == 0 or (len(ret) > 0 and len(ret[0]) == 0)):
                ret = re.compile('var VideoLink\s*?=\s*"(.*?)"').findall(page)
        else:
            # this is a special case where we get a play list
            playlist = getData(ret[0] + "&ticket=" + getCookie("http://10tv.nana10.co.il/Video/?VideoID=" + videoId, "CUTicket" + videoId), 744, str(videoId))
            rets = re.compile('<ref href="(.+?)"').findall(playlist)
            if len(rets) > 1:
                return rets[1]
            elif len(rets) == 1:
                return rets[0] 
            else:
                return 'unavailable'
        if (len(ret) > 0 and len(ret[0]) > 0):
            ret = ret[0]
            if ret.find('gmpl.aspx') != -1:
                ret = ret.replace('gmpl.aspx','gm.asp')
            return ret + "&ticket=" + getCookie("http://10tv.nana10.co.il/Video/?VideoID=" + videoId, "CUTicket" + videoId)