# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from www.themarker.co.il
"""
import urllib, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import pyamf
import httplib
import array

from pyamf import remoting, amf3, util

__settings__ = xbmcaddon.Addon(id='plugin.video.themarker.video')
__cachePeriod__ = __settings__.getSetting("cache")

##General vars
__plugin__ = "TheMarker Video"
__author__ = "Cubicle"

__image_path__ = ''
__settings__ = xbmcaddon.Addon(id='plugin.video.themarker.video')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')


sections_regexp = '<a href=\"(/tv/\S*)\" class=\"child\">(.*?)<\/a>'
tv_mode_playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
tv_playlist_dedup = {}
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)

from common import *

def addMarkerVideoLink(name, url, mode, iconimage='DefaultFolder.png', summary = '', duration=''):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + name
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(name), "Plot": urllib.unquote(summary), "Duration": duration})    
        liz.setProperty('IsPlayable', 'true')
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
        return ok
    
def GENRES():
    # <a href="/tv/%D7%9E%D7%97%D7%90%D7%AA-%D7%94%D7%90%D7%95%D7%94%D7%9C%D7%99%D7%9D" class="child">מחאת האוהלים</a>
    
    # TV Mode
    addMarkerVideoLink("מצב TV", "http://www.themarker.com/tv", 2, 'http://www.themarker.com/images/logos/logo_tm_tv.png')
    
    # First Page
    SERIES("http://www.themarker.com/tv",0, 5, 5)
    
    # Analyze Sections
    page = getData("http://www.themarker.com/tv")    
    matches = re.compile(sections_regexp).findall(page)
    used="" 
    if len(matches) > 0:
      for match in matches:
        action = urllib.unquote(match[0])
        name = match[1]
        if used.find("|||"+name+"|||") == -1:
          addDir(name, "http://www.themarker.com"+action,1, 'http://www.themarker.com/polopoly_fs/7.2655217.1317803332!/image/3977573766.png_gen/derivatives/default/3977573766.png')
        used=used + "|||" + name + "|||"
            
def SERIES(url, item_pos = 0, min_items = 20, max_items_page = 9999,playlist_mode=0):
    # receive the block of shows that are a part of this genre
    params = getParams(sys.argv[2])
    item_pos_page=0
    #xbmc.log("url="+url)
    cache_timeout = 0
    if playlist_mode:
      cache_timeout = __cachePeriod__ 
    page=getData(url,cache_timeout)
    page_content=page[page.find('<div class="tmTeaser videoTeaser'):]
    # <img title='צבי סטפק - צילום:אייל טואג' height='102' alt='צבי סטפק - צילום:אייל טואג' width='136' src='/polopoly_fs/1.1638263.1332170860!/image/1421578058.jpg_gen/derivatives/landscape_136x102/1421578058.jpg' /></a></div>
    # <a class="caption" href="/tv/1.1724394" target="">  <span class="teaserTitleText">מגזין TheMarker מציג: חמישה טייקונים יצאו לדרך</span>
    match_url = re.compile("<div class=\"videoId\" style=\"display:none\">.*?<img .*?src='(.*?)' />.*?<a class=\"caption\" href=\"(.*?)\" target=.*?<span class=\"teaserTitleText\">(.*?)</span>.*?extraText\">(.*?)</div>").findall(page_content)
    
    if len(match_url) > 0:
      for match in match_url:
        image = "http://www.themarker.com"+match[0] 
        url_m = "http://www.themarker.com"+match[1]
        name = match[2]
        duration = match[3]
        item_pos = item_pos + 1
        item_pos_page = item_pos_page + 1
        if ( not playlist_mode ):
          addMarkerVideoLink(name, url_m, 4, image, '', duration)
        if item_pos_page >= max_items_page:
          if ( playlist_mode ):
            if ( not name in tv_playlist_dedup ):
              tv_playlist_dedup[name] = 1
              u = sys.argv[0] + "?url=" + urllib.quote_plus(url_m) + "&mode=4" + "&name=" + name
              liz = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
              liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(name),  "Duration": duration})    
              liz.setProperty('IsPlayable', 'true')
              xbmc.log("TV Mode: Adding to playlist: " + name)
              tv_mode_playlist.add(u, liz)
              return
            else:
              xbmc.log("TV Mode: Skipping [dedup]: " + name)
          break
      
      if ( playlist_mode ):
        return;

      # See if there is a next page
      m_next = re.compile("<a class=\"next\" href=\"(.*?)\"").findall(page)
      if len(m_next) > 0:
         if item_pos < min_items:
          SERIES("http://www.themarker.com"+m_next[0],item_pos, min_items, max_items_page)
         else:
          addDir("עוד...", "http://www.themarker.com"+m_next[0], 1, '') 
      xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
      xbmc.executebuiltin("Container.SetViewMode(500)")# see the image view

def TV_MODE(url):
     params = getParams(sys.argv[2])   
     page = getData("http://www.themarker.com/tv")    
     matches = re.compile(sections_regexp).findall(page)
     section_count = 0
     sections = {}
     sections_dedup = {}
     sections["000"] = "/tv" 
     if len(matches) > 0:
       for match in matches:
         section_count = section_count + 1 
         action = urllib.unquote(match[0])
         name = match[1]
         if ( not name in sections_dedup ):
            sections[str(section_count)+":"+name] = action
            sections_dedup[name] = 1 

     tv_mode_playlist.clear()         
     curr_idx = 0
     while (curr_idx < 7):
        curr_idx = curr_idx + 1
        for section in sections:
           if ( section == "000") & ( curr_idx > 5):
              continue
           action = sections[section]
           name = section
           #print "action = " + action + " name = " + str(name)
           SERIES("http://www.themarker.com"+action,0,curr_idx,curr_idx,1)
     xbmc.log("Running playlist...")
     xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(tv_mode_playlist)
                 
      
        
# Taken from freecable bio.py
def play(url):
   swfUrl = 'http://admin.brightcove.com/viewer/us20120705.1016/federatedVideoUI/BrightcovePlayer.swf'
   
   data = getData(url)
   match = re.compile('playerID".*?lue="(.+?)".*?playerKey".*?lue="(.+?)".*?videoPlayer".*?lue="(.+?)"').findall(data)
   if len(match):
      exp_id, key,content_id = match[0] 
   else:
      xbmc.log("TheMarker play(): Cannot parse address for URL" + url)
      return

   episode_info = get_episode_info(key, content_id, url, exp_id)  
   renditions = episode_info['programmedContent']['videoPlayer']['mediaDTO']['renditions']
   print "Renditions:"
   print renditions
   rtmp = ''
   hi_res = 0
   selected_video = None
   for video in renditions:
      if(int(video['encodingRate'])>hi_res):
         selected_video = video
         hi_res = int(video['encodingRate'])
   
   #rtmpdata = selected_video['defaultURL'].split('&mp4:')
   #rtmp = rtmpdata[0]+' playpath=mp4:'+rtmpdata[1]
   #rtmp += ' pageUrl='+url
   rtmp = selected_video['defaultURL']

   item = xbmcgui.ListItem(path=rtmp)
   return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def get_episode_info(key, content_id, url, exp_id):
   conn = httplib.HTTPConnection("c.brightcove.com")
   envelope = build_amf_request(key, content_id, url, exp_id)
   conn.request("POST", "/services/messagebroker/amf?playerKey="+key, str(remoting.encode(envelope).read()),{'content-type': 'application/x-amf'})
   response = conn.getresponse().read()
   response = remoting.decode(response).bodies[0][1].body
   conn.close()
   return response

class ViewerExperienceRequest(object):
   def __init__(self, URL, contentOverrides, experienceId, playerKey, TTLToken=''):
      self.TTLToken = TTLToken
      self.URL = URL
      self.deliveryType = float(0)
      self.contentOverrides = contentOverrides
      self.experienceId = experienceId
      self.playerKey = playerKey

class ContentOverride(object):
   def __init__(self, contentId, contentType=0, target='videoPlayer'):
      self.contentType = contentType
      self.contentId = contentId
      self.target = target
      self.contentIds = None
      self.contentRefId = None
      self.contentRefIds = None
      self.contentType = 0
      self.featureId = float(0)
      self.featuredRefId = None

def build_amf_request(key, content_id, url, exp_id):
   print 'key:'+key
   print 'ContentId:'+content_id
   print 'ExperienceId:'+exp_id
   print 'URL:'+url
   const = '5e953dada6862ed388075b269a11253eb52a15c4'
   pyamf.register_class(ViewerExperienceRequest, 'com.brightcove.experience.ViewerExperienceRequest')
   pyamf.register_class(ContentOverride, 'com.brightcove.experience.ContentOverride')
   content_override = ContentOverride(int(content_id))
   viewer_exp_req = ViewerExperienceRequest(url, [content_override], int(exp_id), key)

   env = remoting.Envelope(amfVersion=3)
   env.bodies.append(
      (
         "/1",
         remoting.Request(
            target="com.brightcove.experience.ExperienceRuntimeFacade.getDataForExperience",
            body=[const, viewer_exp_req],
            envelope=env
         )
      )
   )
   return env






try:
  pyamf.unregister_class('com.brightcove.experience.ViewerExperienceRequest')
  pyamf.unregister_class('com.brightcove.experience.ContentOverride')
except:
  s=1
  #


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
    TV_MODE(url)

elif mode==4:
    play(url)

elif mode==5:
    SHOWING_NOW(url)   
          
else:
        manager = getattr(__import__('module_' + module.lower()), 'manager_' + module)()
        manager.work(mode, url, name, page)
        


xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
