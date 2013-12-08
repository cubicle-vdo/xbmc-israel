# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

icon = 'http://f.nanafiles.co.il//Upload/52013/Navigate/NavigateCatPic_2532151.jpg'

AddonID = 'plugin.video.nana10tv' 
ADDON = xbmcaddon.Addon(id=AddonID)
__SECTION_BASE__='http://10tv.nana10.co.il/Section/'


def mes():
	try:
		link=OPEN_URL('http://goo.gl/8xDxIf')
		r = re.findall(r'ANNOUNCEMENTWINDOW ="ON"',link)
		if not r:
			return
			
		match=re.compile('<new>(.*?)\\n</new>',re.I+re.M+re.U+re.S).findall(link)
		if not match[0]:
			return
			
		version = ADDON.getAddonInfo('version')
		
		dire=os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), AddonID)
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
                      												  
def Choose_series(url):
        mes()
        link=OPEN_URL('http://10tv.nana10.co.il/Category/?CategoryID=400008')
        matches=re.compile('" href="http://10tv.nana10.co.il/section/(.*?)".?onclick="t1674.getData.*?return false;">(.*?)</a>',re.I+re.M+re.U+re.S).findall(link)
        sorted_movies=[]
        for url ,name in matches : 
                if url !="?SectionId=" and    url !="?SectionId=847131" :
                        if not (url,name) in sorted_movies:
                                sorted_movies.append((url,name))
        sorted_movies = sorted(sorted_movies,key=lambda sorted_movies: sorted_movies[1])
        for movie in sorted_movies:
        
            if not 'http' in movie[0] :    
                    addDir(movie[1],__SECTION_BASE__+ movie[0],2,'','')
           
            
        setView('tvshows', 'anything') 

def series_land(url):
        link=OPEN_URL(url)
        block=re.compile('MiddleColumn(.*?)LeftColumn',re.I+re.M+re.U+re.S).findall(link)
        matches=re.compile('<a href="http://10tv.nana10.co.il/Article/(.*?)".*?<img src="//f.nanafiles.co.il.?/upload(.*?)".*?alt="(.*?)"',re.I+re.M+re.U+re.S).findall(block[0])
        
        for newurl,image,name in matches:
                newurl='http://10tv.nana10.co.il/Article/'+newurl
                addDir(name,newurl,3,'http://f.nanafiles.co.il/upload'+ image,'')

def play_episode(url):
        
        link=OPEN_URL(url)
        urlBase=matches=re.compile('<link rel="canonical" href="(.*?)Article',re.I+re.M+re.U+re.S).findall(link)
        matches=re.compile('<iframe name="VideoIframe".*?src="(.*?)">VideoIframe',re.I+re.M+re.U+re.S).findall(link)
        matches[0]=matches[0].replace('amp;','')
        secondlink=urllib.unquote(OPEN_URL(urlBase[0] + matches[0]))
        
        matches=re.compile('MediaStockVideoItemGroupID","(.*?)"',re.I+re.M+re.U+re.S).findall(secondlink)
        if matches:
                if  matches[0]!='0' and matches[0]!='':
                        thirdlink=OPEN_URL('http://common.nana10.co.il/Video/Action.ashx/Player/GetData?GroupID='+matches[0])
                        matches=re.compile('ClipMediaId=(.*?)"',re.I+re.M+re.U+re.S).findall(thirdlink)
                else :
                        matches=re.compile('ClipMediaID=(.*?)&ak=null',re.I+re.M+re.U+re.S).findall(secondlink)

                   
                matches.sort(key=int)
                
                final_url='http://switch206-01.castup.net/cunet/gm.asp?ClipMediaId='+matches[-1]

        else :
                matches=re.compile('http://SWITCH(.*?).castup.net/cunet/(.*?)&ak',re.I+re.M+re.U+re.S).findall(secondlink)
                if matches :  
                        names=matches[-1][-1]
                        if 'ar=' in names:
                                 i=names.find('ar=')
                                 names=names[i+3:]
                                 names=urllib.quote(names)
                                 firstname=matches[-1][-1][:i+3]
                                 final_url='http://SWITCH'+ str(matches[0][0])+'.castup.net/cunet/'+ firstname+names
                        else:
                                final_url='http://switch206-01.castup.net/cunet/'+names
                else: 
                        match=re.compile('http://switch206-01.castup.net(.*?)&st',re.I+re.M+re.U+re.S).findall(secondlink)[0]
                        
                        final_url='http://switch206-01.castup.net'+match.decode("utf-8")
                        
                
                link=OPEN_URL(final_url,'http://10tv.nana10.co.il/Category/?CategoryID=400008')
                matches=re.compile('<ref href="(.*?).?ct',re.I+re.M+re.U+re.S).findall(link)
                final_url=matches[-1]

        
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.add(final_url,liz)
        if not xbmc.Player().isPlayingVideo():
                xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playlist)


def OPEN_URL(url,ref=None):

    
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    if ref != None :
            req.add_header('Referer',ref)
            
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
        if mode==3 :
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
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

