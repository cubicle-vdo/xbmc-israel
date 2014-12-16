# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from Channel 10 VOD based on Android
    
    Copyright (c) 2010-2014 Shai Bentin + vmaster
    All rights reserved.  Unpublished -- rights reserved

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

"""
import urllib, urllib2, re, os, sys, unicodedata, random, json
import xbmcaddon, xbmc, xbmcplugin, xbmcgui

##General vars
__plugin__ = "il ten"
__author__ = "vmaster"

__settings__ = xbmcaddon.Addon(id='plugin.video.ilten')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__DEBUG__       = __settings__.getSetting('DEBUG') == 'true'

LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'appCaster' ) )
M3U8_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'm3u8' ) )
sys.path.append (LIB_PATH)
sys.path.append (M3U8_PATH)

__properties = {'pKey':'b52501f01699218ca6f6df33c1', 'accountId': '69', 'broadcasterId':'67', 'bundle':'com.applicaster.il.ten', 'bucketId':'4f93d55c37d0d521ad000034'}
import APCategoryLoader, APAccountLoader, APBroadcaster, APCategoryList, APItemLoader, APChannel, APChannelLoader
import APEpgLoader, APVodItem, APCategory, APExtensions, APItemListsLoader, APItemLists


def getMainCategoryList():
    ## Get the account details
    ## account
    accountLoader = APAccountLoader.APAccountLoader(__properties)
    jsonAccountDictionary = accountLoader.loadURL()
    xbmc.log('***** accountURL --> %s' % (accountLoader.getQuery()), xbmc.LOGDEBUG)
    
    # get programs category
    rootCategoryId = ''
    try:
        broadcasterDict = jsonAccountDictionary["account"]["broadcasters"][0]
	if 'broadcaster' in broadcasterDict:
	    broadcasterDict = broadcasterDict['broadcaster']
        extensions = APExtensions.APExtensions(broadcasterDict)
	rootCategoryId = extensions.getProgramsCategoryId()
	xbmc.log('***** Programs category id --> %s' % rootCategoryId, xbmc.LOGDEBUG)
    except:
        xbmc.log('***** Couldnt obtain main content category ID', xbmc.LOGERROR)
        pass
    
    if None != rootCategoryId and '' != rootCategoryId:
        # get the main categories list
        getCategory(rootCategoryId)

	# obtain item lists and attempt to load each one to search for special programs
	itemList = extensions.getItemLists()
	for itemId in itemList:
	    # obtain an item_list. we are interested in promoted shows
	    xbmc.log('***** Retrieving item_list with ID %s' % itemId, xbmc.LOGDEBUG)
	    itemListsLoader = APItemListsLoader.APItemListsLoader(__properties, itemId)
	    itemListsDict = itemListsLoader.loadURL()

	    # make sure its a valid item_lists with actual shows
	    if itemListsDict != None:
	        apItemLists = APItemLists.APItemLists(itemListsDict['item_list'])
		if apItemLists.isValid():
		    # now we can expand the category list
		    itemCategories = apItemLists.getCategoryList()
		    if (itemCategories.hasSubCategories()):
		        for itemCat in itemCategories.getSubCategories():
			    addCategoryView(itemCat)
	    else:
	        xbmc.log('***** Couldnt load item_lists for ID %s' % itemId, xbmc.LOGERROR)

    else:
        xbmc.log('***** Cannot obtain programs category ID, sorry...', xbmc.LOGERROR)

def getCategory(categoryId):
    # get the main categories list
    categoryLoader = APCategoryLoader.APCategoryLoader(__properties, str(categoryId))
    xbmc.log('***** CategoryURL --> %s' % (categoryLoader.getQuery()), xbmc.LOGDEBUG)
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
    xbmc.log('***** ItemURL --> %s' % (itemLoader.getQuery()), xbmc.LOGDEBUG)
    jsonItemDictionary = itemLoader.loadURL()
    item = APVodItem.APVodItem(jsonItemDictionary["vod_item"])
    playMovie(item)
    
          
def addCategoryView(category):

    xbmc.log('***** category --> %s' % (category.getId()), xbmc.LOGDEBUG)
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

    xbmc.log('***** item --> %s' % (item.getId()), xbmc.LOGDEBUG)
    _url = sys.argv[0] + "?item=" + item.getId()    

    title = item.getTitle().encode('UTF-8')
    summary = item.getDescription().encode('UTF-8')
    thumbnail = item.getThumbnail()
    season = item.getSeasonName()
    if season == None:
        season = ''
    airdate = item.getAirDate()
    if airdate == None:
        airdate = ''
    
    listItem = xbmcgui.ListItem(title, iconImage = thumbnail, thumbnailImage = thumbnail)
    listItem.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(title), "Plot": urllib.unquote(summary), "Season": urllib.unquote(season), "Aired": urllib.unquote(airdate)})
    listItem.setProperty("Fanart_Image", thumbnail)
    listItem.setProperty('IsPlayable', 'true')
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=_url, listitem=listItem, isFolder=False)

def playMovie(item):    
    _url = item.getStreamUrl()
    _hls_cookie = item.getHLSCookie()
    xbmc.log('***** vod_item --> %s' % (item.getId()), xbmc.LOGDEBUG)
    xbmc.log('***** playable _url --> %s' % (_url), xbmc.LOGDEBUG)
    
    title = item.getTitle().encode('UTF-8')
    summary = item.getDescription().encode('UTF-8')
    thumbnail = item.getThumbnail()
    
    # falsify a user agent
    _user_agent = '|User-Agent=' + urllib.quote_plus('%D7%A8%D7%A9%D7%AA/24.8.11.46 CFNetwork/672.0.2')
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
    rand2 = int((random.random() * 8999) + 1000)
    rand3 = int((random.random() * 8999) + 1000)

    deviceId = 'd12' + str(rand1) + str(rand2) + str(rand3) 
    
    __settings__.setSetting(id = 'deviceId', value = deviceId)

__properties['deviceId'] = deviceId
xbmc.log('***** deviceId --> %s' % (__properties['deviceId']), xbmc.LOGDEBUG)


# if we dont have a unique user ID and token yet, make it so
uuid = __settings__.getSetting(id = 'UUID')
token = __settings__.getSetting(id = 'deviceAuthToken')

xbmc.log('***** UUID from settings --> %s, auth token from settings --> %s' % (uuid, token), xbmc.LOGDEBUG)
if None == uuid or '' == uuid:
    accountLoader = APAccountLoader.APAccountLoader(__properties)
    uuidDict = accountLoader.loadURL()
    uuid = uuidDict['id']
    token = uuidDict['token']
    if None != id and '' != id:
        __settings__.setSetting(id = 'UUID', value = uuid)
    if None != token and '' != token:
        __settings__.setSetting(id = 'deviceAuthToken', value = token)

__properties['UUID'] = uuid
__properties['deviceAuthToken'] = token

xbmc.log('***** final UUID --> %s, final auth token --> %s' % (uuid, token), xbmc.LOGDEBUG)

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
xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)