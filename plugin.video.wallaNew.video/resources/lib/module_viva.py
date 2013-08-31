# -*- coding: utf-8 -*-
'''
Created on 01/05/2011
Viva
@author: shai
'''

import urllib,urllib2,re,xbmc, xbmcaddon, xbmcplugin,xbmcgui,xbmcaddon,os,sys
import common

__BASE_URL__ = 'http://viva.walla.co.il/'
__NAME__ = 'viva'
__PATTERN__ = '<div class="title w3b"><a href="(.*?)"'
__PATTERN_MORE__ = 'class="p_r"\sstyle=""\shref="(.*?)"'
__PATTERN_FEATURED__ ='<div class="title w5b mb5"><a href="(.*?)"'

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')


class manager_viva:
        
    def __init__(self):
        self.MODES = common.enum(GET_SERIES_LIST=1, GET_EPISODES_LIST=2)
        
        
    def work(self, mode, url='', name='', page=''):
        if (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList()
        elif(mode==self.MODES.GET_EPISODES_LIST):
            common.getEpisodeList(__BASE_URL__, url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST, __PATTERN_FEATURED__, __PATTERN_MORE__)
            self.getMoreChapters(url, page, name)
            
    def getSeriesList(self):
        ## get all the series base url
        contentType,urls = common.getMatches(__BASE_URL__,'<a class="block w3 fldevt goldsep red bold" href="(.+?)" onclick="Evt\(this,(\d),&quot;(.+?)&quot;,3,&quot;folder_new_prakim_melaim')
        ## for each series we get the series page to parse all the info from
        for path, num, title in urls: ## num is not used and does nothing.
            if path.startswith("http://"):
                contentType,page = common.getData(path)
                url = path
            else:
                contentType,page = common.getData(__BASE_URL__ + path)
                url = __BASE_URL__ + path
            
            sumMatch = re.compile('class="w3">(.*?)<').findall(page)
            iconImage = re.compile('class="top_pic" src="(.+?)"').findall(page)
            fanart = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'resources', 'bg', 'curtains.png'))
            if not iconImage == None and len(iconImage) > 0 and len(iconImage[0]) > 0:                
                iconImage = common.getImage(iconImage[0], __NAME__)
            else:
                iconImage = ''
            if (len(sumMatch)) == 1:
                summary = sumMatch[0]
                common.addDir(contentType,title, url, self.MODES.GET_EPISODES_LIST, iconImage, __NAME__, summary, fanart)                    
            
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        
    def getMoreChapters(self, url, currentpage, title):
        numOfpages = len(common.getMatches(url, 'id="page_\d" href="(.+?)&page=(\d)" class="pages"'))
        if not currentpage == None and not currentpage == '':
            # we have at least to pages... if numOfPages is nothing it means that there are only two pages
            # we need to add the first page to the count
            if numOfpages == None or numOfpages == 0:
                numOfpages = 1;
            else:
                numOfpages += 1;
            currentPage = int(currentpage)
            if not (numOfpages == (currentPage - 1)):
                page = str(currentPage + 1)
                if not url.find("&page") == -1:
                    url = url.strip("&page=" + str(currentPage))
                self.addDir(common.__language__(30001), url + '&page=' + page, page)
        else :
            if not numOfpages == None and not numOfpages == 0:
                page = str(2) # second page
                self.addDir(common.__language__(30001), url + '&page=' + page, page)
        
    def addDir(self,name,url,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(self.MODES.GET_EPISODES_LIST)+"&name="+name+"&module="+urllib.quote_plus(__NAME__)+"&page="+page
        liz=xbmcgui.ListItem(name, iconImage='DefaultFolder.png', thumbnailImage='DefaultFolder.png')
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok