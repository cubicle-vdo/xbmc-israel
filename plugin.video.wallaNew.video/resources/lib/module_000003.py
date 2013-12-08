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

import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,os,sys
import wallacommon as common

class manager_000003:
    
    def __init__(self):
        self.MODES = common.enum(PLAY_MODE=10,GET_GENRE=1, GET_SERIES_LIST=2, GET_SEASONS_LIST=5,GET_EPISODES_LIST=3, GET_MOVIE_LIST=4)
        
    def work(self, mode, url='', name='', page=''):
        if (mode==self.MODES.GET_GENRE):
            self.getGenere(url)
        elif (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList(url)
        elif (mode==self.MODES.GET_SEASONS_LIST):
            self.getSeasons(url)
        elif (mode==self.MODES.GET_EPISODES_LIST):
            self.getEpisodes(url)
        elif (mode==self.MODES.GET_MOVIE_LIST):
            self.getMovieList(url)
        elif (mode==self.MODES.PLAY_MODE):
            self.playEpisode(url)
    
    def getGenere(self, url):
       
        categories = self.getMainJSON();
        
        i = 0
        for category in categories:
            #print "WALLA main category :" + str(category)
            categoryName = category["name"]
            
            genreEnglish = str(category["englishName"])
            
            genres = category["genres"]
            for genre in genres:
                genreName = genre["name"]
                genreId = str(genre["id"])
                amount = str(genre["amount"])
                
                dirName = categoryName + ":" + genreName + "(" + amount + ")"
                #iconImage = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images', 'wallaBase', module + '.png'))
                common.addDir('UTF-8', dirName, "genre=" + genreEnglish + "&genreId=" + genreId, self.MODES.GET_SERIES_LIST, elementId=__NAME__)
            #common.addDir('UTF-8', title, __BASE_URL__, self.MODES.GET_SERIES_LIST, 'DefaultFolder.png', __NAME__)
            
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    
    def getSeriesList(self, url):
        print "walla getSeriesList url:" + str(url)
        
        params = common.getParams(url)
        genreId =  params["genreId"]
        genre = params["genre"]
        
        contentType, page = common.getData('http://ws.vod.walla.co.il/ws/mobile/android/genre/'+ genre + "?id=" + genreId + "&page=1&limit=100&sort=newest")
        if  common.__DEBUG__ == True:
            print "WALLA genre API "
            print page
            
        
        resultJSON = json.loads(page)
        seriesList = resultJSON["events"]
        for series in seriesList:
            seriesName = series["title"]
            media=series["media"]
            seriesId = str(series["id"])
            typeName = str(series["typeName"])
            
            dirName = seriesName 
            #iconImage = xbmc.translatePath(os.path.join(__PLUGIN_PATH__, 'cache', 'images', 'wallaBase', module + '.png'))
            common.addDir('UTF-8', dirName, "seriesId=" + seriesId , self.MODES.GET_SEASONS_LIST, elementId=__NAME__)
   
        
    def getSeasons(self, url):
        
        
        print "walla getSeasons url:" + str(url)
        
        params = common.getParams(url)
        seriesId =  str(params["seriesId"])
        
        
        contentType, page = common.getData("http://ws.vod.walla.co.il/ws/mobile/android/tvshow?id=" + seriesId + "&page=1&limit=100&sort=newest")
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
            about = episode["about"]
            imageTypes = media["types"]
            image = imageTypes["type_29"]
            
            iconImage = "http://msc.walla.co.il/w/w-160/" + image["file"]
            
            common.addVideoLink("UTF-8",title, "item_id="+ episodeId ,self.MODES.PLAY_MODE, iconImage,elementId=__NAME__, sum=about)
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
        
        
        listItem = xbmcgui.ListItem("name", 'DefaultFolder.png', 'DefaultFolder.png', path=videoUrl) # + '|' + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        listItem.setInfo(type='Video', infoLabels={ "Title": "name"})
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
        
      
          
#         contentType,main_page = common.getData(url)
#         episodeList = re.compile('<ol class="episode-list".*?</ol>').findall(main_page)
#         episodes = re.compile('data-json.*?tooltipTitle&quot;:&quot;(.*?)&.*?:&quot;(.*?)&quot;.*?:&quot;(.*?)&.*?href="(.*?)"').findall(episodeList[0])
#         for title, summary, img, url in episodes:
#             episodeNum = re.compile('(\d.*?)/').findall(url)[0]
#             contentType, page = common.getData('http://video2.walla.co.il/?w=null/null/' + episodeNum + '/@@/video/flv_pl')
#             titleMatches = re.compile('<title>(.*?)</title>(.*)<subtitle>(.*?)<').findall(page)
#             if (len(titleMatches)) == 1:
#                 title = titleMatches[0][0]
#                 images = re.compile('<preview_pic>(.*?)</preview_pic>').findall(page)
#                 if (len(images)) >= 1:
#                     iconImage = images[0]
#                 details = re.compile('<synopsis>(.*?)</synopsis>').findall(page)
#                 if (len(details)) > 0:
#                     epiDetails = details[0]
#                 
#                 timeInSeconds = re.compile('<duration>(.*?)</duration>').findall(page)
#                 if not timeInSeconds == None and not len(timeInSeconds[0]) <= 0:
#                     time = int(timeInSeconds[0]) / 60
#                 else:
#                     time = '00:00'
#                 url = 'rtmp://waflaWBE.walla.co.il/ app=vod/ swfvfy=true swfUrl=http://i.walla.co.il/w9/swf/video_swf/vod/walla_vod_player_adt.swf?95 tcurl=rtmp://waflaWBE.walla.co.il/vod/ pageurl=http://walla.co.il/ playpath=' + re.compile('<src>(.*?)</src>').findall(page)[0]
#                 common.addLink(contentType,title, url, iconImage, str(time), epiDetails)
#         nextPage = re.compile('<a class="in_blk p_r" href="(.*?)" style=""></a>').findall(main_page)
#         if (len(nextPage)) > 0:
#             addDir('UTF-8',__language__(30001), __BASE_URL__ + nextPage[0], self.MODES.GET_EPISODES_LIST, 'DefaultFolder.png', __NAME__)
       
    
    
    def getMainJSON(self):

        contentType, page = common.getData('http://ws.vod.walla.co.il/ws/mobile/android/toolbar')
        if  common.__DEBUG__ == True:
            print "WALLA API main"
            print page
            
        prms=json.loads(page)
        return prms;