# -*- coding: utf-8 -*-

'''
Created on 02/05/2011
The good life channel
@author: shai
'''

import xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__language__ = __settings__.getLocalizedString
__BASE_URL__ = 'http://vod.walla.co.il/'
__NAME__ = '318'

import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,os,sys
import common

class manager_318:
    
    def __init__(self):
        self.MODES = common.enum(GET_SERIES_LIST=1, GET_EPISODES_LIST=2)
        
    def work(self, mode, url='', name='', page=''):
        if (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList(url)
        elif(mode==self.MODES.GET_EPISODES_LIST):
            self.getEpisodeList(url)

    def getSeriesList(self, url):
        ## get all the series base url
        contentType,baseUrl = common.getData(url)
        seriesBloc = re.compile('<ul class="fc sequence"(.*?)</ul>').findall(baseUrl)
        urls = re.compile('<li.*?data-json="{&quot;tooltipTitle&quot;:&quot;(.*?)&quot;.*?:&quot;(.*?)&.*?<a.*?href="(.*?)".*?class="img" src="(.*?)"').findall(baseUrl)
        for title, desc, url, img in urls:
            common.addDir(contentType, title, __BASE_URL__ + url, self.MODES.GET_EPISODES_LIST, img, __NAME__, desc)
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmc.executebuiltin("Container.SetViewMode(500)")
        
    def getEpisodeList(self, url):
        contentType,main_page = common.getData(url)
        episodeList = re.compile('<ol class="episode-list".*?</ol>').findall(main_page)
        episodes = re.compile('data-json.*?tooltipTitle&quot;:&quot;(.*?)&.*?:&quot;(.*?)&quot;.*?:&quot;(.*?)&.*?href="(.*?)"').findall(episodeList[0])
        for title, summary, img, url in episodes:
            episodeNum = re.compile('(\d.*?)/').findall(url)[0]
            contentType, page = common.getData('http://video2.walla.co.il/?w=null/null/' + episodeNum + '/@@/video/flv_pl')
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
                common.addLink(contentType,title, url, iconImage, str(time), epiDetails)
        nextPage = re.compile('<a class="in_blk p_r" href="(.*?)" style=""></a>').findall(main_page)
        if (len(nextPage)) > 0:
            addDir('UTF-8',__language__(30001), __BASE_URL__ + nextPage[0], self.MODES.GET_EPISODES_LIST, 'DefaultFolder.png', __NAME__)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmc.executebuiltin("Container.SetViewMode(500)")