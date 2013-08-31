# -*- coding: utf-8 -*-
'''
Created on 01/05/2011

@author: shai
'''
__BASE_URL__ = 'http://nick.walla.co.il/'
__NAME__ = 'nick'
__PATTERN__ = '<div class="title w3b"><a href="(.*?)"'
__PATTERN_MORE__ = 'class="p_r"\sstyle=""\shref="(.*?)"'
__PATTERN_FEATURED__ ='<div class="title w5b mt5"><a href="(.*?)"'

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,os,sys
import common

class manager_nick:
    
    def __init__(self):
        self.MODES = common.enum(GET_SERIES_LIST=1, GET_EPISODES_LIST=2)

    def work(self, mode, url='', name='', page=''):
        if (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList()
        elif(mode==self.MODES.GET_EPISODES_LIST):
            common.getEpisodeList(__BASE_URL__, url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST, __PATTERN_FEATURED__, __PATTERN_MORE__)
            
    def getSeriesList(self):
        ## get all the series base url
        contentType,urls = common.getMatches(__BASE_URL__,'<a id="opc".*?href="(.*?)">(.*?)<')
        ## for each series we get the series page to parse all the info from
        for path in urls:
            if path[0].startswith("http://"):
                contentType,page = common.getData(path[0])
            else:
                contentType,page = common.getData(__BASE_URL__ + path[0])
            title = path[1]
            imageMatch = re.compile('class="stripe_title w7b white">(.*?)img\ssrc="(.*?)"').findall(page)
            details = re.compile('class="w3 nohvr">(.*?)<').findall(page)
            if (len(details)) > 0:
                summary = details[0]
            else:
                summary = ''
            if (len(imageMatch)) == 1:
                iconImage = common.getImage(imageMatch[0][1], __NAME__)
                urlMatch = re.compile('class="w6b fntclr2" href="(.*?)">').findall(page)
                if (len(urlMatch)) > 0:
                    common.addDir(contentType,title, __BASE_URL__ + urlMatch[0], self.MODES.GET_EPISODES_LIST, iconImage, __NAME__, summary)                    
            
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')