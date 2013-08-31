# -*- coding: utf-8 -*-

'''
Created on 02/05/2011
Domino Gross channel
@author: shai
'''

__BASE_URL__ = 'http://video.walla.co.il/'
__NAME__ = '2222'
__PATTERN__ = 'class="block w2b fclr1 mrg_t4" href="(.+?)"'

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys
import common

class manager_2222:
    
    def __init__(self):
        self.MODES = common.enum(GET_SERIES_LIST=1, GET_EPISODES_LIST=2)
        
    def work(self, mode, url='', name='', page=''):
        if (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList()
        elif(mode==self.MODES.GET_EPISODES_LIST):
            common.getEpisodeList(__BASE_URL__, url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST)

    def getSeriesList(self):
        ## get all the series base url
        contentType,baseUrl = common.getData(__BASE_URL__ + '?w=/2222')
        urls = re.compile('<div class="bottomBorder"><a href="(.*?)".*?><img src="(.+?)" alt="(.+?)"').findall(baseUrl)
        ## for each series we get the series page to parse all the info from
        for path, image, title in urls:
            if path.startswith("http://"):
                contentType,page = common.getData(path)
                url = path
            else:
                contentType,page = common.getData(__BASE_URL__ + path)
                url = __BASE_URL__ + path
            iconImage = image
            fanartImage = re.compile('class="vbox720x330" src="(.+?)"').findall(page)
            if not fanartImage == None and len(fanartImage) > 0 and len(fanartImage[0]) > 0:
                fanart = fanartImage[0]
            else:
                fanart = ''
            common.addDir(contentType,title, url, self.MODES.GET_EPISODES_LIST, iconImage, __NAME__, '', fanart)                    
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmc.executebuiltin("Container.SetViewMode(500)")      