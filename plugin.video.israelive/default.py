# -*- coding: utf-8 -*-
#code by o2ri \ avigdor based on benny123 project in navix.
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,base64,datetime,json
AddonID = 'plugin.video.israelive'
libDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import myFilmon,commonlive
from commonlive import *

dire=os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(dire):
            os.makedirs(dire)
__icon__='http://static2.wikia.nocookie.net/__cb20121121053458/spongebob/images/f/f4/Check-icon.png'
__icon2__='https://svn.apache.org/repos/asf/openoffice/symphony/trunk/main/extras/source/gallery/symbols/Sign-QuestionMark02-Red.png'
FAV=os.path.join(dire, 'favorites.txt')
if  not (os.path.isfile(FAV)):
    f = open(FAV, 'w') 
    f.write('[]') 
    f.close() 

def CATEGORIES():
    Announcements()
    addDir('הערוצים שלי','favorits',15,'http://cdn3.tnwcdn.com/files/2010/07/bright_yellow_star.png','')
    addDir('עידן פלוס','https://dl.dropbox.com/u/94071174/Online/wow/DTT%2B.plx',2,'http://ftp5.bizportal.co.il/web/giflib/news/idan_plus_gay.jpg','')
    addDir('רדיו','https://dl.dropboxusercontent.com/u/94071174/Online/wow/SUB/Entertainment/IL%20Radio.plx',2,'http://www.binamica.co.il/english/data/images/Image/radio.jpg','')
    addDir('ילדים','https://dl.dropbox.com/u/94071174/Online/wow/Kids.plx',2,'http://4hdwall.com/wp-content/uploads/2012/09/HD-cartoon-wallpaper.jpg','')
    addDir('בידור','https://dl.dropboxusercontent.com/u/94071174/Online/wow/Entertainment.plx',2,'http://digitalmediafilms.webs.com/Variety%20of%20Your%20Favortie%20Channels.jpg','')
    addDir('סרטים','https://dl.dropbox.com/u/94071174/Online/wow/Movies.plx',2,'http://www.attractherdateher.com/wp-content/uploads/2012/08/movie_night.jpg','')
    addDir('מוזיקה','https://dl.dropbox.com/u/94071174/Online/wow/Music.plx',2,'http://www.hdwallpapers.in/wallpapers/dance_with_me_hd_wide-1920x1200.jpg','')
    addDir('חדשות','https://dl.dropbox.com/u/94071174/Online/wow/News.plx',2,'http://www.realtrends.com/application/view/theme/default/docs/scroll/blog6.jpg','')
    addDir('מדע וטבע','https://dl.dropbox.com/u/94071174/Online/wow/Science%20%26%20Nature.plx',2,'http://wallpapers.free-review.net/wallpapers/23/Nature_-_Wallpaper_for_Windows_7.jpg','')
    addDir('ספורט','https://dl.dropbox.com/u/94071174/Online/wow/Sport.plx',2,'http://4vector.com/i/free-vector-sport-vector-pack_098139_sportsvector%20pack.jpg','')
    addDir('עולם','https://dl.dropbox.com/u/94071174/Online/wow/World.plx',2,'http://www.icangiveyouhouse.com/audio/2010/09/world-in-black-and-white-hands-1.jpg','')
   

    if   os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
        addDir('iLive.to','plugin://plugin.video.movie25/?iconimage=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashupArtwork%2fmaster%2fart%2filive.png&mode=119&name=iLive%20Streams&url=ilive',7,'https://raw.github.com/mash2k3/MashupArtwork/master/art/ilive.png','')
    else:
        addDir('[COLOR yellow]לחץ כאן להתקנת תוסף חסר[/COLOR]' ,'https://github.com/o2ri/xbmc-israel/blob/master/mash.zip?raw=true',8,'http://blog.missionmode.com/storage/post-images/critical-factor-missing.jpg','Mash23 addon')
            
    if    not os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.teledunet'):
         addDir('[COLOR yellow]לחץ כאן להתקנת תוסף חסר[/COLOR]' ,'http://superrepo.brantje.com//Frodo/All/plugin.video.teledunet/plugin.video.teledunet-2.0.2.zip',6,'http://blog.missionmode.com/storage/post-images/critical-factor-missing.jpg','Teleduent')
         
        

def update_view(url):

    ok=True        
    xbmc.executebuiltin('XBMC.Container.Update(%s)' % url )
    return ok
        
    
   
def ListLive(url):

        if 'Sport' in url:
            VIPList()
        
        link=OPEN_URL(url)
        link=unescape(link)
        #print link
        matches1=re.compile('pe=(.*?)#',re.I+re.M+re.U+re.S).findall(link)
        for match in matches1 :
            #print "match=" + str(match)
            match=match+'#'
            if match.find('playlist') != 0 :
                regex='name=(.*?)URL=(.*?)#'
                matches=re.compile(regex,re.I+re.M+re.U+re.S).findall(match)
                #print str(matches)
                for name,url in  matches:
                    thumb=''
                    i=name.find('thumb')
                    if i>0:
                        thumb=name[i+6:]
                        name=name[0:i]
		    #print url
                    i=url.find('plugin.video.MyFilmOn')
		    if i >0:
                        addDir('[COLOR yellow]' +name+'[/COLOR]',url,3,thumb,'')
                    else:
                        addDir('[COLOR yellow]'+ name+'[/COLOR]',url,11,thumb,'')  
                
            else:
                regex='name=(.*?)URL=(.*?).plx'
                matches=re.compile(regex,re.I+re.M+re.U+re.S).findall(match)
                for name,url in matches:
                    url=url+'.plx'
                    if name.find('Radio') < 0 :
                        addDir('[COLOR blue]'+name+'[/COLOR]',url,2,'','')
               
       

def play_Filmon(url):
    direct, fullName, iconimage = myFilmon.GetUrlStream(url)
    if direct == None:
    	return
    if (iconimage == None):
    	iconimage = "DefaultVideo.png"
    listitem = xbmcgui.ListItem(fullName, iconimage, iconimage, path=direct)
    listitem.setInfo( type="Video", infoLabels={ "Title":fullName} )
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def FilmonChannelGuide(url):
	chNum, referrerCh, ChName = myFilmon.GetUrlParams(url)
	if referrerCh != None:
		addDir('[COLOR red][B]No TV-Guide for this channel.[/B][/COLOR]', '.', 99, '', '')
		return
		
	channelName, channelDescription, iconimage, tvGuide = myFilmon.GetChannelGuide(chNum)

	if tvGuide == None:
		addDir('[COLOR red][B]No TV-Guide for this channel.[/B][/COLOR]', '.', 99, '', '')
		return
	elif len(tvGuide) == 0:
		addDir('[COLOR red][B]No TV-Guide for "{0}".[/B][/COLOR]'.format(channelName), '.', 99, iconimage, channelDescription)
	else:
		addDir('------- [B]{0} - TV-Guide[/B] -------'.format(channelName), '.', 99, iconimage, channelDescription)
		for programme in tvGuide:
			startdatetime=datetime.datetime.fromtimestamp(programme[0]).strftime('%d/%m %H:%M')
			enddatetime=datetime.datetime.fromtimestamp(programme[1]).strftime('%H:%M')
			programmename='[{0}-{1}] [B]{2}[/B]'.format(startdatetime,enddatetime,programme[2])
			description=programme[3]
			addDir(programmename, chNum, 99, iconimage, description)
		
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin("Container.SetViewMode(504)")

def VIPList():
        addDir('[COLOR blue]links from mash23k addon [/COLOR]','','','','')
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
        addDir('[COLOR blue]end of  mash23k links [/COLOR]','','','','')

def ReadFavories():
     try:
        f = open(FAV,'r')
        fileContent=f.read()
        f.close()
        content=json.loads(fileContent)
     except:
        content=[]

     return content
  
def listFavorites():
    data=ReadFavories()
    print data
    if data==[]:
        addDir('[COLOR red]No channels in your favorits[/COLOR]','',99,'','')
        addDir('[COLOR red]ADD with right click on any channel[/COLOR]','',99,'','')
    for item in data :
        url = item["url"]
        name = item["name"].encode("utf-8")
        image = item["image"].encode("utf-8")
        i=url.find('myfilmon')
        if i >0:
			mode = 17
        else:
			mode = 16
        addDir('[COLOR yellow]'+ name+'[/COLOR]',url,mode,image,'')   
    
def addFavorites(url, iconimage, name):
    dirs=ReadFavories()
    #print dirs 
    for item in dirs:
        if item["url"] == url:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % ('ISRALIVE',  name + "  Already in  favorites", 5000, __icon2__))
            return
    if not iconimage:
		iconimage = ""
    data = {"url": url, "image": iconimage, "name": name}
    dirs.append(data)
    with open(FAV, 'w') as outfile:
		json.dump(dirs, outfile) 
    outfile.close()
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % ('ISRALIVE',  name + "  added to favorites", 5000, __icon__))
	
def removeFavorties(url):
    dirs=ReadFavories()
    #print dirs 
    for item in dirs:
        #print item
        if item["url"] == url:
          dirs.remove(item)
          with open(FAV, 'w') as outfile:
            json.dump(dirs, outfile) 
            outfile.close()
            xbmc.executebuiltin("XBMC.Container.Update('plugin://plugin.video.israelive/?description&iconimage=http%3a%2f%2fcdn3.tnwcdn.com%2ffiles%2f2010%2f07%2fbright_yellow_star.png&mode=15&name=%d7%94%d7%a2%d7%a8%d7%95%d7%a6%d7%99%d7%9d%20%d7%a9%d7%9c%d7%99&url=favorits')")
          



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
	ListLive(url)
elif mode==3 or mode==17:
	play_Filmon(url)
elif mode==4:
	downloader_is( )
elif mode==6:
	downloader_is('https://github.com/hadynz/repository.arabic.xbmc-addons/raw/master/repo/plugin.video.teledunet/plugin.video.teledunet-2.0.2.zip','Teleduent')
	downloader_is('https://github.com/downloads/hadynz/repository.arabic.xbmc-addons/repository.arabic.xbmc-addons-1.0.0.zip','Teleduent repo')
	CATEGORIES()
elif mode==7:
	update_view(url) 
elif mode==8:
	downloader_is(url,description)      
	CATEGORIES()
elif mode==9:   
	FilmonChannelGuide(url)
elif mode==11 or mode==16:
	listitem = xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
	listitem.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
elif mode==10: 
	addFavorites(url, iconimage, name)   
elif mode==15:
	listFavorites()
elif mode==18 :
	removeFavorties(url)
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
