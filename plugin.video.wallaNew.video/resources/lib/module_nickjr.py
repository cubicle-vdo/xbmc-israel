# -*- coding: utf-8 -*-

'''
Created on 30/04/2011

@author: shai
'''
__BASE_URL__ = 'http://nickjr.walla.co.il/'
__NAME__ = 'nickjr'
__PATTERN__ = '<div class="title w4b"><a href="(.*?)"'
__PATTERN_MORE__ = 'class="p_r"\sstyle=""\shref="(.*?)"'
__PATTERN_FEATURED__ ='<div class="title w5b mt5"><a href="(.*?)"'

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys
import wallacommon as common


class manager_nickjr:
    
    def __init__(self):
        self.MODES = common.enum(GET_SERIES_LIST=1, GET_EPISODES_LIST=2)
       
        
    def work(self, mode, url='', name='', page=''):
        
        if (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList()
        elif(mode==self.MODES.GET_EPISODES_LIST):
            common.getEpisodeList(__BASE_URL__, url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST, __PATTERN_FEATURED__, __PATTERN_MORE__)
            
    def getSeriesList(self):
        
        try:
            ## get all the series base url
            contentType,urls = common.getMatches(__BASE_URL__,'<a id="opc" href="(.*?)"')
            ## for each series we get the series page to parse all the info from
            for path in urls:
                contentType,page = common.getData(__BASE_URL__ + path)
                titleMatches = re.compile('class="stripe_title w7b white">\s*(.*?)\s*</h1>\s*<img src="(.*?)"').findall(page)
                if len(titleMatches) == 0:
                    # try a different possibility
                    titleMatches = re.compile('class="stripe_title w7b white">.*?>(.*?)<.*?src="(.*?)"').findall(page)
                details = re.compile('class="w3 nohvr" style="line-height:17px;">(.*?)<').findall(page)
                if (len(details)) > 0:
                    summary = details[0]
                else:
                    summary = ''
                if (len(titleMatches)) == 1:
                    title = titleMatches[0][0]
                    iconImage = common.getImage(titleMatches[0][1],__NAME__)
                    urlMatch = re.compile('class="w6b" href="(.*?)">').findall(page)
                    if (len(urlMatch)) > 0:
                        common.addDir(contentType,title, __BASE_URL__ + urlMatch[0], self.MODES.GET_EPISODES_LIST, iconImage, __NAME__, summary)
            common.addDir('UTF-8',"ספיישל דייגו בספארי לבקשת הורי הפורום", __BASE_URL__ +'?w=//2562538', self.MODES.GET_EPISODES_LIST, "", __NAME__, summary)
            common.addDir('UTF-8',"דייגו מציל את חיות הים --מיוחד לאבות מסורים", __BASE_URL__ +'?w=//2545366', self.MODES.GET_EPISODES_LIST, "", __NAME__, summary)
            common.addDir('UTF-8',"הרפתקאות דורה ודייגו", __BASE_URL__ +'?w=//2505725', self.MODES.GET_EPISODES_LIST, "", __NAME__, summary)
            
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        except Exception as e:
            print "WALLA exception in getSeriesList"
            raise 
