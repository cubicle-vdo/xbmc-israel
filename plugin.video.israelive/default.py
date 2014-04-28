# -*- coding: utf-8 -*-
#code by o2ri \ avigdor based on benny123 project in navix.
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,base64,datetime,json
AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
libDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import myFilmon,commonlive,chardet,myIPTVSimple#, myTeledunet
from commonlive import *

dire=os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(dire):
	os.makedirs(dire)
__icon__='http://static2.wikia.nocookie.net/__cb20121121053458/spongebob/images/f/f4/Check-icon.png'
__icon2__='https://svn.apache.org/repos/asf/openoffice/symphony/trunk/main/extras/source/gallery/symbols/Sign-QuestionMark02-Red.png'
icon = Addon.getAddonInfo('icon')

tmpList=os.path.join(dire, 'tempList.txt')
FAV=os.path.join(dire, 'favorites.txt')
if  not (os.path.isfile(FAV)):
    f = open(FAV, 'w') 
    f.write('[]') 
    f.close() 

def CATEGORIES():
    addDir(localizedString(20101).encode('utf-8'),'settings',40,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')
    addDir(localizedString(20102).encode('utf-8'),'favorits',15,'http://cdn3.tnwcdn.com/files/2010/07/bright_yellow_star.png','')
    
    isTVlight = False if (Addon.getSetting('TV-LightPlaylist').lower() == 'false') else True
    PlxPlaylist = Addon.getSetting("PlxPlaylist")
    
    if PlxPlaylist == "0":
        ListLive('https://dl.dropboxusercontent.com/u/94071174/Online/wow/SUB/TVlight/tvlight.plx')
    elif PlxPlaylist == "1":
		ListLive('https://dl.dropboxusercontent.com/u/94071174/Online/wow/SUB/ZipTV/ZipTV.plx')
    else:
		addDir(localizedString(20103).encode('utf-8'),'https://dl.dropbox.com/u/94071174/Online/wow/DTT%2B.plx',2,'http://ftp5.bizportal.co.il/web/giflib/news/idan_plus_gay.jpg','')
		addDir(localizedString(20104).encode('utf-8'),'https://dl.dropbox.com/u/94071174/Online/wow/Kids.plx',2,'http://4hdwall.com/wp-content/uploads/2012/09/HD-cartoon-wallpaper.jpg','')
		addDir(localizedString(20105).encode('utf-8'),'https://dl.dropboxusercontent.com/u/94071174/Online/wow/Entertainment.plx',2,'http://digitalmediafilms.webs.com/Variety%20of%20Your%20Favortie%20Channels.jpg','')
		addDir(localizedString(20106).encode('utf-8'),'https://dl.dropbox.com/u/94071174/Online/wow/Movies.plx',2,'http://www.attractherdateher.com/wp-content/uploads/2012/08/movie_night.jpg','')
		addDir(localizedString(20107).encode('utf-8'),'https://dl.dropbox.com/u/94071174/Online/wow/Music.plx',2,'http://www.hdwallpapers.in/wallpapers/dance_with_me_hd_wide-1920x1200.jpg','')
		addDir(localizedString(20108).encode('utf-8'),'https://dl.dropbox.com/u/94071174/Online/wow/News.plx',2,'http://www.realtrends.com/application/view/theme/default/docs/scroll/blog6.jpg','')
		addDir(localizedString(20109).encode('utf-8'),'https://dl.dropbox.com/u/94071174/Online/wow/Science%20%26%20Nature.plx',2,'http://wallpapers.free-review.net/wallpapers/23/Nature_-_Wallpaper_for_Windows_7.jpg','')
		addDir(localizedString(20110).encode('utf-8'),'https://dl.dropbox.com/u/94071174/Online/wow/Sport.plx',2,'http://4vector.com/i/free-vector-sport-vector-pack_098139_sportsvector%20pack.jpg','')
		addDir(localizedString(20111).encode('utf-8'),'https://dl.dropbox.com/u/94071174/Online/wow/World.plx',2,'http://www.icangiveyouhouse.com/audio/2010/09/world-in-black-and-white-hands-1.jpg','')

		if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
			addDir('iLive.to','plugin://plugin.video.movie25/?iconimage=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashupArtwork%2fmaster%2fart%2filive.png&mode=119&name=iLive%20Streams&url=ilive',7,'https://raw.github.com/mash2k3/MashupArtwork/master/art/ilive.png','')
		else:
			addDir('[COLOR yellow]לחץ כאן להתקנת תוסף חסר[/COLOR]' ,'https://github.com/o2ri/xbmc-israel/blob/master/mash.zip?raw=true',8,'http://blog.missionmode.com/storage/post-images/critical-factor-missing.jpg','Mash23 addon')
		addDir('Mash Sports','plugin://plugin.video.movie25/?fanart&genre&iconimage=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashupArtwork%2fmaster%2fskins%2fvector%2fk1m05.png&mode=182&name=K1m05%20Sports&plot&url=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashUpK1m05%2fmaster%2fPlaylists%2fSports%2fSports.xml',7,'http://3.bp.blogspot.com/-gJtkhvtY1EY/UVWwH2iCGfI/AAAAAAAAA-o/b-_qJk5UMiU/s1600/Live-Sports+-+Copie.jpg','')
				
    if not os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.ArabicStreamSuperCollection'):
         addDir('[COLOR yellow]לחץ כאן להתקנת תוסף חסר[/COLOR]' ,'stam',6,'http://blog.missionmode.com/storage/post-images/critical-factor-missing.jpg','Teleduent')

def update_view(url):

    ok=True        
    xbmc.executebuiltin('XBMC.Container.Update(%s)' % url )
    return ok

def ListLive(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
	page = urllib2.urlopen(req)
	response=page.read()
	page.close()
	matches=re.compile('(.*?)#',re.I+re.M+re.U+re.S).findall(response)
	list = []
	for match in matches:
		item=re.compile('(.*?)=(.*?)\r\n',re.I+re.M+re.U+re.S).findall("{0}\r\n".format(match))
		item_data = {}
		for field, value in item:
			item_data[field.strip().lower()] = value.strip()
		if not item_data.has_key("type") or (item_data["type"]=='playlist' and item_data['name'].find('Scripts section') >= 0):
			continue
		
		name = item_data['name'].decode(chardet.detect(item_data['name'])["encoding"]).encode("utf-8")
		if item_data["type"]=='video' or item_data["type"]=='audio':
			name = '[COLOR yellow]' +name+'[/COLOR]'
			if item_data['url'].find('plugin.video.MyFilmOn') > 0:
				mode = 3
			else:
				mode = 11 
		elif item_data["type"]=='playlist':
			mode = 2
			name = '[COLOR blue]'+name+'[/COLOR]'
					
		thumb = "" if not item_data.has_key("thumb") else item_data['thumb']
		addDir(name, item_data['url'], mode, thumb, '')
		list.append({"url": item_data['url'], "image": thumb, "name": name, "type": item_data["type"]})
		
	with open(tmpList, 'w') as outfile:
		json.dump(list, outfile) 
	outfile.close()

def play_Filmon(url):
    direct, channelName, programmeName, iconimage = myFilmon.GetUrlStream(url)
    if direct == None:
    	return

    listItem = xbmcgui.ListItem(path=direct)
    listItem.setInfo(type="Video", infoLabels={ "Title": programmeName, "studio": channelName})
    listItem.setThumbnailImage(iconimage)
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

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
			image = programme[4] if programme[4] else iconimage
			addDir(programmename, chNum, 99, image, description)
		
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin("Container.SetViewMode(504)")

def ReadFavories(fileName):
     try:
        f = open(fileName,'r')
        fileContent=f.read()
        f.close()
        content=json.loads(fileContent)
     except:
        content=[]

     return content
  
def listFavorites():
    data=ReadFavories(FAV)
    if data==[]:
        addDir('[COLOR red]No channels in your favorits[/COLOR]','',99,'','')
        addDir('[COLOR red]ADD with right click on any channel[/COLOR]','',99,'','')
    for item in data :
        url = item["url"]
        name = item["name"].encode("utf-8")
        image = item["image"].encode("utf-8")
        i=url.lower().find('myfilmon')
        if i >0:
			mode = 17
        else:
			mode = 16
        addDir('[COLOR yellow]'+ name+'[/COLOR]',url,mode,image,'')   
    
def addFavorites(url, iconimage, name):
    dirs=ReadFavories(FAV)
    #print dirs 
    for item in dirs:
        if item["url"].lower() == url.lower():
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % ('ISRALIVE',  name + "  Already in  favorites", 5000, __icon2__))
            return
    
    list=ReadFavories(tmpList)	
    for item in list:
		if item["name"].lower() == name.lower():
			url = item["url"]
			iconimage = item["image"]
			type = item["type"]
    if not iconimage:
		iconimage = ""
    data = {"url": url, "image": iconimage, "name": name, "type": type}
    dirs.append(data)
    with open(FAV, 'w') as outfile:
		json.dump(dirs, outfile) 
    outfile.close()
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % ('ISRALIVE',  name + "  added to favorites", 5000, __icon__))
	
def removeFavorties(url):
    dirs=ReadFavories(FAV)
    #print dirs 
    for item in dirs:
        #print item
        if item["url"].lower() == url.lower():
          dirs.remove(item)
          with open(FAV, 'w') as outfile:
            json.dump(dirs, outfile) 
            outfile.close()
            xbmc.executebuiltin("XBMC.Container.Update('plugin://plugin.video.israelive/?description&iconimage=http%3a%2f%2fcdn3.tnwcdn.com%2ffiles%2f2010%2f07%2fbright_yellow_star.png&mode=15&name=%d7%94%d7%a2%d7%a8%d7%95%d7%a6%d7%99%d7%9d%20%d7%a9%d7%9c%d7%99&url=favorits')")

def LiveTV_Settings():
	addDir(localizedString(20001).encode('utf-8'),'settings',44,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')
	addDir(localizedString(20002).encode('utf-8'),'settings',41,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')
	addDir(localizedString(20003).encode('utf-8'),'settings',42,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')
	addDir(localizedString(20004).encode('utf-8'),'settings',43,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')
	
def RefreshIPTVlinks():
	#dp = xbmcgui.DialogProgress()
	#dp.create("ISRAELIVE","Checking for updates..")
	xbmc.executebuiltin("XBMC.Notification(ISRALIVE, Checking for updates..., {1}, {2})".format('', 5000 ,icon))
	sourceSettings = myIPTVSimple.CheckIPTVupdates()
	if sourceSettings != None:
		if sourceSettings['isFilmonUpdate'] or sourceSettings['isNewM3U']: 
			#myIPTVSimple.RefreshIPTVlinks(sourceSettings, dp)
			myIPTVSimple.RefreshIPTVlinks(sourceSettings)
		else: # if nothing changed
			message = "Everything is up to date. :-)"
			print message
			xbmc.executebuiltin("XBMC.Notification(ISRALIVE, No updates., {1}, {2})".format('', 5000 ,icon))
			##dp.update(100, line2=message, line3=' ')
			##dp.close()
	#else:
	#	dp.update(100)
	#	dp.close() 
	
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
	downloader_is('https://github.com/hadynz/repository.arabic.xbmc-addons/raw/master/repo/plugin.video.ArabicStreamSuperCollection/plugin.video.ArabicStreamSuperCollection-1.6.0.zip','Teleduent')
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
	listitem = xbmcgui.ListItem(name, iconImage='', thumbnailImage='', path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
elif mode==10: 
	addFavorites(url, iconimage, name) 
elif mode==15:
	listFavorites()
elif mode==18:
	removeFavorties(url)
elif mode==20:
	RefreshIPTVlinks()
	sys.exit()
elif mode==21:
	myIPTVSimple.DownloadLogosFolder()
	sys.exit()
#elif mode==22:
#	myIPTVSimple.UpdateIPTVSimple()
#	sys.exit()
elif mode==40:
	LiveTV_Settings()
elif mode==41:
	Addon.openSettings()
elif mode==42:
	RefreshIPTVlinks()
elif mode==43:
	myIPTVSimple.DownloadLogosFolder()
elif mode==44:
	iptvAddon = myIPTVSimple.GetIptvAddon()
	if iptvAddon != None:
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'You can use Live TV on this machine. :-)')

xbmcplugin.endOfDirectory(int(sys.argv[1]))
