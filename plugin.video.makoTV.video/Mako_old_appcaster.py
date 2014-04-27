# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from Mako VOD based on Android
    
    Copyright (c) 2010-2012 Shai Bentin.
    All rights reserved.  Unpublished -- rights reserved

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

"""
import urllib, urllib2, re, os, sys, unicodedata, random
import xbmcaddon, xbmc, xbmcplugin, xbmcgui

##General vars
__plugin__ = "Mako VOD"
__author__ = "Shai Bentin"

__settings__ = xbmcaddon.Addon(id='plugin.video.makoTV.video')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__DEBUG__       = __settings__.getSetting('DEBUG') == 'true'

LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'appCaster' ) )
M3U8_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'm3u8' ) )
sys.path.append (LIB_PATH)
sys.path.append (M3U8_PATH)

__properties = {'pKey':'81d42db7c211bf9615a895c504', 'accountId': '39', 'broadcasterId':'24', 'bundle':'com.keshet.mako.VODandroid', 'bucketId':'4fb10d943b35010c320041f4'}
import APCategoryLoader, APAccountLoader, APBroadcaster, APCategoryList, APItemLoader, APChannel, APChannelLoader
import APEpgLoader, APVodItem, APCategory, APExtensions


def getMainCategoryList():
    ## Get the account details
    ## account
    accountLoader = APAccountLoader.APAccountLoader(__properties)
    jsonAccountDictionary = accountLoader.loadURL()    
    if __DEBUG__:
        xbmc.log('accountURL --> %s' % (accountLoader.getQuery()), xbmc.LOGERROR)
    
    # get programs category
    rootCategoryId = ''
    try:
        extensionsStr = jsonAccountDictionary["account"]["extensions"]
        extensions = APExtensions.APExtensions(json.loads(extensionsStr, 'utf-8'))
	rootCategoryId = extensions.getProgramsCategoryId()
	if __DEBUG__:
	    xbmc.log('Programs category id --> %s' % rootCategoryId, xbmc.LOGERROR)
    except:
        pass
    
    if '' == rootCategoryId:
        ## broadcaster and main category from previous incarnation of the plugin
        broadcaster = APBroadcaster.APBroadcaster(__properties['broadcasterId'], jsonAccountDictionary["account"]["broadcasters"])
        if __DEBUG__:
            xbmc.log('Main Category --> %s' % (broadcaster.getRootCategory()), xbmc.LOGERROR)
        rootCategoryId = broadcaster.getRootCategory()
    
    # get the main categories list
    getCategory(rootCategoryId)


def getCategory(categoryId):
    # get the main categories list
    categoryLoader = APCategoryLoader.APCategoryLoader(__properties, categoryId)
    if __DEBUG__:
        xbmc.log('CategoryURL --> %s' % (categoryLoader.getQuery()), xbmc.LOGERROR)
    jsonCategoryDictionary = categoryLoader.loadURL()
    categories = APCategoryList.APCategoryList(jsonCategoryDictionary["category"])
    
    if (categories.hasSubCategories()):
        for category in categories.getSubCategories():
            if category.getId() not in ['36', '3103']: # omit the non video stuff
                addCategoryView(category)
    elif (categories.hasVideoitems()):
        for item in categories.getVodItems():
            addItemView(item)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmc.executebuiltin("Container.SetViewMode(504)")
            
def getItem(itemId):
    # get the item and load it's movie
    itemLoader = APItemLoader.APItemLoader(__properties, itemId)
    if __DEBUG__:
        xbmc.log('ItemURL --> %s' % (itemLoader.getQuery()), xbmc.LOGERROR)
    jsonItemDictionary = itemLoader.loadURL()
    item = APVodItem.APVodItem(jsonItemDictionary["vod_item"])
    playMovie(item)
    
          
def addCategoryView(category):
    if __DEBUG__:        
        xbmc.log('category --> %s' % (category.getId()), xbmc.LOGERROR)
    _url = sys.argv[0] + "?category=" + category.getId()    

    title = category.getTitle().encode('UTF-8')
    summary = category.getDescription().encode('UTF-8')
    thumbnail = category.getThumbnail()
    fanart = category.getFanartImage()
    
    liz = xbmcgui.ListItem(title, iconImage = thumbnail, thumbnailImage = thumbnail)
    liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(title), "Plot": urllib.unquote(summary)})
    if not fanart == '':
        liz.setProperty("Fanart_Image", fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=_url, listitem=liz, isFolder=True)

def addItemView(item):
    if __DEBUG__:
        xbmc.log('item --> %s' % (item.getId()), xbmc.LOGERROR)
    _url = sys.argv[0] + "?item=" + item.getId()    

    title = item.getTitle().encode('UTF-8')
    summary = item.getDescription().encode('UTF-8')
    thumbnail = item.getThumbnail()
    
    listItem = xbmcgui.ListItem(title, iconImage = thumbnail, thumbnailImage = thumbnail)
    listItem.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(title), "Plot": urllib.unquote(summary)})
    listItem.setProperty("Fanart_Image", thumbnail)
    listItem.setProperty('IsPlayable', 'true')
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=_url, listitem=listItem, isFolder=False)

def playMovie(item):
    _url = item.getStreamUrl()
    _hls_cookie = item.getHLSCookie()
    if __DEBUG__:
        xbmc.log('vod_item --> %s' % (item.getId()), xbmc.LOGERROR)
        xbmc.log('playable _url --> %s' % (_url), xbmc.LOGERROR)
    
    title = item.getTitle().encode('UTF-8')
    summary = item.getDescription().encode('UTF-8')
    thumbnail = item.getThumbnail()
    
    # falsify a user agent
    _user_agent = '|User-Agent=' + urllib.quote_plus('stagefright/1.2 (Linux; Android 4.2.2)')
    _dummyHeader = '&Accept-Language=en-US'

    # add a specific cookie, if needed (not normally)
    _cookie = ''
    if '' != _hls_cookie:
        _cookie = '&Cookie=' + urllib.quote_plus(_hls_cookie)

    listItem = xbmcgui.ListItem(title, iconImage = thumbnail, thumbnailImage = thumbnail, path=_url + _user_agent + _dummyHeader)
    listItem.setInfo(type='Video', infoLabels={ "Title": urllib.unquote(title), "Plot": urllib.unquote(summary)})
    listItem.setProperty('IsPlayable', 'true')

    # Gotham properly probes the mime type now, no need to do anything special
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

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

# manage a random deviceId (if not already saved)
deviceId = __settings__.getSetting(id = 'deviceId')
if None == deviceId or '' == deviceId:
    rand1 = int((random.random() * 8999) + 1000)
    rand2 = int((random.random() * 89) + 10)
    deviceId = '1d' + str(rand1) + 'd3b4f71c' + str(rand2)
    
    __settings__.setSetting(id = 'deviceId', value = deviceId)

__properties['deviceId'] = deviceId
if __DEBUG__:
    xbmc.log('deviceId --> %s' % (__properties['deviceId']), xbmc.LOGERROR)


# if we dont have a unique user ID and token yet, make it so
uuid = __settings__.getSetting(id = 'UUID')
token = __settings__.getSetting(id = 'deviceAuthToken')
if __DEBUG__:
    xbmc.log('UUID from settings --> %s, auth token from settings --> %s', uuid, token, xbmc.LOGERROR)
if None == uuid or '' == uuid:
    accountLoader = APAccountLoader.APAccountLoader(__properties)
    uuidDict = accountLoader.loadURL()
    id = uuidDict['id']
    token = uuidDict['token']
    if None != id and '' != id:
        __settings__.setSetting(id = 'UUID', value = id)
    if None != token and '' != token:
        __settings__.setSetting(id = 'deviceAuthToken', value = token)

__properties['UUID'] = uuid
__properties['deviceAuthToken'] = token
if __DEBUG__:
    xbmc.log('final UUID --> %s, final auth token --> %s', uuid, token, xbmc.LOGERROR)

params = getParams(sys.argv[2])
categoryId = None
itemId = None

try:
    categoryId=urllib.unquote_plus(params["category"])
except:
    pass
try:
    itemId=urllib.unquote_plus(params["item"])
except:
    pass

if None == categoryId and None == itemId:
    getMainCategoryList()
elif None != categoryId:
    getCategory(categoryId)
elif None != itemId:
    getItem(itemId)
            
xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__, "fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
