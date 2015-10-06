# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from seretil.me
"""
import urllib, urllib2, re, os, sys
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import urlresolver, repoCheck, AntiDDOSProtectcion
from z_t0mm0_common_net import Net
net2=Net()

__plugin__ = 'plugin.video.seretil'
__author__ = "Hillel"
__settings__ = xbmcaddon.Addon(id=__plugin__)
__language__ = __settings__.getLocalizedString
Pages = int(__settings__.getSetting("pages"))
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
addonPath = __settings__.getAddonInfo('path')
user_dataDir = xbmc.translatePath(__settings__.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)

def unescape(text):
	try:			
		rep = {"&nbsp;": " ",
			  "\n": "",
			  "\t": "",
			  "\r":"",
			  "&#39;":"",
			  "&quot;":"\"",
			  "&#8211;":"-",
			  "Permalink to":"",
			  "#039;":"",
			  "&":"'",
			  "תרגום מובנה":"",
			  "לצפייה":"",
			  "ישירה":"",
			  "*":"",
			  "לצפייה ישירה":""
			  }
		for s, r in rep.items():
			text = text.replace(s, r)
			
		# remove html comments
		text = re.sub(r"<!--.+?-->", "", text)	
			
	except TypeError:
		pass

	return text

def searchInSeretil():
	search_entered =''
	keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
	keyboard.doModal()
	if keyboard.isConfirmed():
				search_entered = keyboard.getText()

	if search_entered !='' :
		INDEXSratim('http://seretil.me/?s='+search_entered.replace(' ','+'))


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
					params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
							param[splitparams[0]]=splitparams[1]
							
	return param
	
params=get_params()
url=None
iconimage=None
name=None
mode=None
module=None
page=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
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
    
 
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if mode==212:
                liz.setProperty("IsPlayable","true")
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def INDEXSratim(url):
			url2=url
			'''req = urllib2.Request(url)
			req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()'''
			link=nURL(url).encode('utf-8')
			match=re.compile('entry-thumbnails-link".*?href="(.*?)">.*?src="(.*?)".*?bookmark">(.*?)</a>').findall(link)
			now=re.compile('class=\'current\'>(.*?)<').findall(link)
			try:
			   now_page =int(str(now[0]))
			except:now_page=1
			lastpage=re.compile('<span class=.?pages.?>(.*?)<').findall(link)
			if lastpage:
				lastpage= [int(s) for s in lastpage[0].split() if s.isdigit()][1] 
			else:
				lastpage=2
			i= now_page
			stop=False
			dp = xbmcgui . DialogProgress ( )
			dp.create('please wait','סבלנות')
			oldPage='sf-menu menu clearfix' in link
			if oldPage:
				regex='href="(.*?)">.*?src="(.*?)".*?bookmark">(.*?)</a>'
			else:
				regex='<div class="entry clearfix">.*?<a href="(.*?)".*?title="(.*?)".*?src="(.*?)"'
				
			while i <= int(lastpage) and not stop  :
				link=nURL(url2).encode('utf-8')
				match=re.compile(regex,re.I+re.M+re.U+re.S).findall(link)
				#print match
				for url,image,name in match:
					name=unescape(name)
					image=unescape(image)
					if name!="סדרות" :
						if oldPage:
							addDir(name,url,211,image)
						else:
							addDir(image,url,211,name)
				
				i+=1
				url2 = url2[:-6]
				if url2[len(url2)-1]=='p' :
						url2= url2[:-1]
				elif url2[len(url2)-2]=='p' :
					   url2= url2[:-2]
					   
				url2=url2+'page/'+str(i)+'/'
				#print url2
				if (i%Pages ==0):
					stop=True
					addDir('[COLOR blue]'+'תוצאות נוספות'+'[/COLOR]',url2,4,"")


def SpecialPage(url,moviename,iconimage):
	'''req = urllib2.Request(url)
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()'''
	link=nURL(url).encode('utf-8')
	match=re.compile('<span id(.*?)<\/script>',re.M+re.I+re.S).findall(link)
	match =match[0]
	name=unescape(match) 
	result=re.compile('a href="(.*?)"').findall(name)
	if result:
		addLink('[COLOR red]'+'  '+ moviename+'[/COLOR]','',iconimage)
		addLink('[COLOR red]'+'   בחר מקור לניגון,אם לא עובד נסה אחר '+'[/COLOR]','',iconimage)
		for item in result :
			final=urlresolver.HostedMediaFile(item)
			new_url=final.get_url()
			source=re.compile('http://(.*?)\/').findall(new_url)
			if final:
				addDir('[COLOR blue]'+str(source[0]) + '[/COLOR]' +  moviename +'----' ,new_url,212,iconimage)
                                
                

def ResolverLink(url):
	url=urllib.unquote_plus(url)
	url = urlresolver.resolve(url)
	listitem = xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
	url=urllib.unquote_plus(url)
	listitem.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


def CATEGORIES():
	addDir(' [COLOR blue] חיפוש[/COLOR]','stam',18,'http://4.bp.blogspot.com/_ASd3nWdw8qI/TUkLNXmQwgI/AAAAAAAAAiE/XxYLicNBdqQ/s1600/Search_Feb_02_Main.png')
	addDir('מדובבים ראשי' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%9E%D7%93%D7%95%D7%91%D7%91%D7%99%D7%9D/page1/',4,'http://www.in-hebrew.co.il/images/logo-s.jpg')
	addDir('אנימציה -לא הכל מדובב', 'http://seretil.me/category/%D7%90%D7%A0%D7%99%D7%9E%D7%A6%D7%99%D7%94/page1/',4,'http://upload.wikimedia.org/wikipedia/en/thumb/c/c7/DreamWorks_Animation_SKG_logo.svg/1280px-DreamWorks_Animation_SKG_logo.svg.png')
	#INDEXSratim('http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%9E%D7%93%D7%95%D7%91%D7%91%D7%99%D7%9D/page1/')
	addDir('סרטי פעולה' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D/%D7%A4%D7%A2%D7%95%D7%9C%D7%94/page1/',4,'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQYK9pD6O3mwT5TqYXELuSzMHxVnMCRKjxWS-CMw85Ru3dSgafX1A')
	addDir('סרטי דרמה' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D/%D7%93%D7%A8%D7%9E%D7%94/page1/',4,'http://www.filmsite.org/images/drama-genre.jpg')
	addDir(' סרטי אימה' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D/%D7%90%D7%99%D7%9E%D7%94/page1/',4,'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRgtKPtptcB1sSLVy1KgnB9rXxnyAVFuhy2x7eqMBkXyfqIISIw2w')
	addDir(' סרטי מדע בדיוני' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D/%D7%9E%D7%93%D7%A2-%D7%91%D7%93%D7%99%D7%95%D7%A0%D7%99/page1/',4,'http://i.telegraph.co.uk/multimedia/archive/01474/et_1474485b.jpg')
	addDir('נשיונל גאוגרפיק', 'http://seretil.me/category/%D7%A0%D7%A9%D7%99%D7%95%D7%A0%D7%9C-%D7%92%D7%99%D7%90%D7%95%D7%92%D7%A8%D7%A4%D7%99%D7%A7/page1/',4,'http://images.nationalgeographic.com/wpf/sites/common/i/presentation/NGLogo560x430-cb1343821768.png')
	addDir('2012', 'http://seretil.me/category/2012/page1/',4,'http://farm8.staticflickr.com/7171/6603724951_7b352bda71.jpg')
	addDir('2013', 'http://seretil.me/category/2013/page1/',4,'http://investorplace.com/wp-content/uploads/2012/12/2013-year-630-300x227.jpg')
	addDir('2014', 'http://seretil.me/category/2014/page1/',4,'http://mountainmessenger.com/wp-content/uploads/2014/12/sparkling_2014_lights-300x187.jpg')
	addDir('2015', 'http://seretil.me/category/2015/page1/',4,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcT61KOSCwfNWb4VXqsfQTCkd-eF0R_O16FF4d4fdiyqOXhJUswB')
	addDir('סרטים ישנים', 'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%99%D7%A9%D7%A0%D7%99%D7%9D/page1/',4,'https://www.guthriegreen.com/sites/default/files/Back-to-the-Future.jpg')
   

def Series(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    matches=re.compile('http://seretil.me/category/112211/(.*?)/" >(.*?)</a').findall(link)
    for match in matches:
       addDir(match[1], 'http://seretil.me/category/112211/'+str(match[0]),4,'')



def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req,timeout=100)
    link=response.read()
    response.close()
    return link
   
def _OpenFile(path):
	if os.path.isfile(path): ## File found.
		file = open(path, 'r')
		contents=file.read()
		file.close()
		return contents
	else: return '' ## File not found.
	
def _SaveFile(path, data):
	file = open(path,'w')
	file.write(data)
	file.close()
	
def nURL(url):
	if url=='': return ''
	User_Agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
	AntiTag='<iframe style="display:none;visibility:hidden;" src="http://my.incapsula.com/public/ga/jsTest.html" id="gaIframe"></iframe>'
	dhtml=''
	html=' '+AntiTag+' '
	net2.set_user_agent(User_Agent)
	xTimes=0
	while (AntiTag in html):
		xTimes=xTimes+1
		try: 
			html=net2.http_GET(url).content
		except urllib2.URLError,e: 
			html=dhtml
			try:
				if str(e.code)=='503':
					CFCookie=str(AntiDDOSProtectcion.decryptCFDDOSProtection(url,User_Agent,'',AddonID=__plugin__))
					cf_cookie_file=os.path.join(user_dataDir,'temp.cache.txt')
					if (str(CFCookie)=='None') or (len(str(CFCookie))==0): pass
					else:
						try: 
							my_cookies=_OpenFile(cf_cookie_file)
							if len(my_cookies)==0: my_cookies='#LWP-Cookies-2.0'
							else:
								s='\n*\r*\n*(Set-Cookie3: %s=.+? HttpOnly\s*\r*\n*\r*)'
								try:		
									cfOldA=re.compile(s%'__cfduid').findall(my_cookies)[0]
								except: cfOldA=''
								if len(cfOldA) > 0: my_cookies=my_cookies.replace(cfOldA,'')
								try:		cfOldB=re.compile(s%'cf_clearance').findall(my_cookies)[0]
								except: cfOldB=''
								if len(cfOldB) > 0: my_cookies=my_cookies.replace(cfOldB,'')
								
								gg=['\r*\n(=None; version=0\r*\n)','\r*\n(=None; version=None\r*\n)']
								for g in gg:
									try:		cfOldC=re.compile(g).findall(my_cookies)[0]
									except: cfOldC=''
									if len(cfOldC) > 0: my_cookies=my_cookies.replace(cfOldC,'')
								
								my_cookies=my_cookies.replace('\r\r\n\r\r\n','\r\r\n').replace('\n\n\r\n\n\r','\n\n\r').replace('\r\n\r\n','\r\n').replace('\n\n','\n').replace('\r\r','\r').replace('\r\a\r\a','\r\a').replace('\n\n','\n').replace('\n\a\n\a','\n\a').replace('\a\a','\a')
							_SaveFile(cf_cookie_file,my_cookies+''+str(CFCookie))

							net2.set_cookies(cf_cookie_file)
							net2.set_user_agent(User_Agent)
							html=net2.http_GET(url).content

							return html

						except: pass
				return dhtml
			except Exception, e: 
				print e
				return dhtml
				pass
		except Exception, e: 
			html=dhtml
		except: 
			html=dhtml
		if xTimes > 5: 
			html=html.replace(AntiTag,'')
		elif AntiTag in html: 
			xbmc.sleep(4000)

	return html
		
	
print "checkMode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
       repoCheck.UpdateRepo()
       CATEGORIES()
elif mode==4:
	INDEXSratim(url)
elif mode==8:
	Series(url)
elif mode==18:
	searchInSeretil()
elif mode==211:
	SpecialPage(url,name, iconimage)
elif mode==212:
	ResolverLink(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
