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
__NAME__ = 'wallavod'

__IMAGES_BASE__ = "http://msc.walla.co.il/w/w-160/"

import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,os,sys
import wallacommon as common

class manager_wallavod:
    
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
        if params.has_key("page"):
            page = int(params["page"])
        else :
            page = 1
        
        contentType, jsonString = common.getData('http://ws.vod.walla.co.il/ws/mobile/android/genre/'+ genre + "?id=" + genreId + "&page=" + str(page) + "&limit=50&sort=newest")
        if  common.__DEBUG__ == True:
            print "WALLA genre API "
            print jsonString
            
        
        resultJSON = json.loads(jsonString)
        genreItems = resultJSON["events"]
        totalResults = resultJSON["genre"]["amount"]
        
        if totalResults> (50*page):
            page = page +1
            common.addDir('UTF-8', "לדף הבא.....", "page=" + str(page) + "&genre=" + genre + "&genreId=" + genreId, self.MODES.GET_GENRE_ITEMS, elementId=__NAME__)
        
        for item in genreItems:
            itemName = item["title"]
            media=item["media"]
            itemId = str(item["id"])
            typeName = item["typeName"]
            about = item["about"]
            if item.has_key("duration"):
                duration = str(item["duration"])
            else:
                duration = '0'
            if media["types"].has_key("type_29"):  
                iconImage = __IMAGES_BASE__ + media["types"]["type_29"]["file"]
            else:
                iconImage = 'DefaultFolder.png'     
            if typeName == "movie":
                               
                common.addVideoLink("UTF-8",itemName, "item_id="+ itemId ,self.MODES.PLAY_MODE, iconImage,elementId=__NAME__, sum=about,duration=duration)
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
        limit = 100
        if params.has_key("page"):
            page = int(params["page"])
        else :
            page = 1
        
        contentType, pageContent = common.getData("http://ws.vod.walla.co.il/ws/mobile/android/episodes?id=" + seasonId + "&page=" + str(page)  + "&limit=" + str(limit) + "&sort=newest")
      
        if  common.__DEBUG__ == True:
            print "WALLA episodes API "
            print pageContent
        resultJSON = json.loads(pageContent)
        episodes = resultJSON["episodes"]
        
        # if we have 100 we might have another page - this is assumption there is not total items so we can't check for sure.
        if len(episodes) == 100 :
            common.addDir('UTF-8', "לדף הבא.....", "page=" + str(page+1) + "&seasonId=" + seasonId , self.MODES.GET_EPISODES_LIST, elementId=__NAME__)
                    
        i=1
        for episode in episodes:
            episodeId = str(episode["id"])
            title = "[COLOR yellow]" + str((page*limit)-limit+i) + ".   [/COLOR]" + episode["title"] 
            media = episode["media"]
            
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
            i=i+1
     
    def playEpisode(self,url):
        
        try:
            #report to google about use of the addon
            contentType, jsonString = common.getData("http://goo.gl/saJsOc")        
        except:
            pass
         
        params = common.getParams(url)
        itemId =  str(params["item_id"])
        print itemId
        
        contentType, page = common.getData("http://ws.vod.walla.co.il/ws/mobile/android/flvpl/?item_id=" + itemId +"&type=json")
        if  common.__DEBUG__ == True:
            print "WALLA players API "
            print page
        resultJSON = json.loads(page)
        item = resultJSON["items"]["item"]
        subtitlesUrl = None
        if item.has_key("subtitles") :
            
            subtitles = item["subtitles"]["subtitle"]
            firstitem = subtitles[0]
            print firstitem
            subtitlesUrl = firstitem["src"]
            
            print "subtitleUrl=" + subtitlesUrl
            
        videoUrl = resultJSON["video_src_ipad"]
        #videoSrc = item["src"]
        #videoUrl = "rtmp://waflaWBE.walla.co.il/ app=vod/ swfvfy=true swfUrl=http://isc.walla.co.il/w9/swf/video_swf/vod/WallaMediaPlayerAvod.swf tcurl=rtmp://waflaWBE.walla.co.il/vod/ pageurl=http://vod.walla.co.il playpath=" + videoSrc
        
        duration = item["duration"]
        title = item["title"]
        
        
        listItem = xbmcgui.ListItem(title, 'DefaultFolder.png', 'DefaultFolder.png', path=videoUrl) # + '|' + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        listItem.setInfo(type='Video', infoLabels={ "Title": title,"Duration":str(duration)})
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
        
        if subtitlesUrl:
            self.downloadSubtitles(subtitlesUrl)
            
    
    def downloadSubtitles(self,subtitlesUrl):
        print "download subtitles " + subtitlesUrl
        while not xbmc.Player().isPlaying():
            xbmc.sleep(10) #wait until video is being played
        xbmc.Player().setSubtitles(subtitlesUrl);
        #response = urllib.urlretrieve (url, "c:/subtitles.srt")
        #html = response.read()
        
    def getMainJSON(self):

        contentType, page = common.getData('http://ws.vod.walla.co.il/ws/mobile/android/toolbar')
        if  common.__DEBUG__ == True:
            print "WALLA API main"
            print page
            
        prms=json.loads(page)
        return prms;