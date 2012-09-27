# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from www.ynet.co.il
"""
import urllib, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui

##General vars
__plugin__ = "Ynet Video"
__author__ = "Cubicle"

__image_path__ = ''
__settings__ = xbmcaddon.Addon(id='plugin.video.ynet.video')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)

from common import *

def GENRES():
    #addDir('סרטים','http://www.ynet.co.il/home/0,7340,L-10154,00.html', 1, 'http://www.ynet.co.il/PicServer3/2012/07/30/4070286/koteret.png')
    page = getData('http://www.ynet.co.il/home/0,7340,L-4232,00.html')
    matches = re.compile('<a href="javascript:openInnewWindow\(\'(.*?)\',.*?,.*?,.*?\)" ;><img src=\'(.*?)\' border=0  alt=\'(.*?)\'  title=\'').findall(page)
    if len(matches) > 0:
        for match in matches:
            action = urllib.unquote(match[0])
            is_ynet = re.compile('www.ynet.co.il').findall(action)
            if ( len(is_ynet ) > 0 ):
                name = match[2]
                icon = match[1]
                addDir(name, action,1, icon)
    xbmc.executebuiltin("Container.SetViewMode(500)")# see the image view
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            
def SERIES(url):
    page = getData(url)
    # receive the block of shows that are a part of this genre
    mainUrl = re.compile('AjaxItemsUrl:"(.+?)videoId').findall(page)
    ajax_items_url = mainUrl[0]
    match_url = getMatches(url,'/Ext/Comp/Video/topVideoPlayer/CdaTopVideoPlayer_VidItems/(.*?),toReplace-(.*?).htm')
    if len(match_url) > 0:
        url_m = match_url[0]
        page_id = url_m[0]
        ses_id = url_m[1]
        matches = getMatches(url, 'group_id=\'.*?\' videos_list=\'(.*?)\'><div class=\'tvp_.*?\'>(.*?)</div></a></li>')
        if len(matches) > 0:
            for match in matches:
                videos_list=match[0]
                name=match[1].replace('&quot;','"')
                addDir(name, 'http://www.ynet.co.il/Ext/Comp/Video/topVideoPlayer/CdaTopVideoPlayer_VidItems/' + page_id + ',' + videos_list + '-' + ses_id + '.htm', '2&ynet_ajax_items_url=' + ajax_items_url, '')
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    xbmc.executebuiltin("Container.SetViewMode(500)")# see the image view

def SHOWING_NOW(url):
    page = getData('http://hot.ynet.co.il/')
    shows = re.compile('<tr height=25px>.*?<a href=\'(.*?)\'.*?>(.*?)</a>').findall(page)
    for href, title in shows:
        title = title.replace('&nbsp;', ' ').replace('&quat;', '"').replace('&#39;', '\'')
        seriesId = re.compile('L-(\d+),').findall(href)[0]
        iconImage = __image_path__ + 'hot/series/series_' + seriesId + '.jpg'
        if not os.path.exists(iconImage):
            iconImage = 'DefaultFolder.png'
        addDir(title, 'http://hot.ynet.co.il' + href, 2, iconImage)
        
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    xbmc.executebuiltin("Container.SetViewMode(500)")# see the image view
            
def EPISODES(url, mainUrl):
    ajax_items_url=params["ynet_ajax_items_url"]
    page = getData(url)
    sections = re.compile('<li vidid=\'(.*?)\' artid=\'(.*?)\' chanid=\'(.*?)\'>.*?<img src=\'(.*?)\'.*?tvp_video_title_text\'>(.*?)</span>').findall(page)
    if len(sections) > 0:
        for item in sections:
            vidid = item[0]
            artid = item[1]
            chanid = item[2]
            image = item[3]
            title = item[4]
            addVideoLink(title, 'http://www.ynet.co.il' + ajax_items_url + vidid + '-' + artid + '-' + 'VideoChannel,00.html', '4', 'http://www.ynet.co.il' + image, '')
        
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmc.executebuiltin("Container.SetViewMode(500)")# see the image view
        
def PLAY_MOVIE(url, name):    
    page = getData(url, 0) 
    videoUrl = re.compile('"path":"(.+?)"').findall(page)
    if len(videoUrl) > 0:
        videoPlayListUrl = urllib.unquote(videoUrl[0])
        listItem = xbmcgui.ListItem(name, 'DefaultFolder.png', 'DefaultFolder.png', path=videoPlayListUrl) # + '|' + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        listItem.setInfo(type='Video', infoLabels={ "Title": urllib.unquote(name)})
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
 
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
    GENRES()

elif mode==1:
    SERIES(url)

elif mode==2:
    EPISODES(url, url)

elif mode==3:
    EPISODES(url, module)

elif mode==4:
    PLAY_MOVIE(url, name)

elif mode==5:
    SHOWING_NOW(url)   
          
else:
    GENRES()

xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
