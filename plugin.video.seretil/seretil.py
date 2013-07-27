# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from seretil.me
"""
import urllib, urllib2, re, os, sys
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import urlresolver
from xml.sax import saxutils as su
##General vars
__plugin__ = "www.seretil.me"
__author__ = "o2ri"
__settings__ = xbmcaddon.Addon(id='plugin.video.seretil')



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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def INDEXSratim(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #<li id="menu-item-35114" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-35114"><a href="http://seretil.me/category/%d7%a7%d7%95%d7%9e%d7%93%d7%99%d7%94/">קומדיה</a></li>
        match=re.compile('<li id=.*?"><a href="(.*?)">(.*?)</a>').findall(link)
        for url,name in match:
                if name!="סדרות" :
                    addDir(name,url+'page/1/',4,"")
              

def LinksPage(url):
        print(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #<p><a href="http://www.fileflyer.com/view/TGCZAGG36ZP7Cn" class="autohyperlink" title="http://www.fileflyer.com/view/TGCZAGG36ZP7Cn" target="_blank" rel="nofollow">www.fileflyer.com</a></p>
      #  print(link)
        sources =[]
        match=re.compile('<p><a href="(.*?)"').findall(link)
        for newurl in match:
            sources.append(urlresolver.HostedMediaFile(newurl))
         
        i=1
        for source in sources:
            if source :
                 try :
                     stream_url = source.resolve()
                     addLink("link " + str(i) ,stream_url,"")
                     i=i+1    
                 except:pass
            else:
                print("not playble")
                url=None
        xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)

#<h3 id="title"><a href="http://www.10q.tv/load/ahims_lnshk/aavnha_1/frk_02/141-1-0-1808">פרק 02</a> </h3>
def INDEXchooseSeret(url):
        print(url)
        url2=url
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link2=link
        response.close()    
    #    print(link)
        #<h2 class="title"><a href="http://seretil.me/%d7%98%d7%a0%d7%92%d7%95-%d7%95%d7%a7%d7%90%d7%a9-1989-%d7%aa%d7%a8%d7%92%d7%95%d7%9d-%d7%9e%d7%95%d7%91%d7%a0%d7%94/" title="Permalink to טנגו וקאש (1989) תרגום מובנה לצפייה ישירה" rel="bookmark">טנגו וקאש (1989) תרגום מובנה לצפייה ישירה</a></h2>

        match=re.compile('<h2 class="title"><a href="(.*?)".*?mark">(.*?)</a').findall(link)
        for url,name  in match:
                req = urllib2.Request(url)
                req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link3=response.read()
                response.close()  
                image=None
                images= re.compile('       <img width=".?.?.?" height=".?.?.?" src="(.*?)"').findall(link3)
                print ("images====" +str(images))
                if images==[]:
                    addDir(name,url,5,"")
                    print (name,"url= "+ url +"special one !!!!!!!")
                else:
                    addDir(name,url,5,str(images[0]))
        now=re.compile('class=\'current\'>(.*?)<').findall(link2)
        next_page=re.compile('<span class=.?pages.?>(.*?) מתוך').findall(link2)
        int_now_page =int(str(now[0])) +1
        url2 = url2[:-7]
        if url2[len(url2)-1]=='p' :
            url2= url2[:-1]
        url2=url2+'page/'+ str(int_now_page)+'/'
        print("url the next ",url2)
        addDir("עוד תוצאות",url2,4,"")
        addDir("חזרה לתפריט ראשי",'www.stam.com',None,"");
               
def CATEGORIES():

    INDEXSratim('http://seretil.me/')

   

print "checkMode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
       print ""
       CATEGORIES()
elif mode==4:
    INDEXchooseSeret(url)
     
elif mode==5:
     print ""+url
     LinksPage(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
