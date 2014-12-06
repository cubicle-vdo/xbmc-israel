# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from video.walla.co.il
"""
import urllib, re, xbmc, xbmcplugin, xbmcaddon, os, sys
import repoCheck

##General vars
__plugin__ = "walla"
__author__ = "shlomicthailand"

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__DEBUG__ = __settings__.getSetting("DEBUG") == "true"
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)

from wallacommon import *

print "WALLA Main got URL=" + sys.argv[2]

def CATEGORIES():
	repoCheck.UpdateRepo()
	addDir('UTF-8', "ילדים", 'englishName=kids', 1, elementId='wallavod')
	addDir('UTF-8', "סדרות", 'englishName=tvshows', 1, elementId='wallavod')
	addDir('UTF-8', "סרטים", 'englishName=movies', 1, elementId='wallavod')
	addDir('UTF-8', "תחזוקה - מחיקת זיכרון מטמון", 'englishName=maintenance', 0, elementId='wallavod',isRealFolder=False)
	
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

	
params = getParams(sys.argv[2])
url=None
name=None
mode=None
module=None
page=None

try:
	url=urllib.unquote_plus(params["url"])
	print "WALLA main script url=" + url 
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
	print "WALLA main script name=" + name
except:
	pass
try:
	mode=int(params["mode"])
	print "WALLA main script mode=" + str(mode)
except:
	pass
try:
	module=urllib.unquote_plus(params["module"])
	print "WALLA main script module=" + module
except:
	pass
try:
	page=urllib.unquote_plus(params["page"])
except:
	pass
	
if mode==None or url==None or len(url)<1:
	CATEGORIES()
elif mode==0:
	cleanCache()
	
else:
	xbmc.log('in walla %s' % (module), xbmc.LOGDEBUG)
	
	moduleScript = __import__('module_' + module.lower())
	print "WALLA after moduleScript module:" + module 
	className = 'manager_' + module
	print moduleScript
	if hasattr(moduleScript,className ):
		print "WALLA found attr "
	try:
		manager = getattr(moduleScript, className)()
	except Exception as e:
		print "WALLA got exception"
		print e
		raise e
	   
	manager.work(mode, url, name, page)

xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
