# -*- coding: utf-8 -*-

'''
Created on 16/05/2011
Walla Series
@author: shai
'''
import xbmcaddon
import json

__settings__ = xbmcaddon.Addon(id='plugin.video.wallaNew.video')
__language__ = __settings__.getLocalizedString
__BASE_URL__ = 'http://ws.vod.walla.co.il/ws/mobile/android/main'
__NAME__ = '000003'

__IMAGES_BASE__ = "http://msc.walla.co.il/w/w-160/"

import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,os,sys
import wallacommon as common

class manager_000003:
    
    def __init__(self):
        self.MODES = common.enum(PLAY_MODE=10,GET_GENRE=1, GET_GENRE_ITEMS=2, GET_SEASONS_LIST=5,GET_EPISODES_LIST=3, GET_MOVIE_LIST=4)
        
    def work(self, mode, url='', name='', page=''):

        if (mode==self.MODES.GET_GENRE):
            self.getGenere(url)
        elif (mode==self.MODES.GET_GENRE_ITEMS):
            self.getGenereItems(url)
        elif (mode==self.MODES.GET_SEASONS_LIST):
            self.getSeasons(url)
        elif (mode==self.MODES.GET_EPISODES_LIST):
            self.getEpisodes(url)
        elif (mode==self.MODES.PLAY_MODE):
            self.playEpisode(url)
    
    def getGenere(self, url):
       
        params = common.getParams(url)
        selectedGenre = params["englishName"]
       
        categories = self.getMainJSON();
        
        i = 0
        for category in categories:
            #print "WALLA main category :" + str(category)
            categoryName = category["name"]
            
            genreEnglish = str(category["englishName"])
            
            genres = category["genres"]
            for genre in genres:
                
                genreName = genre["name"]
                if (genreEnglish==selectedGenre):
                    genreId = str(genre["id"])
                    amount = str(genre["amount"])
                    
                    dirName = genreName + " (" + amount + ")"
                    #iconImage = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images', 'wallaBase', module + '.png'))
                    common.addDir('UTF-8', dirName, "genre=" + genreEnglish + "&genreId=" + genreId, self.MODES.GET_GENRE_ITEMS, elementId=__NAME__)
            
            
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    
    def getGenereItems(self, url):
        print "walla getSeriesList url:" + str(url)
        
        params = common.getParams(url)
        genreId =  params["genreId"]
        genre = params["genre"]
        
        contentType, page = common.getData('http://ws.vod.walla.co.il/ws/mobile/android/genre/'+ genre + "?id=" + genreId + "&page=1&limit=500&sort=newest")
        if  common.__DEBUG__ == True:
            print "WALLA genre API "
            print page
            
        
        resultJSON = json.loads(page)
        seriesList = resultJSON["events"]
        for series in seriesList:
            itemName = series["title"]
            media=series["media"]
            itemId = str(series["id"])
            typeName = series["typeName"]
            about = series["about"]
            
            iconImage = __IMAGES_BASE__ + media["types"]["type_29"]["file"] 
            if typeName == "movie":
                               
                common.addVideoLink("UTF-8",itemName, "item_id="+ itemId ,self.MODES.PLAY_MODE, iconImage,elementId=__NAME__, sum=about)
            else:
               
                common.addDir('UTF-8', itemName, "seriesId=" + itemId , self.MODES.GET_SEASONS_LIST, iconImage, elementId=__NAME__)
            
   
        
    def getSeasons(self, url):
        
        
        print "walla getSeasons url:" + str(url)
        
        params = common.getParams(url)
        seriesId =  str(params["seriesId"])
       
        
        contentType, page = common.getData("http://ws.vod.walla.co.il/ws/mobile/android/tvshow?id=" + seriesId + "&page=1&limit=10&sort=newest")
        
        if  common.__DEBUG__ == True:
            print "WALLA tvshow API "
            print page
           
        tvshow = json.loads(page)
  
        seasons = tvshow["episodesContainer"]
        for season in seasons:
            title = season["title"]
            seasonId = str(season["id"])
            common.addDir('UTF-8', title, "seasonId=" + seasonId , self.MODES.GET_EPISODES_LIST, elementId=__NAME__)
        

        
    
    def getEpisodes(self, url):
        
        params = common.getParams(url)
        seasonId =  str(params["seasonId"])
        
        contentType, page = common.getData("http://ws.vod.walla.co.il/ws/mobile/android/episodes?id=" + seasonId + "&page=1&limit=100&sort=newest")
        if  common.__DEBUG__ == True:
            print "WALLA episodes API "
            print page
        resultJSON = json.loads(page)
        episodes = resultJSON["episodes"]
        
        for episode in episodes:
            episodeId = str(episode["id"])
            title = episode["title"]
            media = episode["media"]
            abstract = episode["abstract"]
            imageTypes = media["types"]
            image = imageTypes["type_29"]
            
            summary = ""
            if episode.has_key("abstract"):
                summary = episode["abstract"]
            elif episode.has_key("about"):
                summary = episode["about"]
            
            iconImage = __IMAGES_BASE__ + image["file"]
            
            common.addVideoLink("UTF-8",title, "item_id="+ episodeId ,self.MODES.PLAY_MODE, iconImage,elementId=__NAME__, sum=summary)
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            xbmc.executebuiltin("Container.SetViewMode(500)")
     
    def playEpisode(self,url):
         
        params = common.getParams(url)
        itemId =  str(params["item_id"])
        print itemId
        
        contentType, page = common.getData("http://ws.vod.walla.co.il/ws/mobile/android/flvpl/?item_id=" + itemId +"&type=json")
        if  common.__DEBUG__ == True:
            print "WALLA players API "
            print page
        resultJSON = json.loads(page)
        videoUrl = resultJSON["video_src_tv"]
        title = resultJSON["items"]["item"]["title"]
        
        
        listItem = xbmcgui.ListItem(title, 'DefaultFolder.png', 'DefaultFolder.png', path=videoUrl) # + '|' + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        listItem.setInfo(type='Video', infoLabels={ "Title": title})
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
        
    def getMainJSON(self):

        contentType, page = common.getData('http://ws.vod.walla.co.il/ws/mobile/android/toolbar')
        if  common.__DEBUG__ == True:
            print "WALLA API main"
            print page
            
        prms=json.loads(page)
        return prms;