# -*- coding: utf-8 -*-
'''
Created on 01/05/2011

@author: shai
'''

import urllib,urllib2,re,xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcaddon,os,sys
import common

__BASE_URL__ = 'http://mtv.walla.co.il'
__NAME__ = 'mtv'
__CLIP_DATA__ = 'http://intl.esperanto.mtvi.com/www/xml/media/mediaGen.jhtml?uri=mgid:uma:video:mtv.co.il:'
__PATTERN_MORE__ = 'class="p_r"\sstyle=""\shref="(.*?)"'
__PATTERN_FEATURED__ = ''

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')

class manager_mtv:
    
    def __init__(self):
        self.MODES = common.enum(GET_CATEGORIES=1, GET_SERIES_LIST=2, GET_EPISODES_LIST=3, PLAY_ITEM=4)

    def work(self, mode, url='', name='', page='0'):
        if (mode==self.MODES.GET_CATEGORIES):
            self.getCategories()
        elif (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList(url)
        elif(mode==self.MODES.GET_EPISODES_LIST):
            self.getEpisodeList(url)
        elif(mode==self.MODES.PLAY_ITEM):
            self.play_video(url, name)
            
    def getCategories(self):
        categories = [['/news/new-music/',40001,self.MODES.GET_EPISODES_LIST], 
                      ['/music/mtv-playlist/',40002,self.MODES.GET_SERIES_LIST],
                      ['/charts/',40003,self.MODES.GET_SERIES_LIST],
                      ['/shows/browse/',40004,self.MODES.GET_SERIES_LIST],
                      ['/music/live-session/',40005,self.MODES.GET_EPISODES_LIST]]
        for item in categories:
            title = common.__language__(item[1])
            url = item[0]
            mode = item[2]
            iconImage = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'resources', 'images', 'icon_' + str(item[1]) + '.png'))
            if not os.path.exists(iconImage):
                iconImage = 'DefaultFolder.png'
            fanart = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'resources', 'bg', 'fanart_' + str(item[1]) + '.png'))
            if not os.path.exists(fanart):
                fanart = 'DefaultFolder.png'
            common.addDir('UTF-8',title, __BASE_URL__ + url, mode, iconImage, __NAME__, '', fanart)   
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        
    def getSeriesList(self, url):
        contentType,page = common.getData(url)
        if url.find('page') == -1:
            featured = re.compile('<a class="thumblink" href="(.+?)".*?src="(.+?)".*?alt="(.+?)"').findall(page)
            for url, image, title in featured:
                title = title.replace('<br/>', ' - ')
                title = title.replace('|', ' - ')
                common.addDir(contentType,title, url, self.MODES.GET_EPISODES_LIST, image, __NAME__)
    
        items = re.compile('<div class="entry-content-inside">.*?<a href="(.+?)" title="(.*?)".*?src="(.+?)"').findall(page)
        for url, title, image in items:                
            if url.find('article') == -1:
                title = title.replace('<br/>', ' - ')
                title = title.replace('|', ' - ')
                common.addDir(contentType,title, url, self.MODES.GET_EPISODES_LIST, image, __NAME__)
    
        hasNext = re.compile('class=\'next page-numbers\' href=\'(.+?)\'').findall(page)
        if not hasNext == None and len(hasNext) > 0:
            # there is a next page
            url = hasNext[0]
            common.addDir('UTF-8',common.__language__(30001), url, self.MODES.GET_SERIES_LIST, 'DefaultFolder.png', __NAME__)
        
    def getEpisodeList(self, url):
        contentType,page = common.getData(url)
        if url.find('page') == -1:
            featured = re.compile('<a class="thumblink" href="(.+?)".*?src="(.+?)".*?alt="(.+?)"').findall(page)
            for url, image, title in featured:
                title = title.replace('<br/>', ' - ')
                title = title.replace('|', ' - ')
                common.addVideoLink(contentType,title, url, self.MODES.PLAY_ITEM, image, __NAME__)

        items = re.compile('<div class="entry-content-inside">.*?<a href="(.+?)" title="(.*?)".*?src="(.+?)"').findall(page)
        for url, title, image in items:                
            if url.find('article') == -1:
                title = title.replace('<br/>', ' - ')
                title = title.replace('|', ' - ')
                common.addVideoLink(contentType,title, url, self.MODES.PLAY_ITEM, image, __NAME__)

        hasNext = re.compile('class=\'next page-numbers\' href=\'(.+?)\'').findall(page)
        if not hasNext == None and len(hasNext) > 0:
            # there is a next page
            url = hasNext[0]
            common.addDir('UTF-8',common.__language__(30001), url, self.MODES.GET_EPISODES_LIST, 'DefaultFolder.png', __NAME__)
            
    def play_video(self, url, name):
        contentType,page = common.getData(url)
        videoId = re.compile('<embed.*?src=".+?(\d+)"').findall(page)
        if len(videoId) > 0:
            contentType,movieData = common.getData(__CLIP_DATA__ + videoId[0], 0)
            videoUrl = re.compile('<src>(.+?)</src>').findall(movieData)
            length = len(videoUrl)
            if length > 0:
                playUrl = videoUrl[0] + ' swfurl=http://intl.esperanto.mtvi.com/player/js/swfobject_2_2/expressInstall.swf swfvfy=true'#.replace('rtmpe', 'rtmp')
                listItem = xbmcgui.ListItem(name, 'DefaultFolder.png', 'DefaultFolder.png', path=playUrl) # + '|' + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                listItem.setInfo(type='Video', infoLabels={ "Title": urllib.unquote(name)})
                listItem.setProperty('IsPlayable', 'true')
                xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
            
        
## http://intl.esperanto.mtvi.com/www/xml/media/mediaGen.jhtml?uri=mgid:uma:video:mtv.co.il:648596