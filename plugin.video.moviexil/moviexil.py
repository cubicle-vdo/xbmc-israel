# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from www.ynet.co.il
"""
import urllib, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
from xml.sax import saxutils as su

##General vars
__plugin__ = "MovieX-IL"
__author__ = "Cubicle"

__image_path__ = ''
# Don't forget to set lib/urlresolver/common.py
__settings__ = xbmcaddon.Addon(id='plugin.video.moviexil')
addon = __settings__ 
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__devel__ = 0
base_domain="http://www.moviex-il.com"

LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'lib' ) )
sys.path.append (LIB_PATH)

from common import *
from t0mm0.common.net import Net
from urlresolver import *
import urlresolver

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


def moviex_movie_categories(url):
  page=getData(url,0)
  #<a href="cat.php?cat=ילדים"><span class="menu">ילדים [<strong class="hma">114</strong>]</span></a>
  regexp='\"(cat\.php\?cat=.*?)\"><span class="menu">(.*?)\[<strong class="hma">(\d+)<\/strong>\]'
  matches = re.compile(regexp).findall(page)
  for match in matches:
      results_page=match[0]
      cat_name=match[1]
      cat_count=match[2]
      print "results_page="+results_page+"; cat_name="+cat_name+"; cat_count="+str(cat_count)
      addDir(cat_name + " ["+str(cat_count)+"]" ,base_domain+"/"+results_page,1,'')
  xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def moviex_series(url):
  page=getData(url,1)
  #<a href="ser.php?ser=האגדה%20של%20קורה">
	#		<img src="movpics/4feddfb532688.jpg" alt="seriesImage" />
	#		<span class="serName">האגדה של קורה</span>
  regexp='<a href=\"(ser\.php\?ser=.*?)\".*?src=\"(movpics\/.*?\....)\".*?ame\">(.*?)<\/span>'
  matches = re.compile(regexp).findall(page)
  for match in matches:
      series_page=match[0]
      icon=match[1]
      name=match[2]
      print "series_page="+series_page+"; icon="+icon+"; name="+str(name)
      addDir(name ,base_domain+"/"+series_page,'6&icon='+urllib.quote(icon),base_domain+'/'+icon)
  xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

def moviex_series_seasons(url):
  page=getData(url,7)
  #						<div class="bmovie4">
	#						<a href="ser.php?ser=24&se=1">עונה: 1</a>
	#					</div>
  regexp='<div class=\"bmovie4\">.*?<a href=\"(ser.php\?ser=.*?\&se=.*?)\">([^<>]*?)</a'
  icon=urllib.unquote_plus(params["icon"])
  matches = re.compile(regexp).findall(page)
  for match in matches:
      season_page=match[0]
      name=match[1]
      print "season_page="+season_page+"; icon="+icon+"; name="+str(name)
      addDir(name ,base_domain+"/"+season_page,'7&icon='+urllib.quote(icon),base_domain+'/'+icon)
  xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
  
def moviex_series_season(url):
  icon=urllib.unquote_plus(params["icon"])
  page=getData(url.replace(' ','+'),7)
  print page
  #<a href="series.php?serid=2889">פרק: 21</a>
  regexp='(series\.php\?serid\=.+?)">(.+?)</a>'
  matches = re.compile(regexp).findall(page)
  for match in matches:
      video_page=match[0]
      name=match[1]
      print "video_page="+video_page+"; icon="+icon+"; name="+str(name)
      addVideoLink(name ,base_domain+"/"+video_page,'2&icon='+urllib.quote(icon),base_domain+'/'+icon)
  xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
  
def moviex_video_types():
  if __devel__:
    addVideoLink('test-sockshare', 'http://www.sockshare.com/embed/67CF7956B246AB8E', 2, '' )
    addVideoLink('test-novamov', 'http://embed.novamov.com/embed.php?v=tverz6xc4slbe&px=1', 2, '' )
    addVideoLink('test-series-novamov', 'http://www.moviex-il.com/series.php?serid=2303', 2, '' )
    #http://www.youtube.com/embed/jzCYuflJWas
    addVideoLink('test-youtube', 'http://www.moviex-il.com/movie-%D7%A7%D7%95%D7%A4%D7%99%D7%9D-%D7%91%D7%97%D7%9C%D7%9C-2.html', 2, '' )
    addDir('search: תזיזו', 'תזיזו', 8, '' )
  addDir('סרטים','Movies',4,'')
  addDir('סדרות','http://www.moviex-il.com/page.php?s=seriesList',5,'')
  addDir('חיפוש סרטים','Movies',9,'')
      
def moviex_movies_page(url):
    page=getData(url,0)
    print page
    #<img class="LMimg" src="movpics/5057571d1d0a6.jpg" alt="pic" /></a>
    #				<span class="LMcat">ילדים</span>
    #				<a href="movie-%D7%91%D7%A8%D7%91%D7%99-%D7%9E%D7%A8%D7%9E%D7%93%D7%99%D7%94%3A-%D7%91%D7%AA-%D7%94%D7%99%D7%9D.html"><h3 class="movieNameIndex">ברבי מרמדיה: בת הים - Barbie Mermaidia</h3></a>
    #				<span class="LMdesc">בדרך לעיירת הפיות, אלינה (ברבי) הולכת לארץ בנות הים כדי להציל את חברה נאלו, נסיך בנות הים. נאלו נחטף ע&quot;י עוזרה של לברנה שתוכניותיו היו להשתמש בו כדי לחזק את לברנה על..</span>
		#<div style="text-align: left;">    
    #regexp='<div class="bmovie2">.*?<h2><a href="(.*?)">(.*?)</a></h2>.*?<img.*?class="picmovie" src="(.*?)" /></a>(.*?)<div class="ab'

    #	</div><h1>ילדים</h1><div style="text-align: center; padding: 2px;"><a href="?cat=ילדים&amp;page=1"><span class='numPages' style="color: #FFC409;">1</span></a><a href="?cat=ילדים&amp;page=2"><span class='numPages'>2</span></a><a href="?cat=ילדים&amp;page=3"><span class='numPages'>3</span></a><a href="?cat=ילדים&amp;page=4"><span class='numPages'>4</span></a><a href="?cat=ילדים&amp;page=5"><span class='numPages'>5</span></a><a href="?cat=ילדים&amp;page=6"><span class='numPages'>6</span></a><a href="?cat=ילדים&amp;page=7"><span class='numPages'>7</span></a><a href="?cat=ילדים&amp;page=8"><span class='numPages'>8</span></a><a href="?cat=ילדים&amp;page=9"><span class='numPages'>9</span></a><a href="?cat=ילדים&amp;page=10"><span class='numPages'>10</span></a><a href="?cat=ילדים&amp;page=11"><span class='numPages'>11</span></a><a href="?cat=ילדים&amp;page=12"><span class='numPages'>12</span></a><a href="?cat=ילדים&amp;page=13"><span class='numPages'>13</span></a>&nbsp;&nbsp;| <a href="?cat=ילדים&amp;page=2">הבא</a></div><div class="LastMovie" onClick="window.location='movie-%D7%94%D7%A6%27%D7%99%D7%95%D7%95%D7%90%D7%95%D7%95%D7%94-%D7%9E%D7%91%D7%95%D7%95%D7%A8%D7%9C%D7%99-%D7%94%D7%99%D7%9C%D7%A1-3%3A-%D7%95%D7%99%D7%95%D7%94-%D7%9C%D7%94-%D7%A4%D7%99%D7%90%D7%A1%D7%98%D7%94%21.html'">
		#			  	 <img class="LMimg" src="movpics/506d719d6c6d4.jpg" alt="pic" /><!--
		#			  --><span class="LMcat">קומדיה וילדים</span><!--
		#			  --><h3 class="movieNameIndex">הצ'יוואווה מבוורלי הילס 3: ויוה לה פיאסטה! - Beverly Hills Chihuahua 3: Viva La Fiesta!</h3><!--
		#			  --><span class="LMdesc">פאפי וקלואי, מצטרפים מהלך הרחל וסם למלון לנגהם המפואר, להשלים עם ספא מפואר כלבלב על ידי חמישה גורים השובבים ואת בעלים. אבל יש צרות כאשר רוזה, החבר הקטן ביותר של החבילה, מ..</span>
		#				 <div style="text-align: left;">
		#				 	<span class="LMdate">פורסם ב: 4/10/2012 &nbsp; ע"י crazy in love</span>
		#				 </div>
    regexp = '(movie-.*?\.html).*?class="LMimg" src="(.*?)".*?<h3 class="movieNameIndex">(.*?)</h3>.*?LMdesc">(.*?)</span>'  
    next_page_regexp='\|.<a\s+href="(.*?)">הבא</a></div'
    matches = re.compile(regexp,re.M+re.I+re.S).findall(page)
    for match in matches:
      image=match[1]
      page_link=match[0]
      name=match[2]
      description=match[3].strip()
      #print "page_link="+page_link+"\n"
      print "page_link="+page_link+"; name="+name+"; image="+image+"; description"+description+"\n"
      addVideoLink(name,base_domain+"/"+page_link,"2&name="+urllib.quote(name)+"&image="+urllib.quote(image)+"&description="+urllib.quote(description),base_domain+"/"+image, description)
    next_page_matches = re.compile(next_page_regexp).findall(page)
    if (len(next_page_matches) > 0):
      next_page_url=url
      idx = next_page_url.find("?")
      if ( idx != -1 ):
          next_page_url=next_page_url[0:idx]            
      #next_page_url=next_page_url+ su.unescape(next_page_matches[0])
      next_page_url=next_page_url+ su.unescape(next_page_matches[0])
      print "\nNext Page: "+next_page_url+" (matches="+next_page_matches[0]+")\n"
      addDir("עוד...",next_page_url,1,'')
    else:
      print "No next page. URL=" + url + "\n"
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def moviex_play_video(url):
    name = url
    if ("name" in params):
      name=params["name"]
    image=""
    if ("image" in params):
      image=params["image"]
    description=""
    if "description" in params:  
      description=params["description"]
    print "Resolving URL: " + url
    videoPlayListUrl = urlresolver.HostedMediaFile(url=url).resolve()
    if not videoPlayListUrl:
      print "URL " + url + " could not have been resolved to a movie.\n"
      return
    #addon.resolve_url(stream_url)
    #videoPlayListUrl = urllib.unquote(videoUrl[0])
    listItem = xbmcgui.ListItem(name, image, image, path=videoPlayListUrl) # + '|' + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    listItem.setInfo(type='Video', infoLabels={ "Title": name})
    listItem.setProperty('IsPlayable', 'true')
    print "video url " + videoPlayListUrl
    #xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(videoPlayListUrl)
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

def moviex_video_page(url):
    print "Calling getdata("+url+")\n"
    page = getData(url,0)
    regexp = "(<iframe.*?class=\"mVideo\".*?</iframe>)"  
    matches = re.compile(regexp).findall(page)
    curr_source = 0
    if len(matches) > 0:
      for match in matches:
        movie_url_matches = re.compile('src="(http:.*?)"').findall(match)
        for movie_url_match in movie_url_matches:
          movie_url = movie_url_match
          print "----- Match start -----\n"
          print "Video Link: "  + movie_url + "\n"
          print "----- Match end   -----\n"
          if ( len(matches) == 1):
            moviex_play_video(movie_url)
          else:
            moviex_play_video(movie_url)
            #curr_source=curr_source+1
            #addVideoLink("מקור "+str(curr_source),movie_url,3,'')
      return 
    else:
      print "No matches for "+regexp+"\n"
    regexp = ">(http://www.youtube.com.*?)</a>"  
    matches = re.compile(regexp).findall(page)
    curr_source = 0
    if len(matches) > 0:
      for match in matches:
          print "----- Match start -----\n"
          print "YouTube Link: "  + match + "\n"
          print "----- Match end   -----\n"
          moviex_play_video(match)
    else:
      print "No matches for "+regexp+"\n"
      
      
def moviex_search(url):
    opener = urllib2.build_opener()
    html = opener.open(base_domain+'/inc/rpc.php',urllib.urlencode({'queryString': url})).read()
    #<a href="movie-%D7%AA%D7%96%D7%99%D7%96%D7%95-%D7%90%D7%AA-%D7%94%D7%A8%D7%92%D7%9C%D7%99%D7%99%D7%9D.html">
		#								<img class="SMimg" src="movpics/5009c069e3f13.jpg" alt="img" />
		#							</a>
		#						</div>
		#						<div class="SMcontent">
		#						<span class="LMcat">ילדים, </span>
		#							<a href="movie-%D7%AA%D7%96%D7%99%D7%96%D7%95-%D7%90%D7%AA-%D7%94%D7%A8%D7%92%D7%9C%D7%99%D7%99%D7%9D.html">
		#								<h3 class="searchH3"><span class="searchheading SMhead">תזיזו את הרגליים...</span></h3>
		#							</a>
									#<span class="SMdesc">עלילת הסרט מתרחשת באימפריה הגדולה של הפינגווינים הקיסרים באנטרקטיקה.  הסיפור הוא על זן מסוים של פינג...</span></a>
    print html							
    regexp = 'class="SMimg" src="(.*?)".*?href="(movie-.*?\.html)".*?SMhead\">(.*?)</span></h3>.*?SMdesc">(.*?)</span></a>'  
    matches = re.compile(regexp, re.M+re.I+re.S).findall(html)
    for match in matches:
      page_link=match[1]
      image=match[0]
      name=match[2]
      description=match[3]
      addVideoLink(name,base_domain+"/"+page_link,2,base_domain+"/"+image, description)
def moviex_search_dialog(url):
    searchtext=""
    keyboard = xbmc.Keyboard(searchtext, 'חיפוש סרט')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        #searchtext = urllib.quote_plus()
        moviex_search(keyboard.getText())        

if mode==None:
    moviex_video_types()      
elif mode==1:
    moviex_movies_page(url)
elif mode==2:
    moviex_video_page(url)
elif mode==3:
    moviex_play_video(url)
elif mode==4:
    moviex_movie_categories(base_domain)
elif mode==5:
    moviex_series(url)
elif mode==6:
    moviex_series_seasons(url)
elif mode==7:
    moviex_series_season(url)
elif mode==8:
    moviex_search(url)
elif mode==9:
    moviex_search_dialog(url)
#
#elif mode==3:
#    EPISODES(url, module)
#
#elif mode==4:
#    PLAY_MOVIE(url, name)
#
#elif mode==5:
#    SHOWING_NOW(url)   
#          
#else:
#    GENRES()

xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
