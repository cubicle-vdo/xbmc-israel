# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from www.yeladim.me
"""
import urllib, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui

##General vars
__plugin__ = "Yeladim.Me Video"
__author__ = "Cubicle"

__image_path__ = ''
__settings__ = xbmcaddon.Addon(id='plugin.video.yeladim.me')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)

from yeladimcommon import *

def message(self, title, message):
    dialog = xbmcgui.Dialog()
    dialog.ok(title , message)
    
def MAIN_MENU():
    addDir("הכל א-ת","all-heb",2,'');
    addDir("הכל a-z","all-eng",2,'');

def INDEX_AZ(url):
    page = getData('http://yeladim.me/videos');
    series_list = re.compile('<select name="c" id="order_category">(.*?)</select>').findall(page)[0]  
    matches = re.compile('<option value="(\d*?)">(.*?)</option>').findall(series_list)
    sr_arr = []
    idx = 0
    i=0
    if url == "all-eng":
      idx = 1
    for match in matches:
      m_arr = match[1].split(" / ")
      if (len(m_arr)>1) and (idx==1):
        sr_arr.append(( match[0], m_arr[1].strip() ))
      else:
        sr_arr.append(( match[0], m_arr[0].strip() ))
      i=i+1
    sr_sorted = sorted(sr_arr,key=lambda sr_arr: sr_arr[1])
      
    for key in sr_sorted:
      addDir(str(key[1]),"http://yeladim.me/videos?o=mr&type=&c="+str(key[0])+"&t=a",3,'')
      
def SEARCH(url):
    page = getData(url);
    #  <a href="/video/3534/24-עונה-1-פרק-23-24-s01e23"><img src="/media/videos/tmb/3534/1.jpg" title="24 עונה 1 פרק 23 / 24 S01E23" alt="24 עונה 1 פרק 23 / 24 S01E23"
    matches = re.compile('<a href="/video/(\d+)/(.*?)"><img src="(/media/videos/tmb/.*?)" title=".*?" alt="(.*?)"').findall(page)
    m_sorted = sorted(matches,key=lambda matches: matches[2])

    # Video ID
    # http://media.sdarot.tv/media/videos/flv/3495.flv?start=0
    for item in m_sorted:
        video_id = item[0]
        video_name = item[1]
        video_page_url="http://www.yeladim.me/video/"+str(video_id)+"/"+urllib.quote(video_name)
        image = "http://www.yeladim.me" + item[2]
        title = item[3]
        print "video_id"+str(video_id)+";video_name"+video_name+';image='+image+';title='+title+"\n"
        # Old format - straight to FLV
        #addVideoLink(title, 'http://media.yeladim.me/media/videos/flv/' + video_id + '.flv', '4&image='+urllib.quote(image)+'&title='+urllib.quote(title)+'&xtraparams='+urllib.quote('?start=0|User-Agent='+urllib.quote('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.60 Safari/537.1')), image, '')
        addVideoLink(title, video_page_url, '4&image='+urllib.quote(image)+'&title='+urllib.quote(title), image, '')
    
def play_movie(url):
    video_page = getData(url)
    # ('file', 'http://media.yeladim.me/media/videos/flv/262.flv') 
    # ('token', 'K49sS9q0')
    info_regex="'file', '(http:.+?)'.+\('token', '(.+?)'"
    matches = re.compile(info_regex).findall(video_page)
    if ( len(matches) > 0):
      flv_url = matches[0][0]
      token = matches[0][1]
      url2='http://www.yeladim.me/media/players/player.swf?file='+url+'&provider=http&fullscreen=true'
      #print 'url2='+url2
      #req = urllib2.Request(url2)
      #req.add_header('User-Agent', __USERAGENT__)        
      #response = urllib2.urlopen(req)
      #data = response.read()
      #response.close()
      #print str(data)
      flv_url = flv_url + '?start=0&token=' + token + '|User-Agent='+urllib.quote('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.60 Safari/537.1')+'&Referer='+urllib.quote(url2)    
      liz = xbmcgui.ListItem(params["title"], path=flv_url, iconImage=params["image"], thumbnailImage=params["image"])
      liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(params["title"]) })    
      liz.setProperty('IsPlayable', 'true')
      xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=liz)
      ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=flv_url, listitem=liz, isFolder=False)
    else:
      print "No matches in " + url + " for movie info " + info_regex
      message('Parse Error', 'Movie info could not be found')
      return    
      
    
 
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
    MAIN_MENU()

elif mode==2:
    INDEX_AZ(url)

elif mode==3:
    SEARCH(url)

elif mode==4:
    play_movie(url)

xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
