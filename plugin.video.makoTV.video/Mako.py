# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content like MakoTV 3 Android app
    
    Copyright (c) 2014 derived from original work by Shai Bentin.

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

"""
import urllib, urllib2, re, os, sys, unicodedata, random
import xbmcaddon, xbmc, xbmcplugin, xbmcgui

##General vars
__plugin__ = "MakoTV 3"
__author__ = "Shai Bentin"

__settings__ = xbmcaddon.Addon(id='plugin.video.makoTV.video')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__DEBUG__       = __settings__.getSetting('DEBUG') == 'true'

LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'makoStore' ) )
M3U8_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'm3u8' ) )
sys.path.append (LIB_PATH)
sys.path.append (M3U8_PATH)


import MakoVodIndexLoader, MakoProgramNode, MakoProgramLoader, MakoSeasonNode, MakoSeasonLoader, MakoVodItemLoader, MakoVodItemNode
import MakoTicketLoader
import repoCheck

# define properties dictionary to be delivered down the hierarchy
__properties = { 'consumer':'android4', 'appId':'0c4f6ec6-9194-450e-a963-e524bb6404g2', 'appVer':'3.0.3' }

def getProgramsIndex():
    # obtain VOD index
    repoCheck.UpdateRepo()
    indexLoader = MakoVodIndexLoader.MakoVodIndexLoader(__properties)
    jsonProgramsIndex = indexLoader.loadURL()
    if None == jsonProgramsIndex:
        xbmc.log('Nothing returned from mako-vod-index', xbmc.LOGERROR)

    # find all programs section
    try:
        allPrograms = jsonProgramsIndex['root']['allPrograms']
    except:
        xbmc.log('Couldnt locate allPrograms in main index', xbmc.LOGERROR)
	pass

    # create programs
    for prog in allPrograms:
        programNode = MakoProgramNode.MakoProgramNode(prog)
	addProgramView(programNode)

def addProgramView(programNode):
    _url = sys.argv[0] + "?program=" + urllib.quote_plus(programNode.getProgramURL())
    title = programNode.getTitle().encode('UTF-8')
    summary = programNode.getDescription().encode('UTF-8')
    thumbnail = programNode.getThumbnailURL()
    fanart = ''

    #xbmc.log('***** Mako: adding program %s' % title, xbmc.LOGDEBUG)
    
    liz = xbmcgui.ListItem(title, iconImage = thumbnail, thumbnailImage = thumbnail)
    liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(title), "Plot": urllib.unquote(summary)})
    if not fanart == '':
        liz.setProperty("Fanart_Image", fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=_url, listitem=liz, isFolder=True)

def getProgram(programURL):
    # obtain program seasons and items
    progLoader = MakoProgramLoader.MakoProgramLoader(__properties, programURL)
    xbmc.log('***** Mako: loading data for program URL=%s' % (progLoader.getQuery()), xbmc.LOGDEBUG)
    programDict = progLoader.loadURL()
    if None == programDict:
        xbmc.log('Couldt retrieve json data for program, URL=%s' % (progLoader.getQuery()), xbmc.LOGERROR)
    
    # find seasons, the loader already removed the root element
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
    seasons = programDict['programData']['seasons']
    for season in seasons:
        seasonNode = MakoSeasonNode.MakoSeasonNode(season)
        addSeasonView(seasonNode)

def addSeasonView(seasonNode):
    _url = sys.argv[0] + "?season=" + urllib.quote_plus(seasonNode.getSeasonURL()) + "&seasonId=" + urllib.quote_plus(seasonNode.getGUID())
    title = seasonNode.getTitle().encode('UTF-8')
    summary = seasonNode.getDescription().encode('UTF-8')
    thumbnail = ''

    #xbmc.log('***** Mako: adding season %s' % title, xbmc.LOGDEBUG)

    liz = xbmcgui.ListItem(title, iconImage = thumbnail, thumbnailImage = thumbnail)
    liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(title), "Plot": urllib.unquote(summary)})
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=_url, listitem=liz, isFolder=True)

def getSeason(seasonURL, seasonId):
    # obtain the same page as before but parse the wanted season
    seasonLoader = MakoSeasonLoader.MakoSeasonLoader(__properties, seasonURL, seasonId)
    seasonDict = seasonLoader.loadURL()
    if 'vods' not in seasonDict:
        xbmc.log('***** Mako: didnt find vods in season dict for season with id %s' % (seasonId), xbmc.LOGERROR)
    else:
        # get the vod items and create them
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
	progress = xbmcgui.DialogProgress()
	progress.create('Mako TV', 'Loading VOD items...')
	vodItems = seasonDict['vods']
	step = int(100 / len(vodItems))
	perc = 0
	for vodItem in vodItems:
	    if progress.iscanceled():
	        break
	    # load each item URL since we want all the data available before play
	    url = vodItem['link']
	    xbmc.log('***** Mako: loading vod item page: %s' % (url), xbmc.LOGDEBUG)
	    itemLoader = MakoVodItemLoader.MakoVodItemLoader(__properties, url)
	    vodItemDict = itemLoader.loadURL()
	    vodItemNode = MakoVodItemNode.MakoVodItemNode(vodItemDict)
	    addVodItemView(vodItemNode)
	    perc = perc + step
	    progress.update(perc, 'Mako TV', 'Loading VOD items...')
	progress.close

def addVodItemView(vodItemNode):
    # craft the URL to the video
    _url = sys.argv[0] + "?vodItem=" + urllib.quote_plus(vodItemNode.getDirectVideoUrl()) + "&vodItemId=" + urllib.quote_plus(vodItemNode.getGUID())
    title = vodItemNode.getTitle().encode('UTF-8')
    summary = vodItemNode.getDescription().encode('UTF-8')
    thumbnail = vodItemNode.getThumbnailURL()

    #xbmc.log('***** Mako: adding vod item with URL: %s' % (_url), xbmc.LOGDEBUG)
    listItem = xbmcgui.ListItem(title, iconImage = thumbnail, thumbnailImage = thumbnail)
    listItem.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(title), "Plot": urllib.unquote(summary)})
    listItem.setProperty("Fanart_Image", thumbnail)
    listItem.setProperty('IsPlayable', 'true')
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=_url, listitem=listItem, isFolder=False)

def playItem(vodItemURL, vodItemId):
    # obtain a ticket for the video item
    ticketLoader = MakoTicketLoader.MakoTicketLoader(__properties, vodItemURL, vodItemId)
    ticketLoader.loadURL()
    urlEncodedTicket = ticketLoader.getTicket()
    if urlEncodedTicket == '':
        xbmc.log('***** Mako: unable to find ticket for vod item %s' % vodItemURL, xbmc.LOGERROR)
    else:
        # create final URL
	_url = vodItemURL
	if _url.find('?') == -1:
	    _url = _url + '?' + urlEncodedTicket
	else:
	    _url = _url + '&' + urlEncodedTicket
	xbmc.log('***** Mako: final video URL with ticket: %s' % _url, xbmc.LOGDEBUG)
	title = ''
	summary = ''
	thumbnail = ''

        # falsify a user agent
        _user_agent = '|User-Agent=' + urllib.quote_plus('stagefright/1.2 (Linux; Android 4.2.2)')
        _acceptHeader = '&Accept-Language=en-US'

        listItem = xbmcgui.ListItem(title, iconImage = thumbnail, thumbnailImage = thumbnail, path=_url + _user_agent + _acceptHeader)
        listItem.setInfo(type='Video', infoLabels={ "Title": urllib.unquote(title), "Plot": urllib.unquote(summary)})
        listItem.setProperty('IsPlayable', 'true')

        # Gotham properly probes the mime type
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


# manage a random deviceId (if not already saved) of 15 hex digits.
deviceId = __settings__.getSetting(id = 'deviceId')

# if we encounter a previous incarnation of the add-on, clear and do it again
if None != deviceId and len(deviceId) == 16:
    deviceId = ''
    __settings__.setSetting(id = 'deviceId', value = deviceId)

if None == deviceId or '' == deviceId:
    rand1 = int((random.random() * 8999) + 1000)
    rand2 = int((random.random() * 89) + 10)
    deviceId = 'd' + str(rand1) + 'd6af98ce' + str(rand2)
    
    __settings__.setSetting(id = 'deviceId', value = deviceId)

__properties['deviceId'] = deviceId
xbmc.log('***** Mako: deviceId = %s' % (__properties['deviceId']), xbmc.LOGDEBUG)

# reset old settings, if exist. make a simple UDID out of the unique android ID
__settings__.setSetting(id = 'UUID', value = '')
__settings__.setSetting(id = 'deviceAuthToken', value = '')
udid = 'A1800000000' + deviceId
__properties['UDID'] = udid
xbmc.log('***** Mako: UDID = %s' % (__properties['UDID']), xbmc.LOGDEBUG)

params = getParams(sys.argv[2])
programURL = None
seasonURL = None
seasonId = None
vodItemURL = None
vodItemId = None

# attempt to get program URL
if 'program' in params:
    programURL = urllib.unquote_plus(params["program"])

# attempt to get season URL
if 'season' in params:
    seasonURL = urllib.unquote_plus(params["season"])
    seasonId = urllib.unquote_plus(params["seasonId"])

# attempt to get vodItem URL
if 'vodItem' in params:
    vodItemURL = urllib.unquote_plus(params["vodItem"])
    vodItemId = urllib.unquote_plus(params["vodItemId"])

if None == programURL and None == seasonURL and None == vodItemURL:
    getProgramsIndex()
elif None != programURL:
    getProgram(programURL)
elif None != seasonURL:
    getSeason(seasonURL, seasonId)
elif None != vodItemURL:
    playItem(vodItemURL, vodItemId)
            
xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__, "fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
