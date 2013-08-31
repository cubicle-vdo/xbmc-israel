'''
Created on 23/06/2011

@author: shai
'''
import re, urllib, os, sys, xbmcaddon, xbmcgui, xbmc, xbmcplugin
import common

__BASE_URL__ = 'http://dor.walla.co.il/'
__NAME__ = 'dor'

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__language__ = __settings__.getLocalizedString
__PATTERN__ = '<div class="right navRowItem"><div><a href="(.*?)@vod">'
__PATTERN_MORE__ = 'class="p_r" style="".*?href="(.*?)"'

class manager_dor:
    
    def __init__(self):
        self.MODES = common.enum(GET_CONTENT=1, GET_VOD=2, GET_LIVE=3, GET_EPISODES_LIST=4, GET_CAMERAS=5, PLAY_VIDEO=6)
        
    def work(self, mode, url='', name='', page=''):
        if(mode==self.MODES.GET_CONTENT):
            self.getContent()
        elif (mode==self.MODES.GET_VOD):
            self.getVod(url)
        elif (mode==self.MODES.GET_LIVE):
            self.getLive(url)
        elif(mode==self.MODES.GET_EPISODES_LIST):
            common.getEpisodeList(__BASE_URL__, url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST, '', __PATTERN_MORE__)
        elif(mode==self.MODES.PLAY_VIDEO):
            self.playLive(url, name)
            
    def getContent(self):
        ## Add the VOD item
        common.addDir('UTF-8',__language__(40006), __BASE_URL__ + "?w=/@vod", self.MODES.GET_VOD, "DefaultFolder.png", __NAME__)
        common.addDir('UTF-8',__language__(40007), __BASE_URL__ + "?w=/@live", self.MODES.GET_LIVE, "DefaultFolder.png", __NAME__)
    
    def getVod(self, url):
        contentType,page = common.getData(url)
        features = re.findall('<div class="topNav">(.*?)</div><span class="wcflow"', page)
        if features and len(features) > 0:
            menu = re.findall('href="(.*?)">(.*?)<', features[0])
            for href, name in menu:
                common.addDir(contentType,name, __BASE_URL__ + href, self.MODES.GET_EPISODES_LIST, "DefaultFolder.png", __NAME__)
                
    def getLive(self, url):
        contentType,page = common.getData(url)
        cameras = re.findall('id="camera_div_(\d)" rel="(.*?)"><img src="(.*?)"', page)
        for camId, cameraName, image in cameras:
            href = 'rtmp://waflalive.walla.co.il/livestreamcast_edge?tuid=undefined&un=undefined&ait=undefined&wkeys=undefined&divname=undefined&provider=undefined&location=undefined&channel_name=undefined playpath=s_feedvilla' + camId + ' live=true swfUrl=http://i.walla.co.il/w9/swf/video_swf/live/streamcast_nextGen.swf?10 pageUrl=http://dor.walla.co.il/?w=/@live'
            common.addVideoLink(contentType,cameraName, href, self.MODES.PLAY_VIDEO, image, __NAME__)
            
    def getEpisodeList(self, url):
        contentType,page = common.getData(url)
        episodes = re.findall('<div class="right navRowItem"><div><a href="(.*?)@vod"><img src="(.*?)".*?vod">(.*?)<.*?vod">(.*?)<', page)
        for href, img, name, summary in episodes:
            common.addVideoLink(contentType,name, href, self.MODES.PLAY_VIDEO, img, __NAME__, summary)
        
    def playLive(self, url, name):
        iconImage = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images', 'wallaBase', '0000004.jpg'))
        listItem = xbmcgui.ListItem(name, iconImage=iconImage, thumbnailImage=iconImage, path=url)# + '|' + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        listItem.setInfo(type='Video', infoLabels={ "Title": urllib.unquote(name), "Plot": 'live streaming'})
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
        