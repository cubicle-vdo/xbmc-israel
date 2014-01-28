# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,base64,os

ADDON = xbmcaddon.Addon(id='plugin.video.israelsports')
AddonID='plugin.video.israelsports'



 
def CATEGORIES():
        mes()
        addDir('כל הסרטונים','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=147&page=',2,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTvo6GmRkhBMgJHX0DiWtikRpet97rNyCTsSi_OdsdF7Dp4K-96','1')
        addDir('ליגת האלופות','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4649&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRf7mZyApMKwnQyHcJ5shoFE8OhLOlbmUIhytkWAP05suAGv9h8xA','1')
        addDir('ליגה ספרדית','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4435&page=',2,'http://blog.tapuz.co.il/tlv1/images/%7B0B4BDB70-5D9B-463A-B894-0D5762E59AA0%7D.jpg','1')
        addDir('תקצירי בארסה','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4436&page=',2,'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQYF9lIm6fqSM3cysKy_EqnRFyDOycA8lexCn7dSqp_4Av4vw1mcA','1')
        addDir('תקצירי מדריד','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4437&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTJtSGna8A2FmzVH3WQyBLx6HGwEGqUKeBzPqvzn7cmcKvpkv8D','1')
        addDir('ליגת העל בכדורגל','www.stam.com',6,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRpi-QusXtg3bBYigUFBxDmVj-nbBuPqJsGhWybwI8zx1Rlh2mw','')
        addDir('ליגה איטלקית','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4729&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ5MZPuGkXGn4XoaDo72fi0gKIOik_0GVZHgHXmkQ1avptCA4WS','1')
        addDir('ליגה אנגלית','http://svc.one.co.il/Cat/Video/?c=85&p=',4,'http://www.bettingexpert.com/deprecated/assets/images/blog/PremLeagueBettingAwards/premier-league-logo.jpg','1')
        addDir('NBA','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4986&page=',2,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTMaYyCKAudTxqAh0YUsGGbL5axGDZV5YT-wL1-dYK25VfNNTzhKg','1')
        addDir('מכבי ת"א יורוליג','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4972&page=',2,'http://images1.ynet.co.il/PicServer2/24012010/2885944/hot_maccabi3.jpg','1')
        addDir('יורוליג','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4973&page=',2,'http://www.heinnews.com/wp-content/uploads/2010/06/euroleague-logo.jpg','1')
        addDir('כדורסל ישראלי','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4945&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcROtyknPHO9KMMRBxTivXvWDngNdMzr5Mf5VMyJLyPEx_WEpxtk','1')
        addDir('חמישיות','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=3963&page=',2,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTSYYoacn3zS6w4JwqPORpGCDBqytoJOko8bc6usF3kQ_yoJgwS','1')
        addDir('חדשות הספורט','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=3968&page=',2,'http://www.nrg.co.il/images/archive/300x225/631/730.jpg','1')
        addDir('יציע העיתונות','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=2770&page=',2,'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRVDQaVdqH65g5IqYdUf1zqt_FMHSOsbJPYzLI6tC1lxyh_FS97','1')
        addDir('הקישור','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=3061&page=',2,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIwv5MJeZjUM4QI8iIZEhivnz71tZssEn9naosE1xWkrCNw7ontg','1')
        addDir('מאיר ורוני','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4984&page=',2,'http://www.the7eye.org.il/wp-content/uploads/2013/10/F130801YS191.jpg','1')        
        addDir('LIVE SPORTS','no url',8,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRXXYDnees25Hwhbt2CRWlDuH1E6XTE01_8Uv94E3-mop_7isfM','')
        setView('movies', 'default')
        
       
       
       
                      												  
def  list_videos(url,page):
       
        url1=url+"1"
        url=url+str(page)
        link=OPEN_URL(url1)
        total=re.compile('total-pages="(.*?)"').findall(link)
        if total:
                total=int(total[0])
        else :
                total=1
       
        page=int(page)
        if page <= total:
                link=OPEN_URL(url)
                matches=re.compile('<li id.*?<a href="(.*?)"><img src="(.*?)" title="(.*?)"').findall(link)
                for  newurl ,image , title  in matches :
                        title=title.decode('iso-8859-8').encode('utf-8')
                        title=unescape(title)
                        addDir(title,newurl,3,image,'')
                index=url.find('page=')
                url=url[0:index]
                page=page+ 1
                url=url+"page="
                list_videos(url,page)
        setView('movies', 'default')
        
def play_video(url,name,iconimage):       
        link=OPEN_URL(url)
        clipid=re.compile('clipid=(.*?)&Width',re.M+re.I+re.S).findall(link)
        secondurl = "http://sport5-metadata-rr-d.nsacdn.com/vod/vod/" + str(clipid[0]) +"/HLS/metadata.xml?smil_profile=default"

        link=OPEN_URL(secondurl)

        highres=re.compile('http://s5-s.nsacdn.com/sport5_vod/(.*?)</FileURL>',re.M+re.I+re.S).findall(link)
        direct=  "http://s5-s.nsacdn.com/sport5_vod/" + str (highres[-1])
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title":name} )
        liz.setPath(direct)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        
        
        
def ligat_al():
    link = OPEN_URL('http://svc.one.co.il/Cat/Video/Reviews.aspx?c=28')
    #<a href="/Cat/Video/Reviews.aspx?tm=1"><img style="border:0;width:46px;height:49px;" src="http://images.one.co.il/Images/Teams/Logos_46x49/1.png" alt="הפועל חיפה" /></a>"
    list1=re.compile('<a href="(.*?)".*?src="http://images.one.co.il/Images/Teams/Logos(.*?)" alt="(.*?)" /></a>').findall(link)
    for url ,image,name in list1:

            name=name.decode('iso-8859-8').encode('utf-8')
            name=unescape(name)
            url='http://svc.one.co.il'+url
            image='http://images.one.co.il/Images/Teams/Logos'+image
            addDir(name,url,4,image,'al')
    setView('movies', 'default')

def one_videopage(url,description):
        if description!='al' :
                murl=url+str(description)
        else:
                murl=url
                        
        link = OPEN_URL(murl)
        list1=re.compile('"Image": "(.*?)".*?"Title": "(.*?)".*?"HQ":"(.*?)".*?"ID":(.*?)}').findall(link)
        #var page = 4;var pages = 8;
        page_total=re.compile('var page = (.*?);.*?var pages = (.*?);').findall(link)[0]
        current= page_total[0]
        total= page_total[1]
        current=int(current)
        total =int (total)
        
        
        for image,name,hq,Id in list1:
                image="http://images.one.co.il/images/video/segment377x285/"+image
                name=unescape(name)
                name=name.decode('windows-1255').encode('utf-8')
                addDir(name,str(Id),5,image,hq)
        if current < total :
                current+=1
                addDir("[COLOR yellow]לעמוד הבא[/COLOR]",url,4,'',str(current))
        addDir("[COLOR blue]חזרה לראשי [/COLOR]",'',None,'','')

        setView('movies', 'default')
                

def play_one(name,url,iconimage,description):
        
        url1="http://svc.one.co.il/cat/video/playlisthls.aspx?id="+url
        link = OPEN_URL(url1)
        #source file="http://streambk.one.co.il/2013_2/33266.mp4" label="360p" /><jwplayer:source file="http://streambk.one.co.il/2013_2_HD/33266.mp4" label="720p HD" />
        list2=[]
        regex='source file="(.*?)"'
        direct=re.compile(regex).findall(link)
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title":name} )
        #liz.setProperty("IsPlayable","true")
        
        for item in direct:
                if item.find("ds") ==-1 :
                        if description=='True':
                                if item.find("HD")>0 :
                                     liz.setPath(item)
                                     xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                                
                                        
                        else:
                                addLink(name,item,iconimage,'')


def OPEN_URL(url,host=None):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    if host:
            req.add_header('HOST',host)
    response = urllib2.urlopen(req,timeout=180)
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

def unescape(text):
        try:            
            rep = {"&nbsp;": " ",
                   "\n": "",
                   "\t": "",
                   "\r":"",
                   "&#39;":"",
                   "&quot;":"\""
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
				
        except TypeError:
            pass

        return text

# this is the listing of the items



def downloader_is (url,name ) :
 import downloader,extract   
 i1iIIII = xbmc . getInfoLabel ( "System.ProfileName" )
 I1 = xbmc . translatePath ( os . path . join ( 'special://home' , '' ) )
 O0OoOoo00o = xbmcgui . Dialog ( )
 if name.find('repo')< 0 :
     choice = O0OoOoo00o . yesno ( "XBMC ISRAEL" , "לחץ כן להתקנת תוסף חסר" ,name)
 else:
     choice=True
 if    choice :
  iiI1iIiI = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'packages' ) )
  iiiI11 = xbmcgui . DialogProgress ( )
  iiiI11 . create ( "XBMC ISRAEL" , "Downloading " , '' , 'Please Wait' )
  OOooO = os . path . join ( iiI1iIiI , 'isr.zip' )
  try :
     os . remove ( OOooO )
  except :
      pass
  downloader . download ( url , OOooO , iiiI11 )
  II111iiii = xbmc . translatePath ( os . path . join ( 'special://home' , 'addons' ) )
  iiiI11 . update ( 0 , "" , "Extracting Zip Please Wait" )
  print '======================================='
  print II111iiii
  print '======================================='
  extract . all ( OOooO , II111iiii , iiiI11 )
  iiiI11 . update ( 0 , "" , "Downloading" )
  iiiI11 . update ( 0 , "" , "Extracting Zip Please Wait" )
  xbmc . executebuiltin ( 'UpdateLocalAddons ' )
  xbmc . executebuiltin ( "UpdateAddonRepos" )
  if 96 - 96: i1IIi . ii1IiI1i * iiiIIii1I1Ii % i111I
  if 60 - 60: iII11iiIII111 * IIIiiIIii % IIIiiIIii % O00oOoOoO0o0O * i11i + i1IIi



def addDir(name,url,mode,iconimage,description):
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        if mode==3 or mode==5:
                liz.setProperty("IsPlayable","true")
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

                    

def mes():

        
	try:
		link=OPEN_URL('http://goo.gl/ylPukV')
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


def VIPList():
        url=base64.b64decode('aHR0cHM6Ly9yYXcuZ2l0aHViLmNvbS9tYXNoMmszL01hc2hTcG9ydHMvbWFzdGVyL01hc2hzcHJ0LnhtbA==')
        link=OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<title>([^<]+)</title.+?link>(.+?)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        for name,url,thumb in sorted(match):
                if not'NHL' in name   and not 'Non' in name:
                        if not '</sublink>' in url:
                            addLink(name,url,thumb,'')
                        else:
                              links=re.compile('<sublink>(.*?)</sublink>').findall(url)
                              for link in links:
                                      addLink(name,link,thumb,'')


def ListLive(url):
        print url
        link=OPEN_URL(url,'www.navixtreme.com')
        link=unescape(link)
        #print link
        matches1=re.compile('pe=(.*?)#',re.I+re.M+re.U+re.S).findall(link)
        print str(matches1[0]) + '\n'
        for match in matches1 :
            print "match=" + str(match)
            match=match+'#'
            if match.find('playlist') != 0 :
                regex='name=(.*?)URL=(.*?)#'
                matches=re.compile(regex,re.I+re.M+re.U+re.S).findall(match)
                print str(matches)
                for name,url in  matches:
                    thumb=''
                    i=name.find('thumb')
                    if i>0:
                        thumb=name[i+6:]
                        name=name[0:i]		    
                    if  'port' in  name :
                            addLink('[COLOR yellow]'+ name+'[/COLOR]',url,thumb,'')  
                
                              
                

def LIVE():
        
        addLink('SPORT 5 site live 3','rtmp://s5-s.nsacdn.com:1935/sport5_Live3Repeat/Live3_3 swfUrl=http://playern.sport5.co.il/Plugins/RTMPPlugin.swfpageUrl=http://playern.sport5.co.il/Player.aspx?clipId=Live3&Type=live','https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/s160x160/1234096_10151587235806651_42196135_a.jpg','')
        addLink('SPORT 5 site live 2','rtmp://s5-s.nsacdn.com:1935/sport5_Live2Repeat/Live2 swfUrl=http://playern.sport5.co.il/Plugins/RTMPPlugin.swfpageUrl=http://playern.sport5.co.il/Player.aspx?clipId=Live2&Type=live','https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/s160x160/1234096_10151587235806651_42196135_a.jpg','')
        addLink('SPORT 5 site live 1','rtmp://s5-s.nsacdn.com:1935/sport5_Live1Repeat/Live1_3 swfUrl=http://playern.sport5.co.il/Plugins/RTMPPlugin.swfpageUrl=http://playern.sport5.co.il/Player.aspx?clipId=Live1&Type=live','https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/s160x160/1234096_10151587235806651_42196135_a.jpg','')
        VIPList()


        
               
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
        CATEGORIES()

elif mode==2:
        list_videos(url,description)
elif mode==3:
        play_video(url,name,iconimage)
elif mode==4:
        one_videopage(url,description)
elif mode==5:
        play_one(name,url,iconimage,description)
elif mode==6:
        ligat_al()
elif mode==8:
        LIVE()
elif mode==9:
        VIPList()
elif mode==10:
        downloader_is('http://mirrors.xmission.com/superrepo/Frodo/Video/plugin.video.teledunet/plugin.video.teledunet-2.0.2.zip','Teleduent')
        downloader_is('https://github.com/downloads/hadynz/repository.arabic.xbmc-addons/repository.arabic.xbmc-addons-1.0.0.zip','Teleduent repo')
xbmcplugin.endOfDirectory(int(sys.argv[1]))

