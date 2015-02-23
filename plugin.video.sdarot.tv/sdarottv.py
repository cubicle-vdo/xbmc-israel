# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from www.sdarot.co.in
"""
import urllib, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import HTMLParser
import json
import cookielib
import unicodedata


##General vars        
__plugin__ = "Sdarot.TV Video"
__author__ = "Cubicle"

__image_path__ = ''
__settings__ = xbmcaddon.Addon(id='plugin.video.sdarot.tv')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)


dbg = False # used for simple downloader logging

#DOMAIN='http://sdarot.wf'
DOMAIN = __settings__.getSetting("domain")

#print "Sdarot Domain=" + DOMAIN

from sdarotcommon import *

path = xbmc.translatePath(__settings__.getAddonInfo("profile"))
cookie_path = os.path.join(path, 'sdarot-cookiejar.txt')
#print("Loading cookies from :" + repr(cookie_path))
cookiejar = cookielib.LWPCookieJar(cookie_path)

if os.path.exists(cookie_path):
    try:
        cookiejar.load()
    except:
        pass
elif not os.path.exists(path):
    os.makedirs(path) 
    
cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_handler)
urllib2.install_opener(opener)
#print "built opener:" + str(opener)


def MAIN_MENU():
    CHECK_LOGIN()
    addDir('[COLOR red] חפש  [/COLOR]',DOMAIN+"/search",6,'')
    addDir("הכל א-ת","all-heb",2,'',DOMAIN+'/series');
    addDir("הכל a-z","all-eng",2,'',DOMAIN+'/series');
    page = getData(DOMAIN+'/series',referer="")
    matches = re.compile('<li><a href="/series/genre/(.*?)">').findall(page)
    for match in matches:
         a=str(match)
         sp=a.split('-',1)
         #print sp , a
         addDir(sp[1],"all-heb",2,'',DOMAIN+'/series/genre/'+sp[0]+sp[1])
	
def SearchSdarot(url,search_entered):
	if 'חפש' in  search_entered :
		keyboard = xbmc.Keyboard("", "חפש כאן")
		keyboard.doModal()
		if keyboard.isConfirmed():
			search_entered = keyboard.getText()
	page = getData(url=url,timeout=0,postData="search=" + search_entered)
#	print page
	matches = re.compile('<a href="/watch/(\d+)-(.*?)">').findall(page)
	#print matches

	#needs to remove duplicted result (originaly in site
	matches = [ matches[i] for i,x in enumerate(matches) if x not in matches[i+1:]]
	#print matches
	for match in matches:
	  series_id = match[0]
	  link_name = match[1]
	  image_link=DOMAIN+"/media/series/"+str(match[0])+".jpg"
	  series_link=DOMAIN+"/watch/"+str(match[0])+"/"+match[1]
	  addDir(link_name,series_link,"3&image="+urllib.quote(image_link)+"&series_id="+series_id+"&series_name="+urllib.quote(link_name),image_link)
		
def INDEX_AZ(url,page):
    page = getData(page);
    matches = re.compile('<a href="/watch/(\d+)-(.*?)">.*?</noscript>.*?<div>(.*?)</div>').findall(page)
    sr_arr = []
    idx = 0
    i=0
    if url == "all-eng":
      idx = 1
    for match in matches:
      series_id = match[0]
      link_name = match[1]
      name = HTMLParser.HTMLParser().unescape(match[2])
      m_arr = name.split(" / ")
      if (len(m_arr)>1) and (idx==1):
        sr_arr.append(( series_id, link_name, m_arr[1].strip() ))
      else:
        sr_arr.append(( series_id, link_name, m_arr[0].strip() ))
      i=i+1
    sr_sorted = sorted(sr_arr,key=lambda sr_arr: sr_arr[2])
      
    for key in sr_sorted:
      series_link=DOMAIN+"/watch/"+str(key[0])+"/"+key[1]
      image_link=DOMAIN+"/media/series/"+str(key[0])+".jpg"      
      addDir(key[2],series_link,"3&image="+urllib.quote(image_link)+"&series_id="+str(key[0])+"&series_name="+urllib.quote(key[1]),image_link)
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
      
def sdarot_series(url):
    series_id=urllib.unquote_plus(params["series_id"])
    series_name=urllib.unquote_plus(params["series_name"])
    image_link=urllib.unquote_plus(params["image"])
    downloadEnabled = False
    
    opener.addheaders = [('Referer',url)]
    opener.open(DOMAIN+'/landing/'+series_id).read()
  #  print "sdarot_series: Fetching URL:"+url  
    try:
        page = opener.open(url).read()
        #print cookiejar
    except urllib2.URLError, e:
        print 'sdarot_season: got http error ' +str(e.code) + ' fetching ' + url + "\n"
        raise e
    #page = getData(url);
    #print "Page Follows:\n"
    #print page
                 #<ul id="season">
    block_regexp='id="season">(.*?)</ul>'
    seasons_list = re.compile(block_regexp,re.I+re.M+re.U+re.S).findall(page)[0]
    regexp='>(\d+)</a'
    matches = re.compile(regexp).findall(seasons_list)
            
    for season in matches:
        downloadMenu = []
        if downloadEnabled:
            downloadUrl = "XBMC.RunPlugin(plugin://plugin.video.sdarot.tv/?mode=7&url=" + url + "&season_id="+str(season)+"&series_id="+str(series_id) + ")"
            downloadMenu.append(('הורד עונה', downloadUrl,))
        addDir("עונה "+ str(season),url,"5&image="+urllib.quote(image_link)+"&season_id="+str(season)+"&series_id="+str(series_id)+"&series_name="+urllib.quote(series_id),image_link,contextMenu=downloadMenu)
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
      
def sdarot_season(url):
    series_id=urllib.unquote_plus(params["series_id"])
    series_name=urllib.unquote_plus(params["series_name"])
    season_id=urllib.unquote_plus(params["season_id"])
    image_link=urllib.unquote_plus(params["image"])
    page = getData(url=DOMAIN+"/ajax/watch",timeout=0,postData="episodeList=true&serie="+series_id+"&season="+season_id);
    
    episodes=json.loads(page)
    
    if episodes is None or (len(episodes)==0):
        xbmcgui.Dialog().ok('Error occurred',"לא נמצאו פרקים לעונה")
        return
    
    #print episodes
    for i in range (0, len(episodes)) :
        epis= str(episodes[i]['episode'])
        addVideoLink("פרק "+epis, url, "4&episode_id="+epis+"&image="+urllib.quote(image_link)+"&season_id="+str(season_id)+"&series_id="+str(series_id)+"&series_name="+urllib.quote(series_id),image_link, '')         
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

def download_season(url):
    import SimpleDownloader as downloader
    downloader = downloader.SimpleDownloader()
    downloader.dbg = False
    
    series_id=urllib.unquote_plus(params["series_id"])
   
    season_id=urllib.unquote_plus(params["season_id"])
    
   
    page = getData(url=DOMAIN+"/ajax/watch",timeout=0,postData="episodeList=true&serie="+series_id+"&season="+season_id);
    
    episodes=json.loads(page)
    if episodes is None or (len(episodes)==0):
        xbmcgui.Dialog().ok('Error occurred',"לא נמצאו פרקים לעונה")
        return
    print "Download sdarot series=" + series_id + " season=" + season_id + " #episodes=" + str(len(episodes))
    for i in range (0, len(episodes)) :
        epis= str(episodes[i]['episode'])
        finalVideoUrl,VID = getFinalVideoUrl(series_id,season_id,epis,silent=True)
        if finalVideoUrl == None :
            continue
        
        print "Downloading:" + str(finalVideoUrl)
        fileName = 'S' + str(season_id).zfill(2) + 'E' + str(epis).zfill(2) + '_' + str(VID) + '.mp4'
        download_path = os.path.join(path,str(series_id))
        if not os.path.exists(download_path):
            os.makedirs(download_path) 
        
        finalFileName = os.path.join(download_path,fileName)
        if not os.path.isfile(finalFileName):
            #progress = xbmcgui . DialogProgress ( )
            #progress.create ( "XBMC ISRAEL" , "Downloading " , '' , 'Please Wait' )
        
            try :
               #downloader . download ( finalVideoUrl , download_path , progress )
               downloaderParams = { "url": finalVideoUrl, "download_path": download_path }
               downloader.download(fileName, downloaderParams,async=True)
            except Exception, e:
                print str(e)
                pass
        
def sdarot_movie(url):
    series_id=urllib.unquote_plus(params["series_id"])
    series_name=urllib.unquote_plus(params["series_name"])
    season_id=urllib.unquote_plus(params["season_id"])
    image_link=urllib.unquote_plus(params["image"])
    episode_id=urllib.unquote_plus(params["episode_id"])
    title = series_name + "עונה " + season_id + " פרק" + episode_id
   
    finalUrl,VID = getFinalVideoUrl(series_id,season_id,episode_id)
    #print "finalUrl" + finalUrl
        
    player_url=DOMAIN+'/templates/frontend/blue_html5/player/jwplayer.flash.swf'
    liz = xbmcgui.ListItem(title, path=finalUrl, iconImage=params["image"], thumbnailImage=params["image"])
    liz.setInfo(type="Video", infoLabels={ "Title": title })    
    liz.setProperty('IsPlayable', 'true')
    #print finalUrl
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=liz)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=finalUrl, listitem=liz, isFolder=False)
                                  
params = getParams(sys.argv[2])
#print "params:"
#print params
url=None
name=None
mode=None
module=None
page=None

try:
        url=urllib.unquote_plus(params["url"])
       
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        module=urllib.unquote_plus(params["module"])
except:
        pass
try:
        page=urllib.unquote_plus(params["page"])
except:
        pass
    
if mode==None or url==None or len(url)<1:
    MAIN_MENU()

elif mode==2:
    INDEX_AZ(url,module)

elif mode==3:
    sdarot_series(url)

elif mode==4:
    sdarot_movie(url)

elif mode==5:
    sdarot_season(url)
elif mode==6:
	SearchSdarot(url,name)
elif mode==7:
    download_season(url)

xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)