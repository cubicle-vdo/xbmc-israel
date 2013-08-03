# -*- coding: utf-8 -*-

import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import urlresolver
import t0mm0.common.net
from t0mm0.common.net import Net


ADDON = xbmcaddon.Addon(id='plugin.video.searchil')


def geturl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    return link



# Returns an array of possible video url's from the page_url
def getURL( page_url , premium = False , user="" , password="", video_password="" ):
    
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

 #      addDir('name','url','mode','iconimage','description') mode is where it tells the plugin where to go scroll to bottom to see where mode is
def CATEGORIES():
        addDir('חפש ב seretonline.co','http://seretonline.co/?s=',4,'http://www.seretonline.co/image/logo.png','seretonline')
        addDir('חפש ב livevod','http://www.live-vod.net/?s=',2,'http://www.live-vod.net/images/logo.png','livevod')
        addDir('חפש ב seretil','http://seretil.me/?s=',1,'http://seretil.me/wp-content/uploads/2013/02/cooltext906607089.png','seretil')
        setView('movies', 'default') 
       #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml  
       
       
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
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

# this is the listing of the items        
def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
#same as above but this is addlink this is where you pass your playable content so you dont use addDir you use addLink "url" is always the playable content         
def addLink(name,url,iconimage,description):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
 
        
#below tells plugin about the views                
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type

def Search_dialog():
    searchtext=""
    keyboard = xbmc.Keyboard(searchtext, 'חיפוש סרט')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return keyboard.getText()

def SearchLivevod(url):
    text=Search_dialog()
    url=url+urllib.quote(text)
  
    link2=OPEN_URL(url)
    regex1='<p><strong>מתנצלים, לא הצלחנו למצוא מה שחיפשת</strong><(.*?)>'
    noresult=re.compile(regex1).findall(link2)
    if noresult==[]:
            regex='<a class="entry-thumbnails-link" href="(.*?)"><img.*?src="(.*?)" class="attachment-quick-preview-thumb wp-post-image" alt=".*?\מ.*?rel="bookmark">(.*?)<'
            matches = re.compile(regex).findall(link2)
            for url2 ,image,name in matches:
                  addDir(name,url2,3,image,"")
            if len(matches)>9:
                 xbmcgui.Dialog().ok('נא למקד חיפוש','יותר מדיי תוצאות','מציג רשימה חלקית,נסה חיפוש ממוקד יותר')
    else:
        CATEGORIES()
        
def SearchLivevodLinks(url):
    link2=OPEN_URL(url)
    regex='<iframe src="http://(.*?)"'
    matches = re.compile(regex).findall(link2)
    
    sources=[]
    if matches==[]:
            regex='<p><iframe style=".*?src="(.*?)"'
            matches = re.compile(regex).findall(link2)
            
    for newurl in matches:
           sources.append(urlresolver.HostedMediaFile('http://'+newurl))
    i=1
    for source in sources:
        
        if str(source).find('vk.com')==-1:
                if source :
                      try :
                        stream_url = source.resolve()
                        addLink("link " + str(i) ,stream_url,"","")
                        i=i+1    
                      except:pass
                else:
                   print(str(source)+"not playble")
                   url=None
        else:
            addFinalLink('http://'+newurl,name)    
      
           
def addFinalLink(finalurl,name):
    match = getURL(finalurl)
    addLink(name,match,"","")
    xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)

def  SearchSeretOnline(url):
     text=Search_dialog()
     url=url+urllib.quote(text)
     link2=OPEN_URL(url)
     regex='bold;" href="(.*?)".*?rel="bookmark" title="Permanent Link to (.*?)">.*?\n.*?<img.*?src="(.*?)"'
     matches = re.compile(regex).findall(link2)
     i=1
     for url2 ,name ,image in matches:
            addDir(name,url2,5,image,"")
            i=i+1
     if i>10 :
         xbmcgui.Dialog().ok('נא למקד חיפוש','יותר מדיי תוצאות','מציג רשימה חלקית,נסה חיפוש ממוקד יותר')
        
   

def SeretOnlineLinks(url):
    link2=OPEN_URL(url)
    regex1='<li><img alt=".*?<a href="(.*?)".*?</a></li>'
    line = re.compile(regex1).findall(link2)
    sources=[]
    text="link "
    if name.find('עונה')!=-1 :
        text=" episode \ פרק   "
    for match in line:
        if str(match).find('linkbucks')!=-1:
            match=urllib.unquote(str(match))
            if name.find('עונה')!=-1 :
                xbmc.sleep( 5000)
                dp = xbmcgui.DialogProgress()
                dp.create('מחפש בעונה שלמה','בחרת לראות לינקים לעונה שלמה','נא להמתין בסבלנות ,יהיה טוב','ההודעה הזו תהבהב קצת,נא לא ללחוץ ביטול')  
            link3=OPEN_URL(match)
            regex='Lbjs.TargetUrl = (.*?);'
            link = re.compile(regex).findall(link3)
            if str(link)=='[]':
                regex='<a href="/file/(.*?)"'
                link = re.compile(regex).findall(link3)
                newlink='www.putlocker.com/embed/'+str(link[0])
                
            else:
                newlink=str(link[0])[1:-1]
            
            sources.append(urlresolver.HostedMediaFile(newlink))
    i=1
    for source in sources :
        
        
        if str(source).find('adf')==-1:
                if source :
                      try :
                        stream_url = source.resolve()
                        addLink(text + str(i) ,stream_url,"","")
                        i=i+1    
                      except:pass
                else:
                   print(str(source)+"not playble")
                   url=None
        else:
             print(str(source)+"  adfly?")

def SearchSeretil(url):
    text=Search_dialog()
    newurl=url+urllib.quote(text)
    print ("the new sereturl is " + str(newurl))
    INDEXchooseSeret(newurl)
    
def LinksPage(url):
        print(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        sources =[]
        match=re.compile('<p><a href="(.*?)"').findall(link)
        print (str(match))
        for newurl in match:
            sources.append(urlresolver.HostedMediaFile(newurl))
        print (str(sources) )
        i=1
        for source in sources:
            if source :
                 try :
                     stream_url = source.resolve()
                     addLink("link " + str(i) ,stream_url,"","")
                     i=i+1    
                 except:pass
            else:
                print("not playble")
                url=None
        xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)

def INDEXchooseSeret(url):
        print(url)
        url2=url
        req = urllib2.Request(url)
        req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link2=link
        response.close()    
        print (link)
        if re.findall('Please try again',link) != []:
            xbmcgui.Dialog().ok('חיפוש','נסה חיפוש אחר')
            CATEGORIES()        

   
        else:

            match=re.compile('<h2 class="title"><a href="(.*?)".*?mark">(.*?)</a').findall(link)
            for url,name  in match:
                req = urllib2.Request(url)
                req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link3=response.read()
                response.close()  
                image=None
                images= re.compile('       <img width=".?.?.?" height=".?.?.?" src="(.*?)"').findall(link3)
                if images==[]:
                    addDir(name,url,6,"","")
                    print (name,"url= "+ url +"special one !!!!!!!")
                else:
                    addDir(name,url,6,str(images[0]),"")
                
            if len(match)>9:
                 xbmcgui.Dialog().ok('נא למקד חיפוש','יותר מדיי תוצאות','מציג רשימה חלקית,נסה חיפוש ממוקד יותר')
            now=re.compile('class=\'current\'>(.*?)<').findall(link2)
            next_page=re.compile('<span class=.?pages.?>(.*?) מתוך').findall(link2)
            int_now_page =int(str(now[0])) +1
            url2 = url2[:-7]
            if url2[len(url2)-1]=='p' :
                 url2= url2[:-1]
            url2=url2+'page/'+ str(int_now_page)+'/'
            print("url the next ",url2)
            addDir("עוד תוצאות",url2,7,"","")
            addDir("חזרה לתפריט ראשי",'www.stam.com',None,"","");
    
    
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        SearchSeretil(url)   
       
elif mode==2:
        print ""+url
        SearchLivevod(url)
elif mode==3:
        print ""+url
        SearchLivevodLinks(url)
elif mode==4:
        print""+url
        SearchSeretOnline(url)
elif mode==5:
        print""+url
        SeretOnlineLinks(url)
elif mode==6:
    LinksPage(url)
elif mode==7:
    INDEXchooseSeret(url)
    
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
