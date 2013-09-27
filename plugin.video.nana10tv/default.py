# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc

icon = 'http://f.nanafiles.co.il//Upload/52013/Navigate/NavigateCatPic_2532151.jpg'

ADDON = xbmcaddon.Addon(id='plugin.video.nana10tv')
__SECTION_BASE__='http://10tv.nana10.co.il/Section/'


 
def CATEGORIES():
        addDir('main menu','http://10tv.nana10.co.il/Category/?CategoryID=400008',1,icon,'')
        setView('movies', 'default') 
       #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml  
       
       
                      												  
def Choose_series(url):#  cause mode is empty in this one it will go back to first directory
        link=OPEN_URL('http://10tv.nana10.co.il/Category/?CategoryID=400008')
        matches=re.compile('" href="http://10tv.nana10.co.il/section/(.*?)".?onclick="t1674.getData.*?return false;">(.*?)</a>',re.I+re.M+re.U+re.S).findall(link)
        #print "matches  are :" +str (matches)
        sorted_movies=[]
        matches = [ matches[i] for i,x in enumerate(matches) if x not in matches[i+1:]]
        for url ,name in matches :
                sorted_movies.append((url,name))
        sorted_movies = sorted(sorted_movies,key=lambda sorted_movies: sorted_movies[1])
        for movie in sorted_movies:
            addDir(movie[1],__SECTION_BASE__+ movie[0],2,'','')
       # addDir(name,__SECTION_BASE__+url,2,'','')
        setView('tvshows', 'anything') 

def series_land(url):
        link=OPEN_URL(url)
        
        # class="" onmousedown="return cr(event, 'ClickArticle', 980364, null, 3);">
				#	<img src="//f.nanafiles.co.il/upload/mediastock/img/5/0/105/105370.jpg" alt="׳”׳׳§׳•׳¨ 28.05.13" class="Image" />
        block=re.compile('MiddleColumn(.*?)LeftColumn',re.I+re.M+re.U+re.S).findall(link)
        matches=re.compile('<a href="http://10tv.nana10.co.il/Article/(.*?)".*?<img src="//f.nanafiles.co.il.?/upload(.*?)".*?alt="(.*?)"',re.I+re.M+re.U+re.S).findall(block[0])
        
        for newurl,image,name in matches:
                newurl='http://10tv.nana10.co.il/Article/'+newurl
                addDir(name,newurl,3,'http://f.nanafiles.co.il/upload'+ image,'')

def play_episode(url):
        #http://common.nana10.co.il/Video/Action.ashx/Player/GetData?GroupID=58993
        #addLink('test','http://switch206-01.castup.net/cunet/gm.asp?ClipMediaId=11948638','','')
        
        link=OPEN_URL(url)
        urlBase=matches=re.compile('<link rel="canonical" href="(.*?)Article',re.I+re.M+re.U+re.S).findall(link)
        matches=re.compile('<iframe name="VideoIframe".*?src="(.*?)">VideoIframe',re.I+re.M+re.U+re.S).findall(link)
        matches[0]=matches[0].replace('amp;','')
        secondlink=urllib.unquote(OPEN_URL(urlBase[0] + matches[0]))
        print secondlink
        matches=re.compile('MediaStockVideoItemGroupID","(.*?)"',re.I+re.M+re.U+re.S).findall(secondlink)
        if matches:
                if  matches[0]!='0' :
                        thirdlink=OPEN_URL('http://common.nana10.co.il/Video/Action.ashx/Player/GetData?GroupID='+matches[0])
                        matches=re.compile('ClipMediaId=(.*?)"',re.I+re.M+re.U+re.S).findall(thirdlink)
                else :
                        matches=re.compile('ClipMediaID=(.*?)&ak=null',re.I+re.M+re.U+re.S).findall(secondlink)
        else :
                matches=re.compile('http://SWITCH(.*?).castup.net/cunet/(.*?)"',re.I+re.M+re.U+re.S).findall(secondlink)
                print matches
                final_url='http://SWITCH'+ str(matches[0][0])+'.castup.net/cunet/'+ str(matches[-1][-1])
                print final_url
                link=OPEN_URL(final_url)
                matches=re.compile('<ref href="(.*?).?ct',re.I+re.M+re.U+re.S).findall(link)
                final_url=matches[-1]
                ok=True
                liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
                liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
                liz.setProperty("IsPlayable","true")
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=final_url,listitem=liz,isFolder=False)
                return ok 

        print matches   
        matches.sort(key=int)
        print matches
        final_url='http://switch206-01.castup.net/cunet/gm.asp?ClipMediaId='+matches[-1]
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=final_url,listitem=liz,isFolder=False)
        return ok 
      
        

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
        Choose_series(url)
elif mode==2:
        series_land(url)
elif mode==3:
        play_episode(url)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))

