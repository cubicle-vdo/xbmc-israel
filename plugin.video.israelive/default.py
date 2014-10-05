# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import sys, os, datetime, re
import urllib ,urllib2, json

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString

libDir = os.path.join(Addon.getAddonInfo("path"), 'resources', 'lib')
sys.path.insert(0, libDir)
import myFilmon,commonlive,chardet
from commonlive import *

StreramsMethod = Addon.getSetting("StreramsMethod")
filmonOldStrerams = StreramsMethod == "0"
useRtmp = StreramsMethod == "2"
__icon__='http://static2.wikia.nocookie.net/__cb20121121053458/spongebob/images/f/f4/Check-icon.png'
__icon2__='https://svn.apache.org/repos/asf/openoffice/symphony/trunk/main/extras/source/gallery/symbols/Sign-QuestionMark02-Red.png'
icon = Addon.getAddonInfo('icon')
AddonName = Addon.getAddonInfo("name")

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)

tmpList = os.path.join(user_dataDir, 'tempList.txt')
FAV = os.path.join(user_dataDir, 'favorites.txt')
if not (os.path.isfile(FAV)):
	f = open(FAV, 'w') 
	f.write('[]') 
	f.close() 

PlxPlaylist = int(Addon.getSetting("PlxPlaylist"))
if PlxPlaylist == 0:
	guideFile = os.path.join(user_dataDir, 'filmonZipGuide.txt')
	plxUrl = 'https://dl.dropboxusercontent.com/u/94071174/israelive/ZipTV.plx'
	guideUrl = "https://dl.dropboxusercontent.com/u/26001898/XBMC/israelive/filmonZipGuide.txt"
elif PlxPlaylist == 1:
	guideFile = os.path.join(user_dataDir, 'filmonLightGuide.txt')
	plxUrl = 'https://dl.dropboxusercontent.com/u/94071174/israelive/tvlight.plx'
	guideUrl = "https://dl.dropboxusercontent.com/u/26001898/XBMC/israelive/filmonLightGuide.txt"
else:
	guideFile = os.path.join(user_dataDir, 'filmonFullGuide.txt')
	plxUrl = 'https://dl.dropboxusercontent.com/u/94071174/israelive/wow.plx'
	guideUrl = "https://dl.dropboxusercontent.com/u/26001898/XBMC/israelive/filmonFullGuide.txt"
	
useFilmonEPG = Addon.getSetting("saveFilmonEPG") == "true"
if useFilmonEPG:
	if not (os.path.isfile(guideFile)):
		useFilmonEPG = False
	
def CATEGORIES():
	addDir("[B]{0}[/B]".format(localizedString(20102).encode('utf-8')),'favorits',15,'http://cdn3.tnwcdn.com/files/2010/07/bright_yellow_star.png','')
	
	if PlxPlaylist == 0 or PlxPlaylist == 1:
		ListLive(plxUrl)
	else:
		addDir("[B]{0}[/B]".format(localizedString(20103).encode('utf-8')),'https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/DTT%2B.plx',2,'http://ftp5.bizportal.co.il/web/giflib/news/idan_plus_gay.jpg','')
		addDir("[B]{0}[/B]".format(localizedString(20104).encode('utf-8')),'https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/Kids.plx',2,'http://4hdwall.com/wp-content/uploads/2012/09/HD-cartoon-wallpaper.jpg','')
		addDir("[B]{0}[/B]".format(localizedString(20105).encode('utf-8')),'https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/Entertainment.plx',2,'http://digitalmediafilms.webs.com/Variety%20of%20Your%20Favortie%20Channels.jpg','')
		addDir("[B]{0}[/B]".format(localizedString(20106).encode('utf-8')),'https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/Movies.plx',2,'http://www.attractherdateher.com/wp-content/uploads/2012/08/movie_night.jpg','')
		addDir("[B]{0}[/B]".format(localizedString(20107).encode('utf-8')),'https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/Music.plx',2,'http://www.hdwallpapers.in/wallpapers/dance_with_me_hd_wide-1920x1200.jpg','')
		addDir("[B]{0}[/B]".format(localizedString(20108).encode('utf-8')),'https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/News.plx',2,'http://www.realtrends.com/application/view/theme/default/docs/scroll/blog6.jpg','')
		addDir("[B]{0}[/B]".format(localizedString(20109).encode('utf-8')),'https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/Science%20%26%20Nature.plx',2,'http://wallpapers.free-review.net/wallpapers/23/Nature_-_Wallpaper_for_Windows_7.jpg','')
		addDir("[B]{0}[/B]".format(localizedString(20110).encode('utf-8')),'https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/Sport.plx',2,'http://4vector.com/i/free-vector-sport-vector-pack_098139_sportsvector%20pack.jpg','')
		addDir("[B]{0}[/B]".format(localizedString(20111).encode('utf-8')),'https://dl.dropboxusercontent.com/u/94071174/israelive/SUB/World.plx',2,'http://www.icangiveyouhouse.com/audio/2010/09/world-in-black-and-white-hands-1.jpg','')

		if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
			addDir('[B]iLive.to[/B]','plugin://plugin.video.movie25/?iconimage=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashupArtwork%2fmaster%2fart%2filive.png&mode=119&name=iLive%20Streams&url=ilive',7,'https://raw.github.com/mash2k3/MashupArtwork/master/art/ilive.png','')
		else:
			addDir('[COLOR yellow][B]לחץ כאן להתקנת תוסף חסר[/B][/COLOR]' ,'https://github.com/o2ri/xbmc-israel/blob/master/mash.zip?raw=true',8,'http://blog.missionmode.com/storage/post-images/critical-factor-missing.jpg','Mash23 addon')
		addDir('[B]Mash Sports[/B]','plugin://plugin.video.movie25/?fanart&genre&iconimage=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashupArtwork%2fmaster%2fskins%2fvector%2fk1m05.png&mode=182&name=K1m05%20Sports&plot&url=https%3a%2f%2fraw.github.com%2fmash2k3%2fMashUpK1m05%2fmaster%2fPlaylists%2fSports%2fSports.xml',7,'http://3.bp.blogspot.com/-gJtkhvtY1EY/UVWwH2iCGfI/AAAAAAAAA-o/b-_qJk5UMiU/s1600/Live-Sports+-+Copie.jpg','')
				
	#if not os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.teledunet'):
	#	 addDir('[COLOR yellow]לחץ כאן להתקנת תוסף חסר[/COLOR]' ,'stam',6,'http://blog.missionmode.com/storage/post-images/critical-factor-missing.jpg','Teleduent')

def update_view(url):
	ok=True		
	xbmc.executebuiltin('XBMC.Container.Update(%s)' % url )
	return ok

def ListLive(url):
	epg = None

	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
	page = urllib2.urlopen(req)
	response=page.read().replace("\r", "")
	page.close()
	matches = re.compile('^type(.*?)#$',re.I+re.M+re.U+re.S).findall(response)

	list = []
	for match in matches:
		item=re.compile('^(.*?)=(.*?)$',re.I+re.M+re.U+re.S).findall("type{0}".format(match))
		item_data = {}
		for field, value in item:
			item_data[field.strip().lower()] = value.strip()
		if not item_data.has_key("type") or (item_data["type"]=='playlist' and item_data['name'].find('Scripts section') >= 0):
			continue
		
		url = item_data['url']
		thumb = "" if not item_data.has_key("thumb") else item_data['thumb']
		description = ""
		channelName = item_data['name'].decode(chardet.detect(item_data['name'])["encoding"]).encode("utf-8")
		background = None
		if item_data["type"] == 'video' or item_data["type"] == 'audio':
			channelName = "[COLOR yellow][B]{0}[/B][/COLOR]".format(channelName)
			displayName = channelName
			if url.find('plugin.video.israelive') > 0:
				itemMode = re.compile('url=([0-9]*).*?mode=([0-9]*).*?',re.I+re.M+re.U+re.S).findall(url)
				if len(itemMode) > 0 and itemMode[0] != '':
					mode = int(itemMode[0][1])
				if mode == 1:
					mode = 3
					if useFilmonEPG:
						if epg is None:
							epg = ReadFavories(guideFile)
						programmes = GetProgrammes(epg, itemMode[0][0])
						if programmes is not None:
							programmeName = "[COLOR orange][B]{0}[/B][/COLOR] [COLOR grey][{1}-{2}][/COLOR]".format(programmes[0]["name"].encode('utf-8'), datetime.datetime.fromtimestamp(programmes[0]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[0]["end"]).strftime('%H:%M'))
							displayName = "{0} - {1}".format(channelName, programmeName)
							description = programmes[0]["description"].encode('utf-8')
							#background = thumb
							if programmes[0]["image"] is not None:
								background = programmes[0]["image"]
							if len(programmes) > 1:
								displayName = "{0} - [COLOR white]Next: [B]{1}[/B] [{2}-{3}][/COLOR]".format(displayName, programmes[1]["name"].encode('utf-8'), datetime.datetime.fromtimestamp(programmes[1]["start"]).strftime('%H:%M'), datetime.datetime.fromtimestamp(programmes[1]["end"]).strftime('%H:%M'))
			elif url.find('plugin.video.f4mTester') > 0:
				mode= 12
			else:
				mode = 11
		elif item_data["type"] == 'playlist':
			mode = 2
			channelName = "[COLOR blue][B]{0}[/B][/COLOR]".format(channelName)
			displayName = channelName
		else:
			continue
					
		addDir(displayName, url, mode, thumb, description, channelName = channelName, background=background)
		list.append({"url": url, "image": thumb, "name": channelName, "type": item_data["type"]})
		
	with open(tmpList, 'w') as outfile:
		json.dump(list, outfile) 
	outfile.close()
	
	if useFilmonEPG:
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmc.executebuiltin("Container.SetViewMode(504)")
		
def Playf4m(url, name=None, iconimage=None):
	i = url.find('http://')
	if url.find('keshet') > 0:
		makoTicket = OPEN_URL('http://mass.mako.co.il/ClicksStatistics/entitlementsServices.jsp?et=gt&rv=akamai')
		result = json.loads(makoTicket)
		ticket = result['tickets'][0]['ticket']
		url = "{0}%3F{1}%26hdcore%3D3.0.3".format(url[i:], ticket)
	else:
		url = url[i:]
	
	print url
	if name is not None:
		name = urllib.unquote_plus(name)
		
	from F4mProxy import f4mProxyHelper
	player = f4mProxyHelper()
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
	#player.playF4mLink(urllib.unquote_plus(url), name, use_proxy_for_chunks=True)
	player.playF4mLink(urllib.unquote_plus(url), name, use_proxy_for_chunks=True, iconimage=iconimage)
	
def play_Filmon(url):
	direct, channelName, programmeName, iconimage = myFilmon.GetUrlStream(url, filmonOldStrerams, useRtmp)
	if direct == None:
		return

	listItem = xbmcgui.ListItem(path=direct)
	listItem.setInfo(type="Video", infoLabels={"Title": programmeName})
	#listItem.setInfo(type="Video", infoLabels={ "studio": channelName})
	listItem.setInfo(type="Video", infoLabels={"tvshowtitle": channelName, "episode": "0", "season": "0"})
	listItem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

def FilmonChannelGuide(url):
	chNum, referrerCh, ChName = myFilmon.GetUrlParams(url)
	if referrerCh != None:
		addDir('[COLOR red][B]No TV-Guide for this channel.[/B][/COLOR]', '.', 99, '', '')
		return
		
	channelName, channelDescription, iconimage, tvGuide = myFilmon.GetChannelGuide(chNum, filmonOldStrerams)

	if tvGuide == None:
		addDir('[COLOR red][B]No TV-Guide for this channel.[/B][/COLOR]', '.', 99, '', '')
		return
	elif len(tvGuide) == 0:
		addDir('[COLOR red][B]No TV-Guide for "{0}".[/B][/COLOR]'.format(channelName), '.', 99, iconimage, channelDescription)
	else:
		addDir('------- [COLOR yellow][B]{0}[/COLOR] [COLOR orange]- TV-Guide[/B][/COLOR] -------'.format(channelName), '.', 99, iconimage, channelDescription)
		day = ""
		for programme in tvGuide:
			startdate = datetime.datetime.fromtimestamp(programme["start"]).strftime('%d/%m/%y')
			if startdate != day:
				day = startdate
				addDir('[COLOR white][B]{0}:[/B][/COLOR]'.format(day), '.', 99, iconimage, channelDescription)
			startdatetime = datetime.datetime.fromtimestamp(programme["start"]).strftime('%H:%M')
			enddatetime = datetime.datetime.fromtimestamp(programme["end"]).strftime('%H:%M')
			programmename = '[COLOR orange][{0}-{1}][/COLOR] [COLOR yellow][B]{2}[/B][/COLOR]'.format(startdatetime,enddatetime,programme["name"])
			description = programme["description"]
			image = programme["image"] if programme["image"] else iconimage
			addDir(programmename, chNum, 99, image, description)
		
	xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
	xbmc.executebuiltin("Container.SetViewMode(504)")

def GetProgrammes(epg, channelName ,full=False):
	programmes = []
	try:
		matches = [x["tvGuide"] for x in epg if x["channel"] == int(channelName)]
		programmes = matches[0]
	except:
		pass

	if (full):
		return programmes
		
	retProgrammes = []
	now = int(time.time())
	programmesCount = len(programmes)

	for i in range(programmesCount):
		programme = programmes[i]
		start = programmes[i]["start"]
		stop = programmes[i]["end"]
		if (start < now and now < stop):
			retProgrammes.append(programme)
			if i+1 < programmesCount:
				retProgrammes.append(programmes[i+1])
			return retProgrammes
			
	return None
	
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
	for item in data:
		url = item["url"]
		print url
		name = item["name"].encode("utf-8")
		image = item["image"].encode("utf-8")

		if url.lower().find('israelive') > 0:
			mode = 17
		elif url.lower().find('f4mtester') > 0:
			mode = 13
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
		#if urllib.unquote_plus(item["name"].lower()) == name.lower():
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
			xbmc.executebuiltin("XBMC.Container.Update('{0}/?description&iconimage=http%3a%2f%2fcdn3.tnwcdn.com%2ffiles%2f2010%2f07%2fbright_yellow_star.png&mode=15&name=%d7%94%d7%a2%d7%a8%d7%95%d7%a6%d7%99%d7%9d%20%d7%a9%d7%9c%d7%99&url=favorits')".format(AddonID))

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
		#name=urllib.unquote_plus(params["name"])
		name=params["name"]
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
elif mode==1:
	play_Filmon(sys.argv[2])
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
	#listitem = xbmcgui.ListItem(urllib.unquote_plus(name), iconImage='', thumbnailImage='', path=url)
	listitem = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
elif mode==10: 
	addFavorites(url, iconimage, name) 
elif mode==12 or mode==13:
	Playf4m(url, name, iconimage)
elif mode==15:
	listFavorites()
elif mode==18:
	removeFavorties(url)
elif mode == 20:
	try:
		xbmc.executebuiltin("XBMC.Notification({0}, Making and saving Filmon's guide..., {1}, {2})".format(AddonName, 300000 ,icon))
		myFilmon.MakePLXguide(plxUrl, guideFile)
		xbmc.executebuiltin("XBMC.Notification({0}, Filmon's guide saved., {1}, {2})".format(AddonName, 5000 ,icon))
	except:
		xbmc.executebuiltin("XBMC.Notification({0}, Filmon's guide NOT saved!, {1}, {2})".format(AddonName, 5000 ,icon))
	sys.exit()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
