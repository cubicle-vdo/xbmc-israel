# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from 10q.tv
"""
import urllib, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
from xml.sax import saxutils as su
##General vars
__plugin__ = "www.10q.tv"
__author__ = "o2ri"
base_domain="www.10q.tv"
__settings__ = xbmcaddon.Addon(id='plugin.video.10qtv')

def geturl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    return link



# Returns an array of possible video url's from the page_url
def getURL( page_url , premium = False , user="" , password="", video_password="" ):
    # print("[vk.py] getURL(page_url='%s')" % page_url)

    # Lee la pagina y extrae el ID del video
    #data = scrapertools.cache_page(page_url.replace("amp;",""))
    data = geturl(page_url.replace("amp;",""))
    videourl = ""
    regexp =re.compile(r'vkid=([^\&]+)\&')
    match = regexp.search(data)
    vkid = ""
    if match is not None:
        vkid = match.group(1)
    else:
        print("no vkid")
    
    # Extrae los parametros del video y acade las calidades a la lista
    patron  = "var video_host = '([^']+)'.*?"
    patron += "var video_uid = '([^']+)'.*?"
    patron += "var video_vtag = '([^']+)'.*?"
    patron += "var video_no_flv = ([^;]+);.*?"
    patron += "var video_max_hd = '([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    video_urls = []

    if len(matches)>0:    
        for match in matches:
            if match[3].strip() == "0" and match[1] != "0":
                tipo = "flv"
                if "http://" in match[0]:
                    videourl = "%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                else:
                    videourl = "http://%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                
                # Lo acade a la lista
                video_urls.append( ["FLV [vk]",videourl])

            elif match[1]== "0" and vkid != "":     #http://447.gt3.vkadre.ru/assets/videos/2638f17ddd39-75081019.vk.flv 
                tipo = "flv"
                if "http://" in match[0]:
                    videourl = "%s/assets/videos/%s%s.vk.%s" % (match[0],match[2],vkid,tipo)
                else:
                    videourl = "http://%s/assets/videos/%s%s.vk.%s" % (match[0],match[2],vkid,tipo)
                
                # Lo acade a la lista
                video_urls.append( ["FLV [vk]",videourl])
                
            else:                                   #http://cs12385.vkontakte.ru/u88260894/video/d09802a95b.360.mp4
                #quality = config.get_setting("quality_flv")
                quality = "1"
                #Si la calidad elegida en el setting es HD se reproducira a 480 o 720, caso contrario solo 360, este control es por la xbox
                if match[4]=="0":
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                elif match[4]=="1":
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p [vk]",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])
                elif match[4]=="2":
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p [vk]",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])
                    video_urls.append( ["480p [vk]",get_mp4_video_link(match[0],match[1],match[2],"480.mp4")])
                elif match[4]=="3":
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p [vk]",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])
                    video_urls.append( ["480p [vk]",get_mp4_video_link(match[0],match[1],match[2],"480.mp4")])
                    video_urls.append( ["720p [vk]",get_mp4_video_link(match[0],match[1],match[2],"720.mp4")])
                else:
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p [vk]",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])

    for video_url in video_urls:
        print("%s - %s" % (video_url[0],video_url[1]))

    #return video_urls
    result = video_urls[len(video_urls)-1]
    return result[1]
    

def get_mp4_video_link(match0,match1,match2,tipo):
    if match0.endswith("/"):
        videourl = "%su%s/videos/%s.%s" % (match0,match1,match2,tipo)
    else:
        videourl = "%s/u%s/videos/%s.%s" % (match0,match1,match2,tipo)
    return videourl

  
     
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
        #<a href="/load/90210/173"> <div style="border: 1px solid black; border-radius: 10px; text-align: center; padding: 5px; background: #E5E5E5; margin: 2px;">
        #<img alt="" src="http://www.10q.tv/images/bg/90210small.jpg" height="317" width="214">  <br><b>90210</b>
        match=re.compile('top"><a href="(.*?)"> <div style.*?src="(.*?)" height=.*?<br><b>(.*?)<').findall(link)
        for url,thumb,name in match:
                addDir(name,base_domain+url,2,thumb)
                print (name,"url= "+ base_domain+url,"thumb= "+thumb)

def INDEXseason(url):
        print(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #><a href="http://www.10q.tv/load/abvdims/aavnha_1/41" class="catName">עונה 1</a>        
        print(link)
        match=re.compile('<a href="(.*?)" class="catName">(.*?)<').findall(link)
        for url,name in match:
                addDir(name,url,3,"")
                print (name,"url= "+ url)

#<h3 id="title"><a href="http://www.10q.tv/load/ahims_lnshk/aavnha_1/frk_02/141-1-0-1808">פרק 02</a> </h3>
def INDEXepisode(url):
        print(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()    
        print(link)
        #<h3 id="title"><a href="http://www.10q.tv/load/ahims_lnshk/aavnha_1/frk_02/141-1-0-1808">פרק 02</a> </h3>
        match=re.compile('id="title"><a href="(.*?)">(.*?)<').findall(link)
        for url,name in match:
                addDir(name,url,4,"")
                print (name,"url= "+ url)                
def CATEGORIES():
        addDir("סדרות",'http://www.10q.tv/load',1,"")
        addDir( "","",1,"")
        addDir( "","",1,"")
        addDir("","",1,"")

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
     INDEXepisode(url)
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



xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
