# -*- coding: utf-8 -*-

'''
Created on 02/05/2011

@author: shai
'''

__BASE_URL__ = 'http://video.walla.co.il/'
__NAME__ = '2245'
__PATTERN__ = 'class="block w2b fclr1 mrg_t4" href="(.+?)"'

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys
import common

class manager_2245:
    
    def __init__(self):
        self.MODES = common.enum(GET_SERIES_LIST=1, GET_EPISODES_LIST=2)
        
    def work(self, mode, url='', name='', page=''):
        if (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList()
        elif(mode==self.MODES.GET_EPISODES_LIST):
            common.getEpisodeList(__BASE_URL__, url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST)

    def getSeriesList(self):
        ## get all the series base url
        contentType,baseUrl = common.getData(__BASE_URL__ + '?w=/2245')
        urls = re.compile('<div class="bottomBorder"><a href="(.*?)".*?><img src="(.+?)"').findall(baseUrl)
        ## for each series we get the series page to parse all the info from
        for path, image in urls:
            if path.startswith("http://"):
                contentType,page = common.getData(path)
            else:
                contentType,page = common.getData(__BASE_URL__ + path)
            details = re.compile('class="w3" style="margin-left:288px;">(\s.*)<div>(.*?)</div>(\s.*)<div>(.+?)<').findall(page)
            if (len(details)) > 0:
                summary = details[0][3]
            else:
                summary = ''
            iconImage = image
            fanartImage = re.compile('class="vbox720x330" src="(.+?)" alt="(.*?)"').findall(page)
            if not fanartImage == None:
                try:
                    fanart = fanartImage[0][0]
                    title = fanartImage[0][1]
                except:
                    title = fanartImage
                urlMatch = re.compile('class="hd1 mrg_r1 none" style=""><a href="(.+?)"').findall(page)
                if (len(urlMatch)) > 0:
                    common.addDir(contentType,title, __BASE_URL__ + urlMatch[0], self.MODES.GET_EPISODES_LIST, iconImage, __NAME__, summary, fanart)                    
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')        