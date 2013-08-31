# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from yes.walla.co.il
"""
import urllib, re, xbmc, xbmcplugin, xbmcaddon, os, sys

##General vars
__plugin__ = "wallaYes"
__author__ = "Shai Bentin"

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaYes.video')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)

from common import *

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
        mode = 1


manager = getattr(__import__('module_yes'), 'manager_yes')()
manager.work(mode, url, name, page)

xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
