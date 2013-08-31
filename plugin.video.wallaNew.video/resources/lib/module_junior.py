# -*- coding: utf-8 -*-

'''
Created on 02/05/2011

@author: shai
'''
__BASE_URL__ = 'http://junior.walla.co.il/'
__NAME__ = 'junior'
__PATTERN__ = '<div class="title w3b"><a href="(.*?)"'
__PATTERN_MORE__ = 'class="p_r"\sstyle=""\shref="(.*?)"'
__PATTERN_FEATURED__ ='<div class="title w5b mt5"><a href="(.*?)"'

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys
import common

class manager_junior:
    
    def __init__(self):
        self.MODES = common.enum(GET_SERIES_LIST=1, GET_EPISODES_LIST=2, GET_CHAPTERS=3)
        
    def work(self, mode, url='', name='', page=''):
        if (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList()
        elif(mode==self.MODES.GET_CHAPTERS):
            self.getChapterList(url)
        elif(mode==self.MODES.GET_EPISODES_LIST):
            common.getEpisodeList(__BASE_URL__, url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST, __PATTERN_FEATURED__, __PATTERN_MORE__)
            
    def getSeriesList(self):
        ## get all the series base url
        contentType,baseUrl = common.getData(__BASE_URL__)
        urls = re.compile('class="opc".*?href="(.*?)".*?w3b">(.*?)<.*?src="(.*?)"').findall(baseUrl)
        ## for each series we get the series page to parse all the info from
        for path, title, img in urls:
            if path.startswith("http://"):
                url = path
            else:
                url = __BASE_URL__ + path
            common.addDir(contentType, title, url, self.MODES.GET_CHAPTERS, img, __NAME__)
                                       
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        
    def getChapterList(self, url):
        ## get all the series base url
        contentType,baseUrl = common.getData(url)
        print baseUrl
        menuItems = re.compile('<div class="right channel_wrap">.*?href="(.*?)"').findall(baseUrl)
        chapterUrl = __BASE_URL__ + menuItems[1]
        common.getEpisodeList(__BASE_URL__, chapterUrl, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST, __PATTERN_FEATURED__, __PATTERN_MORE__)