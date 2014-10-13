# -*- coding: utf-8 -*-


import urllib, urllib2, re, os, sys ,chardet
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import HTMLParser
##General vars
def geturl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    return link



# Returns an array of possible video url's from the page_url

def addLink(name,url,iconimage,description):
        url=urllib.unquote(url[7:])
        url="http://"+url.replace('amp;',"")
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    


#finalurl="http://vk.com/video_ext.php?oid=179599192&id=164903206&hash=ea095a7093bb4152&sd&quot"
def addFinalLink(finalurl,name):
    match = getURL(finalurl)
    addLink(name,match,"")
    xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)

def INDEXsdarot(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a class="aodInnerTitle".*?<b>(.*?)</b>(.*?)<tr style="margin-top:15px">',re.I+re.M+re.U+re.S).findall(link)
        #print "sdsdsd" +str(match[0]) +str(match[1])
        for result in  match:
           #print ("name:::"+ str(result[0]).decode(chardet.detect(str(result[0]))["encoding"]).encode("utf-8"),"url= "+ str(result[1]))
           addDir(str(result[0]).decode(chardet.detect(str(result[0]))["encoding"]).encode("utf-8"),str(result[1]),3,'')

def INDEXseason(url):
        print(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.*?)" class="catName">(.*?)<').findall(link)
        for url,name in match:
                name=name.encode("utf-8")
                print ("name:::"+ name,"url= "+ url)
                addDir(name,url,3,"")
                #print ("name:::"+ name,"url= "+ url)

def INDEXepisode(url,name):  
        print url +'llll'
        match=re.compile('title="(.*?)</a>.*?"schedule_code" style="display:none">(.*?)<',re.I+re.M+re.U+re.S).findall(url)
        print str(match) + 'kkkkkkkk'
        for  name2,num in match:
                #name2=name2.encode("utf-8")
                url='http://switch31-01.castup.net/cunet/gm.asp?ai=31&ar='+num+'&ak=null'
                addLink(str(name2).decode(chardet.detect(str(name2))["encoding"]).encode("utf-8"),url,"","")
                #print ("name:::"+ name,"url= "+ fff)            
                
def CATEGORIES():
        addDir("IBA",'http://www.iba.org.il/nagish/accessibility.aspx?siteCode=1',1,'http://icons.iconarchive.com/icons/thvg/popcorn/256/TV-Shows-icon.png')
        # addDir("סרטים",'http://www.10q.tv/board/filmy/3',5,'http://icons.iconarchive.com/icons/thiago-silva/palm/256/Videos-icon.png')
        
def IndexSeret(url):
        print(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('top"> <a href="(.*?)" class="sdarot">(.*?)</a>').findall(link)
        for url,name in match:
                addDir(name,"http://"+base_domain+url,6,"")
                print (name,"url= "+ base_domain+url)

def ChooseSeret(url):
        print(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()    
        pages=re.compile('return false;"><span>(.*?)</span></a>').findall(link)
        print pages
        pages=pages[-1]
        pages=pages.split("-")
        numOfItems = int(pages[1])
        print pages
        if numOfItems % 10 == 0:
            last =numOfItems // 10
        else:
            last= (numOfItems//10) +1

        i=1
        sorted_movies=[]
        while i <= last :
            req = urllib2.Request(url+"-"+str(i)+"-2")
            req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()     
            match=re.compile('<img src="http://www.10q.tv/_bd/(.*?)".*?<h4><a id="href" href="(.*?)">(.*?)</a> </h4>',re.I+re.M+re.U+re.S).findall(link)
            i=i+1
            for image,newurl,name in match:
            #    addDir(name,newurl,7,"http://www.10q.tv/_bd/"+image)
                sorted_movies.append(( "http://www.10q.tv/_bd/"+image,newurl,name))
                print (name,"url= "+ newurl)
        sorted_movies = sorted(sorted_movies,key=lambda sorted_movies: sorted_movies[2])
        for movie in sorted_movies:
            addDir(movie[2],movie[1],7,movie[0])
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        
        
         
def playMovie(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()    
        media=re.compile('<a href="(.*?)"<span style').findall(link)
        print ("the vk link is "+  str(media))
        addFinalLink(media[0],str(name))

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

print "checkMode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
       print ""
       CATEGORIES()
     
elif mode==1:
     print ""+url
     INDEXsdarot(url)

elif mode==2:
     print ""+url
     INDEXseason("http://"+url)       
elif mode==3:
     print ""+url
     INDEXepisode(url,name)
elif mode==4:
    print ""+url
    req = urllib2.Request(url)
    req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
   #<BR><a href="http://vk.com/video_ext.php?oid=181414759&id=164711282&hash=6d92e5c01d83b3b3&sd&quot      
    media=re.compile('a href="(.*?)&quot').findall(link)
    print ("the vk link is "+  str(media))
    addFinalLink(media[0],str(name))
elif mode==7:
    playMovie(url)
    
elif mode==5:
    IndexSeret(url)
elif mode==6:
    ChooseSeret(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
