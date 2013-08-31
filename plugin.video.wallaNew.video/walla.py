# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from video.walla.co.il
"""
import urllib, re, xbmc, xbmcplugin, xbmcaddon, os, sys

##General vars
__plugin__ = "walla"
__author__ = "Shai Bentin"

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)

from common import *

def CATEGORIES():

    contentType, page = getData('http://vod.walla.co.il/')
    topMenuBloc = re.compile('<nav class="fc main-nav"(.*?)</nav>').findall(page)
    bottomGroupBloc = re.compile('<nav class="fc footer-logos".*?</nav>').findall(page)
    
    items = re.compile('<a href="(.*?)".*?<span>(.*?)</span>').findall(topMenuBloc[0])
    i = 0
    for url, title in items:
        if i >= 4: 
            break            
        module = '00000' + str(i)
        iconImage = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images', 'wallaBase', module + '.png'))
        if i!=0:
            addDir('UTF-8', title, 'http://vod.walla.co.il' + url, 1, iconImage, module)
        i=i+1
    
    bottomItems = re.compile('<td.*?<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(bottomGroupBloc[0])  
    for url, img, title in bottomItems:
        iconImage = getImage(img, 'wallaBase')
        if url.startswith('http'):
            elementId = re.compile("http://(.*?)\.").findall(url)
            addDir('UTF-8', title, url, 1, iconImage, elementId[0])     
        else :
            elementId = str(url)
            elementId= elementId[9:]
            s=elementId.find("/")
            elementId= elementId[:s]
            addDir('UTF-8', title, 'http://vod.walla.co.il' + url, 1, iconImage, elementId)
        
            
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

params = getParams(sys.argv[2])
url=None
name=None
mode=None
module=None
page=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        module=urllib.unquote_plus(params["module"])
except:
        pass
try:
        page=urllib.unquote_plus(params["page"])
except:
        pass
    
if mode==None or url==None or len(url)<1:
        CATEGORIES()

else:
        xbmc.log('in walla %s' % (module), xbmc.LOGDEBUG)
        manager = getattr(__import__('module_' + module.lower()), 'manager_' + module)()
        manager.work(mode, url, name, page)
        


xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
