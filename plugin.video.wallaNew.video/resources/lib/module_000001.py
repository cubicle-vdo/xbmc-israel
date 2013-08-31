# -*- coding: utf-8 -*-

'''
Created on 16/05/2011

@author: shai
'''
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__language__ = __settings__.getLocalizedString

__BASE_URL__ = 'http://vod.walla.co.il/'
__NAME__ = '000001'

import urllib, re, sys
import xbmc, xbmcplugin, xbmcgui
import common

class manager_000001:
    
    def __init__(self):
        self.MODES = common.enum(GET_GENRE=1, GET_SERIES_LIST=2, GET_EPISODES_LIST=3)
        
    def work(self, mode, url='', name='', page=''):
        if (mode==self.MODES.GET_GENRE):
            self.getGenere(url)
        elif (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList(url)
        elif (mode==self.MODES.GET_EPISODES_LIST):
            self.getEpisodeList(url)
    
    def getGenere(self, url):
        ## get all the series base url
        contentType, page = common.getData(url)
        genreBloc = re.compile('<nav class="sideNav".*?</nav>').findall(page)        
        genres = re.compile('<li.*?href="(.*?)".*?"text">(.*?)<').findall(genreBloc[0])
        i = 1
        for url, title in genres:
            if i > 1:
                common.addDir('UTF-8', title, __BASE_URL__ + url, self.MODES.GET_SERIES_LIST, 'DefaultFolder.png', __NAME__)
            i = i + 1
        
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmc.executebuiltin("Container.SetViewMode(503)")
    
    def getSeriesList(self, url):
        ## get all the series base url
        contentType,baseUrl = common.getData(url)
        seriesBloc = re.compile('<ul class="fc sequence"(.*?)</ul>').findall(baseUrl)
        urls = re.compile('<li.*?data-json="{&quot;tooltipTitle&quot;:&quot;(.*?)&quot;.*?:&quot;(.*?)&.*?<a.*?href="(.*?)".*?class="img" src="(.*?)"').findall(baseUrl)
        for title, desc, url, img in urls:
            episodeNum = re.compile('/(\d.*)').findall(url)[0]
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
                playPath = re.compile('<src>(.*?)</src>').findall(page)
                length = len(playPath)
                url = 'rtmp://waflaWBE.walla.co.il/ app=vod/ swfvfy=true swfUrl=http://isc.walla.co.il/w9/swf/video_swf/vod/WallaMediaPlayerAvod.swf tcurl=rtmp://waflaWBE.walla.co.il/vod/ pageurl=http://vod.walla.co.il' + url + ' playpath=' + playPath[length -1]
                common.addLink(contentType,title, url, img, str(time), epiDetails)
            #common.addDir('UTF-8', title, __BASE_URL__ + url, self.MODES.GET_EPISODES_LIST, img, __NAME__, desc)
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmc.executebuiltin("Container.SetViewMode(500)")