# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc

ADDON = xbmcaddon.Addon(id='plugin.video.israelsports')



 
def CATEGORIES():
        Announcements()
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
        addDir('מאיר ורוני','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4948&page=',2,'http://www.the7eye.org.il/wp-content/uploads/2013/10/F130801YS191.jpg','1')
        addLink('SPORT 5 site live 3','rtmp://s5-s.nsacdn.com:1935/sport5_Live3Repeat/Live3_3 swfUrl=http://playern.sport5.co.il/Plugins/RTMPPlugin.swfpageUrl=http://playern.sport5.co.il/Player.aspx?clipId=Live3&Type=live','https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/s160x160/1234096_10151587235806651_42196135_a.jpg','')
        addLink('SPORT 5 site live 2','rtmp://s5-s.nsacdn.com:1935/sport5_Live2Repeat/Live2 swfUrl=http://playern.sport5.co.il/Plugins/RTMPPlugin.swfpageUrl=http://playern.sport5.co.il/Player.aspx?clipId=Live2&Type=live','https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/s160x160/1234096_10151587235806651_42196135_a.jpg','')
        addLink('SPORT 5 site live 1','rtmp://s5-s.nsacdn.com:1935/sport5_Live1Repeat/Live1_3 swfUrl=http://playern.sport5.co.il/Plugins/RTMPPlugin.swfpageUrl=http://playern.sport5.co.il/Player.aspx?clipId=Live1&Type=live','https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/s160x160/1234096_10151587235806651_42196135_a.jpg','')
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
        liz.setProperty("IsPlayable","true")
        playlist.add(direct,liz)
        
        
        if not xbmc.Player().isPlayingVideo():
                xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playlist)
        
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
        liz.setProperty("IsPlayable","true")
        for item in direct:
                if item.find("ds") ==-1 :
                        if description=='True':
                                if item.find("HD")>0 :
                                     #addLink(name,item,iconimage,'')
                                     playlist.add(item,liz)      
                                     if not xbmc.Player().isPlayingVideo():
                                        xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playlist)
                                
                                        
                        else:
                                addLink(name,item,iconimage,'')


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    
    response = urllib2.urlopen(req,timeout=100)
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
def addDir(name,url,mode,iconimage,description):
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        if mode==3 or mode==5:
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

def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()

def Announcements():
        #Announcement Notifier from xml file
        
        try:
              link=OPEN_URL('https://dl.dropboxusercontent.com/u/5461675/sportsisarel.xml')
              # link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

        except:
                link='nill'
        r = re.findall(r'ANNOUNCEMENTWINDOW ="ON"',link)
        if r:

                match=re.compile('<new>(.*?)\\n</new>',re.I+re.M+re.U+re.S).findall(link)
                if match[0]:
                        TextBoxes("[B][COLOR blue] SPORTS ISRAEL[/B][/COLOR]",match[0])                      



               
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
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))

