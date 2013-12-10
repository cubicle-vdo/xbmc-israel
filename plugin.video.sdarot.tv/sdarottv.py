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


ADDON = xbmcaddon.Addon(id='plugin.video.sdarot.tv')
##General vars        
__plugin__ = "Sdarot.TV Video"
__author__ = "Cubicle"

__image_path__ = ''
__settings__ = xbmcaddon.Addon(id='plugin.video.sdarot.tv')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)
from sdarotcommon import *


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


try:
    link=OPEN_URL('http://goo.gl/A1HFEi')
    match=re.compile('<domain>(.*?)</domain>',re.I+re.M+re.U+re.S).findall(link)
    DOMAIN=match[0]
except:
    pass
    DOMAIN='http://www.sdarot.co.in'

print DOMAIN


path = xbmc.translatePath(__settings__.getAddonInfo("profile"))
cookie_path = os.path.join(path, 'sdarot-cookiejar.txt')
print("Loading cookies from :" + repr(cookie_path))
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



def LOGIN():
    #print("LOGIN  is running now!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    loginurl = DOMAIN+'/login'
    if ADDON.getSetting('username')=='':
        dialog = xbmcgui.Dialog()
        xbmcgui.Dialog().ok('Sdarot','www.sdarot.tv התוסף דורש חשבון  חינמי באתר' ,' במסך הבא יש להכניס את שם המשתמש והסיסמא')
    
    if ADDON.getSetting('username')=='':
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'נא הקלד שם משתמש')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() 
        ADDON.setSetting('username',search_entered)
        
    if ADDON.getSetting('user_password')=='':
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'נא הקלד סיסמא')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText()
        ADDON.setSetting('user_password',search_entered)

    username = ADDON.getSetting('username')
    password = ADDON.getSetting('user_password')
    if not username or not password:
        print "Sdarot tv:no credencials found skipping login"
        return
    
    
    print "Trying to login to sdarot tv site username:" + username
    page = getData(url=loginurl,timeout=0,postData="username=" + username + "&password=" + password +"&submit_login=התחבר",referer=DOMAIN+"/");
   
 
def MAIN_MENU():
    
    # check's if login  is required.
    print "check if logged in already"
    page = getData(DOMAIN,referer="")
    match = re.compile('<span class="blue" id="logout"><a href="/log(.*?)">').findall(page)
    
    if len(match)!= 1 :
        print "login required"
        LOGIN()
    else:
        print "already logged in."
    addDir("הכל א-ת","all-heb",2,'');
    addDir("הכל a-z","all-eng",2,'');
    addDir("חפש",DOMAIN+"/search",6,'')
	
def SearchSdarot(url):
	search_entered = ''
	keyboard = xbmc.Keyboard(search_entered, "חפש כאן")
	keyboard.doModal()
	if keyboard.isConfirmed():
		search_entered = keyboard.getText()
	page = getData(url=url,timeout=0,postData="search=" + search_entered)
#	print page
	matches = re.compile('<a href="/watch/(\d+)-(.*?)">').findall(page)
	print matches

	#needs to remove duplicted result (originaly in site
	matches = [ matches[i] for i,x in enumerate(matches) if x not in matches[i+1:]]
	print matches
	for match in matches:
	  series_id = match[0]
	  link_name = match[1]
	  image_link=DOMAIN+"/media/series/"+str(match[0])+".jpg"
	  series_link=DOMAIN+"/watch/"+str(match[0])+"/"+match[1]
	  addDir(link_name,series_link,"3&image="+urllib.quote(image_link)+"&series_id="+series_id+"&series_name="+urllib.quote(link_name),image_link)
		
def INDEX_AZ(url):
    page = getData(DOMAIN+'/series');
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
    
    
    opener.addheaders = [('Referer',url)]
    opener.open(DOMAIN+'/landing/'+series_id).read()
  #  print "sdarot_series: Fetching URL:"+url  
    try:
        page = opener.open(url).read()
        print cookiejar
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
        addDir("עונה "+ str(season),url,"5&image="+urllib.quote(image_link)+"&season_id="+str(season)+"&series_id="+str(series_id)+"&series_name="+urllib.quote(series_id),image_link)
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
      
def sdarot_season(url):
    series_id=urllib.unquote_plus(params["series_id"])
    series_name=urllib.unquote_plus(params["series_name"])
    season_id=urllib.unquote_plus(params["season_id"])
    image_link=urllib.unquote_plus(params["image"])
    page = getData(url=DOMAIN+"/ajax/watch",timeout=0,postData="eplist=true&serie="+series_id+"&season="+season_id);
    episodes=page.split(",")
    for episode in episodes:
      if ( episode.find("-") != -1 ):
        episode=episode.replace("-0","")
      addVideoLink("פרק "+str(episode), url, "4&episode_id="+str(episode)+"&image="+urllib.quote(image_link)+"&season_id="+str(season_id)+"&series_id="+str(series_id)+"&series_name="+urllib.quote(series_id),image_link, '')         
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

def sdarot_movie(url):
    series_id=urllib.unquote_plus(params["series_id"])
    series_name=urllib.unquote_plus(params["series_name"])
    season_id=urllib.unquote_plus(params["season_id"])
    image_link=urllib.unquote_plus(params["image"])
    episode_id=urllib.unquote_plus(params["episode_id"])
    title = series_name + "עונה " + season_id + " פרק" + episode_id
    page = getData(url=DOMAIN+"/ajax/watch",timeout=1,postData="watch=true&serie="+series_id+"&season="+season_id+"&episode="+episode_id,referer=DOMAIN+"/watch")
   
    print "JSON:" 
    #print cookiejar
    try:
       
        #try to see if 
        prms=json.loads(page)
        if prms.has_key("error"):
            
            #encoding needed for hebrew to appear right
            error = str(prms["error"].encode("utf-8"))
        
            if len(error) > 0 :
                print "error:" + error +"\n"
                xbmcgui.Dialog().ok('Error occurred',error)
                return
        
        vid_url = str(prms["url"])
        print "vid_url: "+vid_url+"\n"
        VID = str(prms["VID"])
        print "VID: "+VID+"\n"
        
        
        vid_time = str(prms["time"])
        print "Time: "+ vid_time +"\n"
        token = str(prms["token_sd"])
        print "Token: "+token +"\n"        
    
    except Exception as e:
        print e
        raise

    if not token:
        xbmcgui.Dialog().ok('Error occurred',"התוסף לא הצליח לקבל אישור לצפייה, אנא נסה מאוחר יותר")
        return
    
    finalUrl = "http://" + vid_url + "/media/videos/sd/"+VID+'.mp4?token='+token+'&time='+vid_time
  
        
    player_url=DOMAIN+'/templates/frontend/blue_html5/player/jwplayer.flash.swf'
    liz = xbmcgui.ListItem(title, path=finalUrl, iconImage=params["image"], thumbnailImage=params["image"])
    liz.setInfo(type="Video", infoLabels={ "Title": title })    
    liz.setProperty('IsPlayable', 'true')
    #print finalUrl
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=liz)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=finalUrl, listitem=liz, isFolder=False)
                                  
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
    sdarot_series(url)

elif mode==4:
    sdarot_movie(url)

elif mode==5:
    sdarot_season(url)
elif mode==6:
	SearchSdarot(url)

xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
