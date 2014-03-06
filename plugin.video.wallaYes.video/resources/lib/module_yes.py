# -*- coding: utf-8 -*-
'''
Created on 01/05/2011

@author: shai
'''

import urllib,urllib2,re,xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcaddon,os,sys
import common

__BASE_URL__ = 'http://yes.walla.co.il/'
__NAME__ = 'yes'
__PATTERN__ = 'top"><a href="(.+?)" class="w2b">'
__PATTERN_MORE__ = 'class="p_r"\sstyle=""\shref="(.*?)"'
__PATTERN_FEATURED__ = ''
__settings__ = xbmcaddon.Addon(id='plugin.video.wallaYes.video')
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')

class manager_yes:
    
    def __init__(self):
        self.MODES = common.enum(GET_CATEGORIES=1, GET_SERIES_LIST=2, GET_EPISODES_LIST=3)

    def work(self, mode, url='', name='', page='0'):
        if (mode==self.MODES.GET_CATEGORIES):
            self.getCategories()
        elif (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList(url)
        elif(mode==self.MODES.GET_EPISODES_LIST):
            self.getEpisodeList(url, page)
            
    def getCategories(self):
        categories={'1':30003,'2':30004, '4':30005, '100':30006}
        for genre, titleNLS in categories.iteritems():
            title = common.__language__(titleNLS)
            iconImage = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'resources', 'images', 'icon_' + str(titleNLS) + '.png'))
            if not os.path.exists(iconImage):
                iconImage = 'DefaultFolder.png'
            fanart = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'resources', 'bg', 'fanart_' + str(titleNLS) + '.png'))
            if not os.path.exists(fanart):
                fanart = 'DefaultFolder.png'
            common.addDir('UTF-8',title,genre,self.MODES.GET_SERIES_LIST,iconImage,__NAME__,'', fanart)
        
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        
    def getSeriesList(self, genre):
        if genre == '100':
            ## handle movies
            categories={'7373':30007,'7396':30008, '7397':30009, '7367':30010}
            for url, titleNLS in categories.iteritems():
                title = common.__language__(titleNLS)
                iconImage = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'resources', 'images', 'icon_' + str(titleNLS) + '.png'))
                if not os.path.exists(iconImage):
                    iconImage = 'DefaultFolder.png'
                fanart = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'resources', 'bg', 'fanart_' + str(titleNLS) + '.png'))
                if not os.path.exists(fanart):
                    fanart = 'DefaultFolder.png'
                common.addDir('UTF-8',title, url, self.MODES.GET_EPISODES_LIST, iconImage, __NAME__, '', fanart)
        else:
            ## get all the series that have full episodes
            contentType,matches = common.getMatches('http://yes.walla.co.il/?w=0/7701','id="(\d+)" href="" onclick="itemsFetchRows\(this.id,' + str(genre) + ',0\); return\(false\);">(.+?)<')                
            for url, name in matches:
                iconimage = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'resources', 'images', 'icon_' + name + '.png'))
                if not os.path.exists(iconimage):
                    iconimage = 'DefaultFolder.png'
                fanart = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'resources', 'bg', 'fanart_' + name + '.png'))
                if not os.path.exists(fanart):
                    fanart = 'DefaultFolder.png'
                common.addDir('windows-1255', name, str(genre) + '/' + url, self.MODES.GET_EPISODES_LIST, iconimage, __NAME__, '', fanart)
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        
    def getEpisodeList(self, url, page='0'):
        if page == None:            
            page = '0'
        if url.find("/") == -1:
            detailUrl = 'http://yes.walla.co.il/?w=1/' + url + '/' + page + '/10/@ajaxItems'
            mypattern = '<a href="" onclick="itemsFetchRows\((\d+)\); return false;"><img align="absmiddle" src=".*?" class="prevPage"'
        else:
            detailUrl = 'http://yes.walla.co.il/?w=' + url + '/' + page + '/@Ajax_display_full_chapters'
            constants = url.split('/')
            mypattern = '<a href="" onclick="itemsFetchRows\(' + constants[1] + ',' + constants[0] + ',(\d+)\); return false;"><img align="absmiddle" src=".*?" class="prevPage"'
            
        common.getEpisodeList(__BASE_URL__, detailUrl, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST, __PATTERN_FEATURED__, __PATTERN_MORE__)
        contentType,hasNext = common.getMatches(detailUrl, mypattern)
        if not hasNext == None and len(hasNext) > 0:
            # there is a next page
            page = hasNext[0]
            self.addDir(common.__language__(30001), url, page)
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
                        
    def addDir(self,name,url,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(self.MODES.GET_EPISODES_LIST)+"&name="+name+"&module="+urllib.quote_plus(__NAME__)+"&page="+page
        ok=True
        liz=xbmcgui.ListItem(name, iconImage='DefaultFolder.png', thumbnailImage='DefaultFolder.png')
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok