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
import wallacommon as common

class manager_nick:
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
            #block=re.compile('<div style="padding: 10px(.*?)folder2_game')
            contentType,block = common.getMatches(__BASE_URL__,'padding: 10px(.*?)folder2_game')
            page = re.compile('<a href="(.*?)".*?">(.*?)<').findall(block[0])
            #contentType,urls = common.getMatches(__BASE_URL__,'margin-left: 0px;">(.*?)</a><a href="(.*?)"')
            ## for each series we get the series page to parse all the info from
            idx=1
            for path in page:
                
                print path
                #contentType,page = common.getData(__BASE_URL__ + path[0])
                #page = re.compile(__BASE_URL__ + path[0])
                #titleMatches = re.compile('class="stripe_title w7b white">\s*(.*?)\s*</h1>\s*<img src="(.*?)"').findall(page)
                #if len(titleMatches) == 0:
                    # try a different possibility
                    #titleMatches = re.compile('class="stripe_title w7b white">.*?>(.*?)<.*?src="(.*?)"').findall(page)
                #details = re.compile('class="w3 nohvr" style="line-height:17px;">(.*?)<').findall(page)
                #if (len(details)) > 0:
                    #summary = details[0]
                #else:
                summary = ''
                title=path[1]
                '''if (len(titleMatches)) == 1:
                    title = titleMatches[0][0]'''
                iconImage =common.getImageNick(idx,'nick',__BASE_URL__ + path[0])
                print iconImage
                idx=idx + 1
                '''urlMatch = re.compile('class="w6b" href="(.*?)">').findall(page)
                print urlMatch
                
                if (len(urlMatch)) > 0:'''
                common.addDir(contentType,title, __BASE_URL__ + path[0], self.MODES.GET_EPISODES_LIST, iconImage, __NAME__, summary)               
            
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        except Exception as e:
            print "WALLA exception in getSeriesList"
            raise 