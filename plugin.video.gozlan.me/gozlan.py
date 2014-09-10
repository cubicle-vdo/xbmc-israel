# -*- coding: utf-8 -*-

"""
	Plugin for streaming video content from gozlan.me
"""
import urllib, urllib2, re, os, sys, httplib
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
from xml.sax import saxutils as su
import urlresolver

##General vars
__plugin__ = "gozlan.me"
__author__ = "Cubicle"

__image_path__ = ''
__settings__ = xbmcaddon.Addon(id='plugin.video.gozlan.me')
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)
from gozlancommon import *

__icon__ = __settings__.getAddonInfo('icon')
__devel__ = 0

base_domain = __settings__.getSetting('domain')
isProxy = __settings__.getSetting('useProxy') == "true"

if isProxy:
	http_proxy = "http://anonymouse.org/cgi-bin/anon-www.cgi/"
	full_domain = "{0}{1}".format(http_proxy, base_domain)
	prefix = "{0}/".format(full_domain)
	no_prefix = ""
else:
	http_proxy = ""
	full_domain = base_domain
	prefix = ""
	no_prefix = "{0}/".format(full_domain)

#print full_domain

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

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):  
		return urllib.unquote_plus(headers["Location"])

	def http_error_302(self, req, fp, code, msg, headers):
		return urllib.unquote_plus(headers["Location"])
		
def GetMediaUrl(video_page_link):
	if isProxy:
		page = getData(video_page_link,3)
		regexp = 'location /\*\*/ = \'http://(.*?)\''
		matches = re.compile(regexp).findall(page)
		return "http://{0}".format(matches[0])
	else:
		httplib.HTTPConnection.debuglevel = 1
		opener = urllib2.build_opener(SmartRedirectHandler())
		request = urllib2.Request(video_page_link)
		video_page_link = opener.open(request)
		return video_page_link[video_page_link.find("http://", 7):]
	
def gozlan_movie_categories(url):
  page=getData(url+"/",0)
  #<li><a href="search.html?g=הרפתקאות">סרטי הרפתקאות</a></li>
  #regexp='<li><a href="search.html\?(\w+)=(.*?)">(.*?)</a></li>'
  regexp='<li><a href="{0}search.html\?(\w+)=(.*?)">(.*?)</a></li>'.format(prefix)
  matches = re.compile(regexp).findall(page)
  for match in matches:
	  results_cat=match[0]
	  results_crit=match[1]
	  results_page=match[0]+"="+urllib.quote(results_crit)
	  cat_name=match[2]
	  #print "results_page="+results_page+"; cat_name="+cat_name
	  addDir(cat_name,full_domain+"/search.html?"+results_page,"1&content=movies",'')
  xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def gozlan_series(url):
  page=getData(url,1)
  #<a href="ser.php?ser=האגדה%20של%20קורה">
	#		<img src="movpics/4feddfb532688.jpg" alt="seriesImage" />
	#		<span class="serName">האגדה של קורה</span>
	#<li style="width:153px"><div class="pic_top_movie2"><a href="vseries.html?id=127"><img src="http://gozlan.me/uploads/50c9cfb938aab.jpg" alt="The Voice ישראל לצפייה ישירה" /></a></div><div class="text_banner_top2"><a href="vseries.html?id=127">The Voice ישראל</a></div>
  regexp='<a href="({0}vser.*?)"><img src="(.*?)" alt=".*?<a href.*?">(.*?)</a></div>'.format(prefix)
  matches = re.compile(regexp).findall(page)
  for match in matches:
	  series_page=match[0]
	  icon=match[1]
	  name=match[2]
	  #print "series_page="+series_page+"; icon="+icon+"; name="+str(name)
	  addDir(name ,no_prefix+series_page,'6&icon='+urllib.quote(icon),icon)
  xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

def gozlan_series_seasons(url):
  page=getData(url,7)
  #						<div class="bmovie4">
	#						<a href="ser.php?ser=24&se=1">עונה: 1</a>
	#					</div>
  block_regexp='<h2>עונות:</h2>(.*?)<div class="foot" style="height:35px">'
  block_matches = re.compile(block_regexp).findall(page)
  #print block_matches[0]
  regexp='href="{0}search.html\?s=(.+?)">'.format(prefix)
  icon=urllib.unquote_plus(params["icon"])
  matches = re.compile(regexp).findall(block_matches[0])
  for match in matches:
	  season_page="search.html?s="+urllib.quote(match)
	  name=match
	  #print "season_page="+season_page+"; icon="+icon+"; name="+str(name)
	  addDir(name ,full_domain+'/'+season_page,'1&icon='+urllib.quote(icon),icon)
  xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    
def gozlan_video_types():
  if __devel__:
	addVideoLink('test-sockshare', 'http://www.sockshare.com/embed/67CF7956B246AB8E', 2, '' )
	addVideoLink('test-novamov', 'http://embed.novamov.com/embed.php?v=tverz6xc4slbe&px=1', 2, '' )
	addVideoLink('test-series-novamov', 'http://www.moviex-il.com/series.php?serid=2303', 2, '' )
	#http://www.youtube.com/embed/jzCYuflJWas
	addVideoLink('test-youtube', 'http://www.moviex-il.com/movie-%D7%A7%D7%95%D7%A4%D7%99%D7%9D-%D7%91%D7%97%D7%9C%D7%9C-2.html', 2, '' )
	addDir('search: תזיזו', 'תזיזו', 8, '' )
  addDir('סרטים',full_domain,4,'')
  addDir('סדרות',full_domain+'/series.html',5,'')
  addDir('חיפוש סרטים',full_domain,9,'')

def gozlan_search_page(url):
	content="tvshows"
	if "content" in params:  
	  content=params["content"]
	page_no=1
	if ("page_no" in params):
	  page_no=int(params["page_no"])
	next_page_no=str(page_no+1)
	page=getData(url,0)
	#print page
	#<div class="movie_pic"><a href="האי-של-נים-מדובב-לעברית--לצפייה-ישירה-3831.html"><img src="uploads/50c928afbc30c.jpg" width="105" height="156" alt="האי של נים-מדובב לעברית- לצפייה ישירה" /></a></div>
	regexp = '<div class="movie_pic">.*?<img src="(.*?)" width.*?<strong>.*?<h2><a href="(.*?)">(.*?)</a></h2>'
	matches = re.compile(regexp,re.M+re.I+re.S).findall(page)
	for match in matches:
	  image=match[0]
	  page_link=match[1]
	  name=match[2]
	  #print "page_link="+page_link+"\n"
	  #print "page_link="+page_link+"; name="+name+"; image="+image+"\n"
	  addDir(name,page_link,"2&conetnt="+urllib.quote(content)+"&name="+urllib.quote(name)+"&image="+urllib.quote(image),no_prefix+image, '')
	#class="pagenum"><a href="/search.html?s=%D7%9E%D7%93%D7%95%D7%91%D7%91&p=2">2</a>  
	next_page_regexp='<span class="currentSC">{0}</span><a href="(.+?)">{1}</a>'.format(page_no, next_page_no)
	next_page_matches = re.compile(next_page_regexp).findall(page)
	if (len(next_page_matches) > 0):
	  next_page_url=no_prefix+ su.unescape(next_page_matches[0])
	  #print "\nNext Page: "+next_page_url+" (matches="+next_page_matches[0]+")\n"
	  addDir("עוד...",next_page_url,"1&conetnt="+urllib.quote(content)+"&page_no="+next_page_no,'')
	else:
	  print "No next page. URL=" + url + ";regexp=" + next_page_regexp + "\n"
	xbmcplugin.setContent(int(sys.argv[1]), content)

def gozlan_play_video(url):
	try:
		url = GetMediaUrl(url)
		url = urlresolver.HostedMediaFile(url=url).resolve()
		if not url or len(url) < 1:
			raise
	except:
		print "Cannot play {0}.".format(url)
		xbmc.executebuiltin('Notification({0}, {1}, {2}, {3})'.format(__plugin__,  "Cannot play this source.", 5000, __icon__))
		return
	
	
	print "Playing {0}.".format(url)
	name = url
	if ("name" in params):
		name=params["name"]
	image=""
	if ("image" in params):
		image=params["image"]
	description=""
	if "description" in params:  
		description=params["description"]

	listItem = xbmcgui.ListItem(name, image, image, path=url)
	listItem.setInfo(type='Video', infoLabels={ "Title": name})
	listItem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

def gozlan_video_page(url):
	name = urllib.unquote(url)
	if ("name" in params):
		name=urllib.unquote(params["name"])
	image=""
	if ("image" in params):
		image=params["image"]
	description=""
	if "description" in params:  
		description=params["description"]
	content="tvshows"
	if "content" in params:  
		content=params["content"]
		
	#print "Calling getdata({0}{1})".format(no_prefix, url)
	
	page = getData(no_prefix+url,3)

	description= re.compile('<meta property="og:description" content="(.*?)"',re.M+re.I+re.S).findall(page)[0]
	regexp = 'quality_button">.*?<img.*?src="(.*?)" alt="(.*?)"\s*/></span><span class="quality_button">(.*?)</span><span\s+?class="playing_button"><a.*?href="(.*?)"'
	matches = re.compile(regexp).findall(page)

	if len(matches) > 0:
		for match in matches:
			provider_image=match[0]
			if ( provider_image.find("http:") == -1 ):
				provider_image=full_domain+"/"+provider_image
			provider_name=match[1]
			provider_quality=match[2]
			video_page_link=match[3]

			addVideoLink("[B]{2}[/B] {0} דרך {1} - ".format(name, provider_name, provider_quality), video_page_link, "3&name={0}&image={1}&description={2}".format(urllib.quote(name), urllib.quote(image), urllib.quote(description)), "{0}/{1}".format(full_domain, image), description)
	else:
		print "No matches for {0}".format(regexp)

	'''
	regexp = 'quality_button.*?<strong.*?>(.*?)</strong></span>.*?_button">(.*?)</span><span class="playing_button"><a  href="(.*?)"'  
	matches = re.compile(regexp).findall(page)

	if len(matches) > 0:
		for match in matches:
			provider_image=""
			provider_name=match[0]
			provider_quality=match[1]
			video_page_link=match[2]

			addVideoLink("{0} דרך {1} [[B]{2}[/B]]".format(name, provider_name, provider_quality), video_page_link, "3&name={0}&image={1}&description={2}".format(urllib.quote(name), urllib.quote(image), urllib.quote(description)), "{0}/{1}".format(full_domain, image), description)
	else:
		print "No matches for {0}".format(regexp)
	'''
		
	xbmcplugin.setContent(int(sys.argv[1]), content)
	   
def gozlan_search_dialog(url):
	searchtext=""
	keyboard = xbmc.Keyboard(searchtext, 'חיפוש סרט')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		#searchtext = urllib.quote_plus()
		gozlan_search_page(full_domain+"/search.html?s="+keyboard.getText())		


if mode==None:
	gozlan_video_types()	  
elif mode==1:
	gozlan_search_page(url)
elif mode==2:
	gozlan_video_page(url)
elif mode==3:
	gozlan_play_video(url)
elif mode==4:
	gozlan_movie_categories(url)
elif mode==5:
	gozlan_series(url)
elif mode==6:
	gozlan_series_seasons(url)
elif mode==9:
	gozlan_search_dialog(url)


xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
