# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from hot.ynet.co.il
"""
import urllib, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui

##General vars
__plugin__ = "Hot VOD"
__author__ = "Shai Bentin"

__image_path__ = 'http://ilvideo.googlecode.com/svn/trunk/'
__settings__ = xbmcaddon.Addon(id='plugin.video.hotVOD.video')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)

from common import *

def GENRES():
    addDir(__language__(30004), 'http://hot.ynet.co.il/', 5, __image_path__ + 'hot/genre/shows.png')
    addDir('ערוץ 8', 'http://hot.ynet.co.il/home/0,7340,L-7461,00.html', 5,'http://ilvideo.googlecode.com/svn/trunk/hot/genre/genre-1.png')
    addDir(' HOT 3', 'http://hot.ynet.co.il/home/0,7340,L-7456,00.html', 5,'http://upload.wikimedia.org/wikipedia/he/2/2c/Hot3.gif')
    addDir(' קומדי סנטרל', 'http://hot.ynet.co.il/home/0,7340,L-7479,00.html', 5,'http://ilvideo.googlecode.com/svn/trunk/hot/genre/genre-0.png')
    addDir(' הוט בידור ישראלי', 'http://hot.ynet.co.il/home/0,7340,L-7261,00.html', 5,'http://blog.tapuz.co.il/tvav/images/%7B9DF988F0-F567-4026-8EFD-94F0E46792D3%7D.jpg')
    addDir(' HOT VOD', 'http://hot.ynet.co.il/home/0,7340,L-7482,00.html', 5,'http://msc.wcdn.co.il/w/w-700/174718-5.jpg')
    addDir(' HOT VOD YOUNG', 'http://hot.ynet.co.il/home/0,7340,L-7449,00.html', 5,'http://ilvideo.googlecode.com/svn/trunk/hot/genre/genre-6.png')
    addDir('החיים הטובים', 'http://hot.ynet.co.il/home/0,7340,L-7421,00.html', 5,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRsTHHZMA4SabVhgHUM1ehzeMW7Q8QVbjCviGkRcv9Hf97CkTgZ')
    addDir('אופנה ישראלית', 'http://hot.ynet.co.il/home/0,7340,L-10312,00.html', 5,'http://msc.wcdn.co.il/w/w-700/1244322-5.jpg')
    xbmc.executebuiltin("Container.SetViewMode(500)")# see the image view
    
            
def SERIES(url):
    # receive the block of shows that are a part of this genre
    matches = getMatches('http://hot.ynet.co.il/', '<div id=\'links_column.*?</div></div></div>')
    
    if len(matches) > 0:
        series = re.compile('<div style=\'margin-bottom: 5px; text-align: right;\'><a href=\'(.+?)\'\s*>(.*?)<').findall(matches[int(url)])
        for href, name in series:
            name = name.replace('&nbsp;', ' ').replace('&quat;', '"').replace('&#39;', '\'')
            seriesId = re.compile('L-(\d+.*?),').findall(href)[0]
            iconImage = __image_path__ + 'hot/series/series_' + seriesId + '.jpg'
            if not os.path.exists(iconImage):
                iconImage = 'DefaultFolder.png'
            addDir(name, 'http://hot.ynet.co.il' + href, 2, iconImage)
            
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmc.executebuiltin("Container.SetViewMode(500)")# see the image view

def SHOWING_NOW(url):
    page = getData(url)
    #print page
    shows = re.compile('<tr height=25px>.*?<a href=\'(.*?)\'.*?>(.*?)</a>',re.I+re.M+re.U+re.S).findall(page)
    sorted_movies=[]
    #print shows
    for href, title in shows:
        title = title.replace('&nbsp;', ' ').replace('&quat;', '"').replace('&#39;', '\'')
        seriesId = re.compile('L-(\d+),').findall(href)[0]
        iconImage = __image_path__ + 'hot/series/series_' + seriesId + '.jpg'
        if not os.path.exists(iconImage):
            iconImage = 'DefaultFolder.png'
        sorted_movies.append(( title,'http://hot.ynet.co.il' + href,iconImage))
    sorted_movies = sorted(sorted_movies,key=lambda sorted_movies: sorted_movies[0])
    for movie in sorted_movies:
         addDir(movie[0], movie[1], 2, movie[2])
        
        
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    xbmc.executebuiltin("Container.SetViewMode(500)")# see the image view
            
def SEASONS(url):
    page = getData(url)
    if 'meta property="og:video"' in page :
        blockurl=re.compile('og:video(.*?)manifest').findall(page)
        #print blockurl
        directurl=re.compile('http(.*?)mp4').findall(blockurl[0])
        directurl=urllib.unquote('http'+directurl+'mp4')
        #print directurl
        listItem = xbmcgui.ListItem('video', 'DefaultFolder.png', 'DefaultFolder.png', path=directurl)
        listItem.setPath(directurl)        
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listItem)
        
    else:
        seriesId = re.compile('L-(\d+.*?),').findall(url)[0]
        if (seriesId.find('-') > -1):
            seriesId = seriesId[0:seriesId.index('-')]
        availSeasons = re.compile('<tr id=\'tr_\d\'(.*?)</tr>').findall(page)
        mainUrl = re.compile('AjaxItemsUrl:"(.+?)videoId').findall(page)
        if len(availSeasons) > 0:
            # if we have different menu items we need to extract names and actions....
            for item in availSeasons:
                menuItems = re.compile('topSrsLoadVidItems\((.+?)\);">.*?110px;\'>(.+?)<').findall(item)
                if len(menuItems) > 0:
                    urlId = '/Ext/Comp/Hot/TopSeriesPlayer_Hot/CdaTopSeriesPlayer_VidItems_Hot/0,13031,L-' + seriesId + '-' + menuItems[0][0] + '-0-0,00.html'
                    name = menuItems[0][1]
                else :
                    menuItems = re.compile('window.location=\'(.+?)\'">.*?class.*?>(.+?)<').findall(item)
                    if len(menuItems) > 0:
                        urlId = menuItems[0][0]
                        name = menuItems[0][1]
                if len(availSeasons)==1 and name.find('סרט') !=-1:
                  print 'name is' + str (name)
                  #addDir(name, 'http://hot.ynet.co.il' + urlId, 2, 'DefaultFolder.png', mainUrl[0])
                  addDir(name, url, 6, 'DefaultFolder.png',urlId)
                  #EPISODES2(url)
                    
                else:    
                    if not urlId == None and not name == None:
                        name = name.replace('&nbsp;', ' ').replace('&quat;', '"').replace('&#39;', '\'')
                        if urlId.find('/Ext/') !=-1:
                            addDir(name, 'http://hot.ynet.co.il' + urlId, 3, 'DefaultFolder.png', mainUrl[0])
                        else: # sometimes its just another link to a series page 
                            addDir(name, 'http://hot.ynet.co.il' + urlId, 2, 'DefaultFolder.png', mainUrl[0])
        
    
    
    #    else :     
    #         we only show the episodes on the page.
    #    print "got here"
    #    EPISODES2(url)

def EPISODES2(url,module):
    #print "hhhhhhh" + url
    page = getData('http://hot.ynet.co.il'+module)
    sections = re.compile('<table border=0 cellspacing=0 cellpadding=0 height=100%(.*?)</table></div>.*?</t').findall(page)
    #print sections
    if len(sections) > 0:
        for item in sections:
            images = re.compile('<img id=\'topSrsImg.*?src=\'(.+?)\'').findall(item)
            titles = re.compile('1;\'>(.+?)<').findall(item)
            details = re.compile('/div><font.*?topSrsUpdateStage\(\'small\',\d+\);">(.+?)</font').findall(item)
            urls = re.compile('topSrsUpdateStage.*?\(\'small\',(\d+)\)').findall(item)
            print "gagagagag"+ str (urls[0])
            if len(urls) > 0: # we must have a url to continue
                page = getData(url[:-8]+'-'+urls[0]+',00.html')
                
                if 'meta property="og:video"' in page :
                    
                    blockurl=re.compile('og:video(.*?)manifest').findall(page)
                    
                    directurl=re.compile('%3A%2F%2F(.*?)mp4').findall(blockurl[0])                    
                    print directurl
                    directurl=urllib.unquote('http://'+directurl[0]+'mp4')
                    directurl=directurl.replace('/z','')
                    listItem = xbmcgui.ListItem(name, 'DefaultFolder.png', 'DefaultFolder.png', path=directurl) 
                    listItem.setInfo( type="Video", infoLabels={ "Title":name} )
                    listItem.setPath(directurl)        
                    #print directurl
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listItem)
                    
        
        
         
         
def EPISODES(url, mainUrl):
    
    page = getData(url)
    if 'meta property="og:video"' in page :
        
        blockurl=re.compile('og:video(.*?)manifest').findall(page)
        directurl=re.compile('http(.*?)mp4').findall(blockurl[0])
        directurl=urllib.unquote('http'+directurl+'mp4')
        #print directurl
        listItem = xbmcgui.ListItem('video', 'DefaultFolder.png', 'DefaultFolder.png', path=directurl)
        listItem.setPath(directurl)        
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listItem)
        
    else:
        sections = re.compile('<table border=0 cellspacing=0 cellpadding=0 height=100%(.*?)</table></div>.*?</t').findall(page)
        if len(sections) > 0:
            for item in sections:
                images = re.compile('<img id=\'topSrsImg.*?src=\'(.+?)\'').findall(item)
                titles = re.compile('1;\'>(.+?)<').findall(item)
                details = re.compile('/div><font.*?topSrsUpdateStage\(\'small\',\d+\);">(.+?)</font').findall(item)
                urls = re.compile('topSrsUpdateStage.*?\(\'small\',(\d+)\)').findall(item)
                if len(urls) > 0: # we must have a url to continue
                    if len(images) == 0:
                        images = 'DefaultVideo.png'
                    else:
                        images = images[0]
                    if len(titles) == 0:
                        titles = __language__(30003)
                    else:
                        titles = urllib.unquote(titles[0])
                    if len(details) == 0:
                        details = ''
                    else:
                        details = urllib.unquote(details[0])
                    titles = titles.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', '\'')
                    addVideoLink(titles, 'http://hot.ynet.co.il' + mainUrl + urls[0] + '-0,00.html', 4, images, details)
            
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            xbmc.executebuiltin("Container.SetViewMode(500)")# see the image view
            print   'urls='+ str(urls[0])
            
def PLAY_MOVIE(url, name):
    page = getData(url, 0) #'http://hot.ynet.co.il/Cmn/App/Video/CmmAppVideoApi_AjaxItems/0,0,'+url+'-0,00.html'
    videoUrl = re.compile('path":"(.+?)"').findall(page)
    
    #http://ynethd-f.akamaihd.net/z/1112/hot/1411121445ima_veabaz_1_ynet.mp4/manifest.f4m
    videoUrl[0]=videoUrl[0][:-13]
    videoUrl[0]=videoUrl[0].replace('/z/','/').replace(' ','%20')
    
    
    if len(videoUrl) > 0:
        videoPlayListUrl = videoUrl[0]
        listItem = xbmcgui.ListItem(name, 'DefaultFolder.png', 'DefaultFolder.png', path=videoPlayListUrl) # + '|' + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        listItem.setPath(videoUrl[0])        
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listItem)
        
        
        
        
  
params = getParams(sys.argv[2])
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
    GENRES()

elif mode==1:
    SERIES(url)

elif mode==2:
    SEASONS(url)

elif mode==3:
    EPISODES(url, module)

elif mode==4:
    PLAY_MOVIE(url, name)

elif mode==5:
    SHOWING_NOW(url)   
elif mode==6:    
    EPISODES2(url,module)      
else:
        manager = getattr(__import__('module_' + module.lower()), 'manager_' + module)()
        manager.work(mode, url, name, page)
        


xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
