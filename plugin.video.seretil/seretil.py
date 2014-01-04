# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from seretil.me
"""
import urllib, urllib2, re, os, sys
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import urlresolver
from xml.sax import saxutils as su
import StorageServer
from xgoogle.search import GoogleSearch, SearchError



def searchInSeretil():
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
        keyboard.doModal()
        if keyboard.isConfirmed():
                    search_entered = keyboard.getText()

        if search_entered !='' :
                try:
                  gs = GoogleSearch("site:seretil.me "+ search_entered) 
                  gs.results_per_page = 100
                  results = gs.get_results()
                  for res in results:
                    title=res.title.encode('utf8')
                    url= res.url.encode('utf8')
                    title=title.replace('SERETIL.ME','')
                    title=title.replace('לצפייה ישירה','')
                    title=title.replace('וסדרות','')
                    title=title.replace('תרגום מובנה','')
                    title=title.replace('|','')
                    title=title.replace('.','')
                    title=title.replace('סרטים','')
                    title=title.replace('עם','')
                    title=title.replace('לצפיה','')
                    
                    
                    
                    
                    if 'עונה' in title   :
                                        if not 'page' in url  and not 'tag' in url  and not '?s' in url and not 'search' in url :
                                                addDir(title,url,211,'')
                    else:        
                                    if not 'page' in url  and not 'tag' in url  and not '?s' in url and not 'search' in url:
                                        image=''
                                        req = urllib2.Request(url)
                                        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                        response = urllib2.urlopen(req)
                                        link3=response.read()
                                        response.close()  
                                        
                                        block= re.compile('<div class="post-wrap post-wrap-single">(.*?)linkwithin_hook',re.M+re.I+re.S).findall(link3)
                                        image=''
                                        images= re.compile('src="http(.*?).?jpg').findall(block[0])
                                        if images:
                                                image='http'+images[0]+'.jpg'
                                        addDir(title,url,5,image)
                
                                    
                except SearchError, e:
                  print "Search failed: %s" % e
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

##General vars
__plugin__ = 'plugin.video.seretil'
__author__ = "Hillel"
__settings__ = xbmcaddon.Addon(id=__plugin__)
__language__ = __settings__.getLocalizedString
__cachePeriod__ = __settings__.getSetting("cache")
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
cacheServer = StorageServer.StorageServer("plugin.video.seretil",__cachePeriod__ )



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
    
 
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
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
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li id=.*?"><a href="(.*?)">(.*?)</a>').findall(link)
        for url,name in match:
                if name!="סדרות" :
                    addDir(name,url+'page/1/',4,"")


def SpecialPage(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<p>(.*?)</p>',re.M+re.I+re.S).findall(link)
        print match 
        for name in match:
                if (name.find('http') != -1 ):
                        print name
                        match=re.compile('a href="(.*?)"').findall(name)
                        if match:
                                if (match[0].find('multi')== -1) and (match[0].find('flyer') ==-1) :
                                        addDir('LINK',str(match[0]),212,'')
                                
                else :
                        if name !='&nbsp;' and name.find('לצעירים') ==-1 and name.find('span')==-1:
                                try:
                                        
                                        addLink('                 [COLOR red] '+ name+'[/COLOR]','','')
                                except:pass
                



def ResolverLink(url):
        url=urllib.unquote_plus(url)
        url = urlresolver.resolve(url)
        listitem = xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
        url=urllib.unquote_plus(url)
        listitem.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        
def LinksPage(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        sources =[]
        match=re.compile('<p><a href="(.*?)"').findall(link)
        for newurl in match:
            sources.append(urlresolver.HostedMediaFile(newurl))
         
        for item in sources:
                new_url = item.get_url()
                new_name=item.get_host()
                if new_name:
                        addDir(new_name,new_url,212,'')
        if not sources:
                match=re.compile('<div itemprop="description"><a href="(.*?)"').findall(link)
                if not match:
                        match=re.compile('<p><center><iframe src="(.*?)"').findall(link)
                

                if match :
                        addDir(name,match[0],212,'')
                


def INDEXchooseSeret(url):
        print url
        url2=url
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header ('Referer','http://seretil.me/')
        response = urllib2.urlopen(req,timeout=50)
        link=response.read()
        link2=link
        response.close()  
        cacheServer.table_name="seretilINDEXchooseSeret"
        cacheKey=str(url)
        movies=cacheServer.get(cacheKey)
        
        if  not movies:
                now=re.compile('class=\'current\'>(.*?)<').findall(link2)
                now_page =int(str(now[0]))
                movies=[]
                lastpage=re.compile('<span class=.?pages.?>(.*?)<').findall(link)
                lastpage= [int(s) for s in lastpage[0].split() if s.isdigit()][1]
                i= now_page
                stop=False
                dp = xbmcgui . DialogProgress ( )
		dp.create('please wait','בפעם הבאה זה ייטען הרבה יותר מהר קצת סבלנות')
                while i <= int(lastpage) and not stop  :
                        
                        percent= ((i%30)*3.44)
                        dp.update(int(percent),"בפעם הבאה זה ייטען הרבה יותר מהר קצת סבלנות","החילזון מהשפן")
                        link=OPEN_URL(url2)
                        match=re.compile('<h2 class="title"><a href="(.*?)".*?mark">(.*?)</a').findall(link)
                        
                        for url,name  in match:
                                '''req = urllib2.Request(url)
                                req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                link3=response.read()
                                response.close()  
                                image=None
                                images= re.compile('       <img width=".?.?.?" height=".?.?.?" src="(.*?)"').findall(link3)
                                if images==[]:'''
                                        
                                movies.append((name,url))
                                addDir(name,url,5,"")
                                    
                                '''else:
                                    movies.append((name,url,images[0]))    
                                    addDir(name,url,5,str(images[0]))'''
                        i+=1
                        url2 = url2[:-7]
                        if url2[len(url2)-1]=='p' :
                                url2= url2[:-1]
                        elif url2[len(url2)-2]=='p' :
                               url2= url2[:-2]
                               
                        url2=url2+'page/'+str(i)+'/'
                        if (i%30 ==0):
                                stop=True
                                addDir("תוצאות נוספות",url2,4,"")
                                movies.append(("more",url2))
                                
                                
                                                        
                dp.close()
                cacheServer.set(cacheKey, repr(movies))
                
        else:
           movies= eval (movies)
        
           for item in movies:
                    if item[0]=="more":
                            addDir("תוצאות נוספות",item[1],4,"")
                    else: 
                            addDir(item[0],item[1],5,"")
        try:                    
                xbmc.executebuiltin('Container.SetViewMode(51)')
        except:
                pass
               
def CATEGORIES():   
    mes()
    addDir(' [COLOR blue] חיפוש[/COLOR]','stam',18,'http://4.bp.blogspot.com/_ASd3nWdw8qI/TUkLNXmQwgI/AAAAAAAAAiE/XxYLicNBdqQ/s1600/Search_Feb_02_Main.png')
    addDir(' אוסף סרטים מדובבים' ,'http://seretil.me/%D7%90%D7%95%D7%A1%D7%A3-%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%9E%D7%93%D7%95%D7%91%D7%91%D7%99%D7%9D/',211,'http://seretil.me/wp-content/uploads/2013/08/Disney-Cartoon-wallpaper-classic-disney-14019958-1024-768-300x225.jpg')
    addDir('אוסף מספר 2 סרטים מדובבים' ,'http://seretil.me/%D7%90%D7%95%D7%A1%D7%A3-%D7%92%D7%93%D7%95%D7%9C-%D7%A9%D7%9C-%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%9E%D7%A6%D7%95%D7%99%D7%A8%D7%99%D7%9D%D7%9E%D7%93%D7%95%D7%91%D7%91%D7%99%D7%9D/',211,'http://seretil.me/wp-content/uploads/2012/05/images.jpg')
    INDEXSratim('http://seretil.me/')
        

def mes():

        
	try:
		link=OPEN_URL('http://goo.gl/cpGAcA')
		r = re.findall(r'ANNOUNCEMENTWINDOW ="ON"',link)
		if not r:
			return
			
		match=re.compile('<new>(.*?)\\n</new>',re.I+re.M+re.U+re.S).findall(link)
		if not match[0]:
			return
			
		version = __settings__.getAddonInfo('version')
		
		dire=os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), __plugin__)
		if not os.path.exists(dire):
			os.makedirs(dire)
		
		aSeenFile = os.path.join(dire, 'announcementSeen.txt')
		if (os.path.isfile(aSeenFile)): 
			f = open(aSeenFile, 'r') 
			content = f.read() 
			f.close() 
			if content == match[0] :
				return

		f = open(aSeenFile, 'w') 
		f.write(match[0]) 
		f.close() 

		dp = xbmcgui . Dialog ( )
		dp.ok("UPDATES", match[0])
	except:
		pass

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req,timeout=100)
    link=response.read()
    response.close()
    return link
     
print "checkMode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
       print ""
       CATEGORIES()
elif mode==4:
    INDEXchooseSeret(url)
     
elif mode==5:
     LinksPage(url)
elif mode==18:
        searchInSeretil()
elif mode==211:
         SpecialPage(url)
elif mode==212:
        ResolverLink(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
