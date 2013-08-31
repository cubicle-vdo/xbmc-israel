# -*- coding: utf-8 -*-

'''
Created on 02/05/2011
Kofiko
@author: shai
'''

__BASE_URL__ = 'http://kofiko.walla.co.il/'
__NAME__ = 'kofiko'
__PATTERN__ = '<div class="title w3b"><a href="(.*?)"'
__PATTERN_FEATURED__ ='<div class="title w5b mt5"><a href="(.*?)"'

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys
import common

class manager_kofiko:
    
    def __init__(self):
        self.MODES = common.enum(GET_SERIES_LIST=1, GET_EPISODES_LIST=2)
        
    def work(self, mode, url='', name='', page=''):
        if (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList()
        elif(mode==self.MODES.GET_EPISODES_LIST):
            common.getEpisodeList(__BASE_URL__, url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST, __PATTERN_FEATURED__)

    def getSeriesList(self):
        ## get all the series base url
        contentType,baseUrl = common.getData(__BASE_URL__)
        urls = re.compile('<a class="in_blk tbBtn" href="\/(.+?)"').findall(baseUrl)
        url = urls[0] ## first is the url we need.
        common.getEpisodeList(__BASE_URL__, __BASE_URL__ + url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST,  __PATTERN_FEATURED__)