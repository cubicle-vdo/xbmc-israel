# -*- coding: utf-8 -*-

'''
Created on 30/04/2011

@author: shai
'''
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'



import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os,sys,time,cookielib

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__language__ = __settings__.getLocalizedString
__cachePeriod__ = __settings__.getSetting("cache")
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__DEBUG__ = __settings__.getSetting("DEBUG") == "true"

def enum(**enums):
        return type('Enum', (), enums)

def getMatches(url, pattern):
        contentType,page = getData(url)
        matches=re.compile(pattern).findall(page)
        return contentType,matches   

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

def translate(arg):
        return __language__(arg)
        
def addDir(contentType, name,url,mode,iconimage='DefaultFolder.png',elementId='',summary='', fanart=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+name+"&module="+urllib.quote_plus(elementId)
        liz=xbmcgui.ListItem(clean(contentType, name), iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": urllib.unquote(clean(contentType, name)), "Plot": urllib.unquote(summary)})
        if not fanart=='':
            liz.setProperty("Fanart_Image", fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(contentType, name,url,iconimage='DefaultFolder.png',time='',sub=''):
        liz=xbmcgui.ListItem(clean(contentType, name), iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": urllib.unquote(clean(contentType, name)),"Duration":time,"Plot": urllib.unquote(sub)} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addVideoLink(contentType, name, url, mode, iconimage='DefaultFolder.png', elementId='', sum=''):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(str(url)) + "&mode=" + str(mode) + "&name=" + name+"&module="+urllib.quote_plus(elementId)
        liz = xbmcgui.ListItem(clean(contentType, name), iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(clean(contentType, name)),"Plot": urllib.unquote(sum)})
        liz.setProperty('IsPlayable', 'true')
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
        return ok
    
def getData(url, period = __cachePeriod__):
        if __DEBUG__:
            print 'url --> ' + url
        if float(period) > 0:
            cachePath = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'pages', urllib.quote(url,"")))
            if (os.path.exists(cachePath) and (time.time()-os.path.getmtime(cachePath))/60/60 <= float(period)):
                f = open(cachePath, 'r')
                ret = f.read()
                f.close()
                return 'UTF-8',ret
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', __USERAGENT__)
            response = urllib2.urlopen(req)
            contentType = response.headers['content-type']
            data = response.read().replace("\n","").replace("\t","").replace("\r","")
            response.close()            
            
        except:
            if __DEBUG__:
                errno, errstr = sys.exc_info()[:2]
                print 'Error in getData: ' + str(errno) + ': ' + str(errstr)
            xbmc.log('Error in getData: Unable to save cache', xbmc.LOGERROR)
            return 'UTF-8','unavailable'
        return contentType, data
    
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
        for header in response.headers:
            name = response.headers[header]
            if __DEBUG__:
                print 'Cookie --> %s' % (name)
        data = response.read().replace("\n","").replace("\t","").replace("\r","")        
        response.close()
        return data, "ERROR"
        
def getEpisodeList(urlbase, inUrl, pattern, modulename, mode, patternFeatured='', patternmore='class="in_blk p_r"\sstyle=""\shref="(.*?)"'):
    ## get all the rest of the episodes
    contentType,mainPage = getData(inUrl)
    if patternFeatured != '':
        urls = re.compile(patternFeatured).findall(mainPage)
        urls += re.compile(pattern).findall(mainPage)
    else:
        urls = re.compile(pattern).findall(mainPage)
    ## for each episode we get the episode page to parse all the info from
    for path in urls:
        contentType,page = getData(urlbase + path + '/@@/video/flv_pl')
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
            url = 'rtmp://waflaWBE.walla.co.il/ app=vod/ swfvfy=true swfUrl=http://i.walla.co.il/w9/swf/video_swf/vod/walla_vod_player_adt.swf?95 tcurl=rtmp://waflaWBE.walla.co.il/vod/ pageurl=http://walla.co.il/ playpath=' + re.compile('<src>(.*?)</src>').findall(page)[0]
            addLink(contentType,title, url, iconImage, str(time), epiDetails)
    nextPage = re.compile(patternmore).findall(mainPage)
    if (len(nextPage)) > 0:
        addDir('UTF-8',__language__(30001), urlbase + nextPage[0], mode, 'DefaultFolder.png', modulename)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    
def clean(contentType, name):
    try:
        if contentType.find('UTF-8') == -1:
            name = name.decode("windows-1255")
    except:
        if __DEBUG__:
            print contentType
        errno, errstr = sys.exc_info()[:2]
        print 'Error in clean: ' + str(errno) + ': ' + str(errstr)
    return name.replace("&quot;","\"").replace("&#39;", "'").replace("&nbsp;", " ")