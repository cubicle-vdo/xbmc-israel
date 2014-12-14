# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from seretil.me
"""
import urllib, urllib2, re, os, sys,htmlentitydefs
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import urlresolver, repoCheck

__plugin__ = 'plugin.video.seretil'
__author__ = "Hillel"
__settings__ = xbmcaddon.Addon(id='plugin.video.seretil')
__language__ = __settings__.getLocalizedString
Pages = int(__settings__.getSetting("pages"))
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
#cacheServer = StorageServer.StorageServer("plugin.video.seretil",__cachePeriod__ )

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
				INDEXSratim('http://seretil.me/?s='+str(search_entered))


##General vars




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
			url2=url
			req = urllib2.Request(url)
			req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
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
							
				link=OPEN_URL(url2)
				match=re.compile(regex,re.I+re.M+re.U+re.S).findall(link)
				print match
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
						#print   "test"  + url2
						addDir("תוצאות נוספות",url2,4,"")


def SpecialPage(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<p>(.*?)</p>',re.M+re.I+re.S).findall(link)
        #print match 
        for name in match:
                name=unescape(name) 
                if (name.find('<br />') ==-1) and (name.find('http') != -1 ):
                        #print name
                        match=re.compile('a href="(.*?)"').findall(name)
                        if match:
                                match=urlresolver.HostedMediaFile(match[0])
                                name=match.get_host()
                                new_url=match.get_url()
                                if name :
                                     addDir(name,new_url,212,'')
                                
                else :
                        if name !='&nbsp;' and name.find('לצעירים') ==-1 and name.find('span')==-1:
                           if (name.find('<br />') !=-1):
                               name=name[-2:]
                           try:
                                        
                                addLink('[COLOR red]'+'     '+ name+'[/COLOR]','','')
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
        #print url
        url2=url
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header ('Referer','http://seretil.me/')
        response = urllib2.urlopen(req,timeout=50)
        link=response.read()
        link2=link
        response.close()  
        
        
        now=re.compile('class=\'current\'>(.*?)<').findall(link2)
        now_page =int(str(now[0]))
        lastpage=re.compile('<span class=.?pages.?>(.*?)<').findall(link)
        lastpage= [int(s) for s in lastpage[0].split() if s.isdigit()][1]
        #print lastpage
        i= now_page
        stop=False
        dp = xbmcgui . DialogProgress ( )
        dp.create('please wait','בפעם הבאה זה ייטען הרבה יותר מהר קצת סבלנות')
        while i <= int(lastpage) and not stop  :
                        
            percent= ((i%10)*10)
            dp.update(int(percent),"סבלנות","טוען קטגוריה")
            link=OPEN_URL(url2)
            match=re.compile('<h2 class="title"><a href="(.*?)".*?mark">(.*?)</a').findall(link)
            
            for url,name  in match:
                name=unescape(name)
                req = urllib2.Request(url)
                req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link3=response.read()
                response.close()  
                image=None
                images= re.compile('       <img width=".?.?.?" height=".?.?.?" src="(.*?)"').findall(link3)
                if images==[]:
                     addDir(name,url,5,"")   
                                    
                else: 
                    addDir(name,url,5,str(images[0]))
                #addDir(name,url,5,"")
            #print name
            i+=1
            url2 = url2[:-7]
            if url2[len(url2)-1]=='p' :
                    url2= url2[:-1]
            elif url2[len(url2)-2]=='p' :
                   url2= url2[:-2]
                   
            url2=url2+'page/'+str(i)+'/'
            #print url2
            if (i%10 ==0):
                    stop=True
                    #print   "test"  + url2
                    addDir("תוצאות נוספות",url2,4,"")
                        
                        
                        
                                                
                
        try:                    
                xbmc.executebuiltin('Container.SetViewMode(51)')
        except:
                pass
               
def CATEGORIES():
    repoCheck.UpdateRepo()
    addDir(' [COLOR blue] חיפוש[/COLOR]','stam',18,'http://4.bp.blogspot.com/_ASd3nWdw8qI/TUkLNXmQwgI/AAAAAAAAAiE/XxYLicNBdqQ/s1600/Search_Feb_02_Main.png')
    addDir(' אוסף סרטים מדובבים' ,'http://seretil.me/%D7%90%D7%95%D7%A1%D7%A3-%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%9E%D7%93%D7%95%D7%91%D7%91%D7%99%D7%9D/',211,'http://seretil.me/wp-content/uploads/2013/08/Disney-Cartoon-wallpaper-classic-disney-14019958-1024-768-300x225.jpg')
    addDir('אוסף מספר 2 סרטים מדובבים' ,'http://seretil.me/%D7%90%D7%95%D7%A1%D7%A3-%D7%92%D7%93%D7%95%D7%9C-%D7%A9%D7%9C-%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%9E%D7%A6%D7%95%D7%99%D7%A8%D7%99%D7%9D%D7%9E%D7%93%D7%95%D7%91%D7%91%D7%99%D7%9D/',211,'http://seretil.me/wp-content/uploads/2012/05/images.jpg')
    addDir('מדובבים ראשי' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%9E%D7%93%D7%95%D7%91%D7%91%D7%99%D7%9D/page1/',4,'http://www.in-hebrew.co.il/images/logo-s.jpg')
    #INDEXSratim('http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%9E%D7%93%D7%95%D7%91%D7%91%D7%99%D7%9D/page1/')
    addDir('סרטי פעולה' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D/%D7%A4%D7%A2%D7%95%D7%9C%D7%94/page1/',4,'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQYK9pD6O3mwT5TqYXELuSzMHxVnMCRKjxWS-CMw85Ru3dSgafX1A')
    addDir('סרטי דרמה' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D/%D7%93%D7%A8%D7%9E%D7%94/page1/',4,'http://www.filmsite.org/images/drama-genre.jpg')
    addDir(' סרטי אימה' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D/%D7%90%D7%99%D7%9E%D7%94/page1/',4,'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRgtKPtptcB1sSLVy1KgnB9rXxnyAVFuhy2x7eqMBkXyfqIISIw2w')
    addDir(' סרטי מדע בדיוני' ,'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D/%D7%9E%D7%93%D7%A2-%D7%91%D7%93%D7%99%D7%95%D7%A0%D7%99/page1/',4,'http://i.telegraph.co.uk/multimedia/archive/01474/et_1474485b.jpg')
    addDir('נשיונל גאוגרפיק', 'http://seretil.me/category/%D7%A0%D7%A9%D7%99%D7%95%D7%A0%D7%9C-%D7%92%D7%99%D7%90%D7%95%D7%92%D7%A8%D7%A4%D7%99%D7%A7/page1/',4,'http://images.nationalgeographic.com/wpf/sites/common/i/presentation/NGLogo560x430-cb1343821768.png')
    addDir('2014', 'http://seretil.me/category/2014/page1/',4,'http://www.makingdifferent.com/wp-content/uploads/2013/12/2014-Numbers-Happy-2014-Wallpaper-New-Year-Image-1024x768.jpg')
    addDir('סרטים ישנים', 'http://seretil.me/category/%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%99%D7%A9%D7%A0%D7%99%D7%9D/page1/',4,'https://www.guthriegreen.com/sites/default/files/Back-to-the-Future.jpg')
    addDir('אנימציה -לא הכל מדובב', 'http://seretil.me/category/%D7%90%D7%A0%D7%99%D7%9E%D7%A6%D7%99%D7%94/page1/',4,'http://upload.wikimedia.org/wikipedia/en/thumb/c/c7/DreamWorks_Animation_SKG_logo.svg/1280px-DreamWorks_Animation_SKG_logo.svg.png')
    #addDir('[COLOR blue] סדרות [/COLOR]', 'http://seretil.me/category/112211/',4,'http://cdn3.tnwcdn.com/wp-content/blogs.dir/1/files/2011/12/itv-android-tablets.jpg')
    #addDir('', '/page1/',4,'')
    #addDir('', '/page1/',4,'')






def Series(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    #<li class="cat-item cat-item-23297"><a href="http://seretil.me/category/112211/%d7%94%d7%9c%d7%a7%d7%98%d7%a1/" >הלקטס</a></li>
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
     
print "checkMode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
       #print ""
       CATEGORIES()
elif mode==4:
    INDEXSratim(url)
     
elif mode==5:
     LinksPage(url)
elif mode==8:
     Series(url)
elif mode==18:
        searchInSeretil()
elif mode==211:
         SpecialPage(url)
elif mode==212:
        ResolverLink(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
