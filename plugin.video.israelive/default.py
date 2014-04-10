# -*- coding: utf-8 -*-
#code by o2ri \ avigdor based on benny123 project in navix.
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,base64,datetime,json
AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)
libDir = os.path.join(xbmc.translatePath("special://home/addons/"), AddonID, 'resources', 'lib')
sys.path.insert(0, libDir)
import myFilmon,commonlive,chardet#, myTeledunet
from commonlive import *

dire=os.path.join(xbmc.translatePath( "special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(dire):
	os.makedirs(dire)
__icon__='http://static2.wikia.nocookie.net/__cb20121121053458/spongebob/images/f/f4/Check-icon.png'
__icon2__='https://svn.apache.org/repos/asf/openoffice/symphony/trunk/main/extras/source/gallery/symbols/Sign-QuestionMark02-Red.png'
tmpList=os.path.join(dire, 'tempList.txt')
FAV=os.path.join(dire, 'favorites.txt')
if  not (os.path.isfile(FAV)):
    f = open(FAV, 'w') 
    f.write('[]') 
    f.close() 

def CATEGORIES():
    addDir('הגדרות Live TV','settings',40,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')
    addDir('הערוצים שלי','favorits',15,'http://cdn3.tnwcdn.com/files/2010/07/bright_yellow_star.png','')
    
    isTVlight = False if (Addon.getSetting('TV-LightPlaylist').lower() == 'false') else True
    
    if isTVlight == True:
        ListLive('https://dl.dropboxusercontent.com/u/94071174/Online/wow/SUB/TVlight/tvlight.plx')
    else:
		addDir('עידן פלוס','https://dl.dropbox.com/u/94071174/Online/wow/DTT%2B.plx',2,'http://ftp5.bizportal.co.il/web/giflib/news/idan_plus_gay.jpg','')
		addDir('ילדים','https://dl.dropbox.com/u/94071174/Online/wow/Kids.plx',2,'http://4hdwall.com/wp-content/uploads/2012/09/HD-cartoon-wallpaper.jpg','')
		addDir('בידור','https://dl.dropboxusercontent.com/u/94071174/Online/wow/Entertainment.plx',2,'http://digitalmediafilms.webs.com/Variety%20of%20Your%20Favortie%20Channels.jpg','')
		addDir('סרטים','https://dl.dropbox.com/u/94071174/Online/wow/Movies.plx',2,'http://www.attractherdateher.com/wp-content/uploads/2012/08/movie_night.jpg','')
		addDir('מוזיקה','https://dl.dropbox.com/u/94071174/Online/wow/Music.plx',2,'http://www.hdwallpapers.in/wallpapers/dance_with_me_hd_wide-1920x1200.jpg','')
		addDir('חדשות','https://dl.dropbox.com/u/94071174/Online/wow/News.plx',2,'http://www.realtrends.com/application/view/theme/default/docs/scroll/blog6.jpg','')
		addDir('מדע וטבע','https://dl.dropbox.com/u/94071174/Online/wow/Science%20%26%20Nature.plx',2,'http://wallpapers.free-review.net/wallpapers/23/Nature_-_Wallpaper_for_Windows_7.jpg','')
		addDir('ספורט','https://dl.dropbox.com/u/94071174/Online/wow/Sport.plx',2,'http://4vector.com/i/free-vector-sport-vector-pack_098139_sportsvector%20pack.jpg','')
		addDir('עולם','https://dl.dropbox.com/u/94071174/Online/wow/World.plx',2,'http://www.icangiveyouhouse.com/audio/2010/09/world-in-black-and-white-hands-1.jpg','')

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
	link=OPEN_URL(url)
	#print link
	link=unescape(link)
	
	matches1=re.compile('pe=(.*?)#',re.I+re.M+re.U+re.S).findall(link)
	list = []
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
				name = name.decode(chardet.detect(name)["encoding"]).encode("utf-8")
				name = '[COLOR yellow]' +name+'[/COLOR]'
				if url.find('plugin.video.MyFilmOn') > 0:
					mode = 3
				else:
					mode = 11 
				addDir(name, url, mode, thumb, '')
				data = {"url": url, "image": thumb, "name": name}
				list.append(data)
		else:
			regex='name=(.*?)URL=(.*?).plx'
			matches=re.compile(regex,re.I+re.M+re.U+re.S).findall(match)
			for name,url in matches:
				url=url+'.plx'
				if name.find('Scripts section') < 0 :
					thumb=''
					i=name.find('thumb')
					if i>0:
						thumb=name[i+6:]
						name=name[0:i]
					name = name.decode(chardet.detect(name)["encoding"]).encode("utf-8")
					name = '[COLOR blue]'+name+'[/COLOR]'
					addDir(name,url,2,thumb,'')
					data = {"url": url, "image": None, "name": name}
					list.append(data)

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

def LiveTV_Settings():
	addDir('בדיקת תאימות Live TV','settings',44,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')
	addDir('הצגת הגדרות התוסף','settings',41,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')
	addDir('רענון תחנות Live TV','settings',42,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')
	addDir('הורדת חבילת סמלי ערוצים','settings',43,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQdhwAJTHe3O3EFl7wV_vj1MA-jymE-_6x7RsklkF86gYGQbwEX','')

def GetIptvAddon():
	import platform
	
	if os.path.exists(xbmc.translatePath("special://home/addons/") + 'pvr.iptvsimple') or os.path.exists(xbmc.translatePath("special://xbmc/addons/") + 'pvr.iptvsimple'):
		#addDir('[COLOR yellow][B] PVR IPTVSIMPLE INSTALLED ON YOUR MACHINE. PLEASE ENABLE IT IN XBMC SETTINGS[/B][/COLOR]','stam',99,'','')
		return xbmcaddon.Addon("pvr.iptvsimple")
		
	osType = platform.system()
	osVer = platform.release()
	xbmcVer = xbmc.getInfoLabel( "System.BuildVersion" )[:2]

	if osType == "Windows":
		if int(xbmcVer) > 12:
			downloader_is("https://dl.dropboxusercontent.com/u/5461675/pvr.iptvsimple.1.9.3.win32.zip", "IPTVSIMPLE version 1.9.3")
			#addDir('Install PVR IPTVSIMPLE','https://dl.dropboxusercontent.com/u/5461675/pvr.iptvsimple.1.9.3.win32.zip',12,'','IPTVSIMPLE version 1.9.3')
		else: # frodo i hope...
			downloader_is("https://dl.dropboxusercontent.com/u/5461675/pvr.iptvsimple.1.6.1.win32.zip", "IPTVSIMPLE version 1.6.1")
			#addDir('Install PVR IPTVSIMPLE', 'https://dl.dropboxusercontent.com/u/5461675/pvr.iptvsimple.1.6.1.win32.zip',12,'','IPTVSIMPLE version 1.6.1') 
		return xbmcaddon.Addon("pvr.iptvsimple")
	else:
		msg1 = "PVR IPTVSimple is NOT installed on your machine."
		msg2 = "Please install XBMC version that include IPTVSimple in it."
		#addDir('[COLOR yellow][B]{0} {1}[/B][/COLOR]'.format(msg1, msg2), 'stam', 99, '', '')
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', msg1, msg2)
		return None

def GetTVLightSettings(isIptvAddonGotham):
	staticM3UdefaultUrl = "https://www.dropbox.com/s/oti2i7rl9eyw1x3/iptv.m3u?dl=1" # --> Default Frodo <--
	staticM3UdefaultGothamUrl = "https://www.dropbox.com/s/tk28rx6lvwta5i1/iptv_v13.m3u?dl=1" # --> Default Gotham <--
	
	d = {'packageFolder': os.path.join(dire, 'TVLight')}
	
	d['FilmonChannelsURL'] = "https://www.dropbox.com/s/ivzyeswaj61l6ev/FilmonChannels.txt?dl=1"
	d['FilmonLastUpdateURL'] = "https://www.dropbox.com/s/qxst2r0brfvi5i5/FilmonLastUpdate.txt?dl=1"
	d['staticM3Uurl'] = staticM3UdefaultGothamUrl if isIptvAddonGotham else staticM3UdefaultUrl # Take URL for static-channels by xbmc version from default URLs.
	d['staticM3UlastUpdateUrl'] = "https://www.dropbox.com/s/dthhfdv7223rjj0/iptvLastUpdate.txt?dl=1"

	d['logoBaseUrl'] = "https://www.dropbox.com/sh/94r40pxohmi415p/xa7wCOsPPS?dl=1"
	
	d['IPTVepgPathType'] = "1"
	#d['IPTVepgUrl'] = "https://www.dropbox.com/s/l8w7m1dcyzwxtz0/guide.xml?dl=1"
	d['IPTVepgUrl'] = "https://copy.com/IzBkjGdaPq8w?download=1"
	d['IPTVlogoPathType'] = "0"
	d['IPTVlogoPath'] = os.path.join(dire, 'Channel Logos')
	d['IPTVm3uPathType'] = "0"
	d['IPTVm3uPath'] = os.path.join(d['packageFolder'], 'myM3U.m3u')

	return d
	
def GetEnglishOptimizedSettings(isIptvAddonGotham):
	staticM3UdefaultUrl = "https://www.dropbox.com/s/rv5eiiiyxb8uqb2/iptv.m3u?dl=1" # --> Default Frodo <--
	staticM3UdefaultGothamUrl = "https://www.dropbox.com/s/dfxzz5t6cpafon3/iptv_v13.m3u?dl=1" # --> Default Gotham <--
	
	d = {'packageFolder': os.path.join(dire, 'EnglishOptimized')}
	
	d['FilmonChannelsURL'] = "https://www.dropbox.com/s/qoii81a7ps4ds63/FilmonChannels.txt?dl=1"
	d['FilmonLastUpdateURL'] = "https://www.dropbox.com/s/slk6r3wq5evy7r2/FilmonLastUpdate.txt?dl=1"
	d['staticM3Uurl'] = staticM3UdefaultGothamUrl if isIptvAddonGotham else staticM3UdefaultUrl # Take URL for static-channels by xbmc version from default URLs.
	d['staticM3UlastUpdateUrl'] = "https://www.dropbox.com/s/s6cco122w7o1pwj/iptvLastUpdate.txt?dl=1"
	
	d['logoBaseUrl'] = "https://www.dropbox.com/sh/94r40pxohmi415p/xa7wCOsPPS?dl=1"
	
	d['IPTVepgPathType'] = "1"
	#d['IPTVepgUrl'] = "https://www.dropbox.com/s/l8w7m1dcyzwxtz0/guide.xml?dl=1"
	d['IPTVepgUrl'] = "https://copy.com/IzBkjGdaPq8w?download=1"
	d['IPTVlogoPathType'] = "0"
	d['IPTVlogoPath'] = os.path.join(dire, 'Channel Logos')
	d['IPTVm3uPathType'] = "0"
	d['IPTVm3uPath'] = os.path.join(d['packageFolder'], 'myM3U.m3u')

	return d

def GetSourceSettings():
	iptvAddon = GetIptvAddon()
	if iptvAddon == None:
		return None, None
	
	isIptvAddonGotham = iptvAddon.getAddonInfo('version')  >= "1.9.3"
	iptvPackage = Addon.getSetting("iptvPackage")
	
	if iptvPackage == "0":
		sourceSettings = GetTVLightSettings(isIptvAddonGotham)
	elif iptvPackage == "1":
		sourceSettings = GetEnglishOptimizedSettings(isIptvAddonGotham)
	
	return iptvAddon, sourceSettings

def RefreshIPTVlinks():
	iptvAddon, sourceSettings = GetSourceSettings()
	if iptvAddon == None:
		return
	
	FilmonChannelsURL = sourceSettings['FilmonChannelsURL']
	FilmonLastUpdateURL = sourceSettings['FilmonLastUpdateURL']

	isForceFilmonScan = False if (Addon.getSetting('ForceFilmonScan').lower() == 'false') else True

	staticM3Uurl = sourceSettings['staticM3Uurl']
	staticM3UlastUpdateUrl = sourceSettings['staticM3UlastUpdateUrl']
	
	packageFolder = sourceSettings['packageFolder']
	
	if not os.path.exists(packageFolder):
		os.makedirs(packageFolder)
	
	# --- Locals files ---
	localFilmonLastUpdateFile = os.path.join(packageFolder, 'FilmonLastUpdate.txt')
	localOldM3Ufile = os.path.join(packageFolder, 'iptv.m3u')
	localM3ULastUpdateFile = os.path.join(packageFolder, 'iptvLastUpdate.txt')
	localIPFile = os.path.join(packageFolder, 'myPublicIP.txt') # stored IP in file for compare on next run (if IP chaneged, there is need to refresh filmon's channels). 
	localFilmonM3Ufile = os.path.join(packageFolder, 'myFilmonM3U.m3u') # store filmon's links.
	finalM3Ufilename = os.path.join(packageFolder, 'myM3U.m3u') # The final m3u file. (static + filmon links)
	errorLogFile = os.path.join(packageFolder, 'iptvErr.log') # log errors.
	
	UpdateIPTVSimpleSettings(iptvAddon, sourceSettings) # check and update iptv-simple settings if nesessery
	
	dp = xbmcgui.DialogProgress()
	dp.create("ISRAELIVE","Checking for changes..")
	dp.update(0)
	
	M3ULastUpdate = OPEN_URL(staticM3UlastUpdateUrl) # get static channels' last update from server.
	
	if not os.path.isfile(localM3ULastUpdateFile): # compare last update against local file (if exist)
		f = open(localM3ULastUpdateFile,'w')
		f.write(M3ULastUpdate)
		fileContent = ''
		f.close()
	else:
		f = open(localM3ULastUpdateFile,'r')
		fileContent = f.read()
		f.close()
	
	isNewM3U = M3ULastUpdate != fileContent # check if static channels changed
	m3uVer = M3ULastUpdate if isNewM3U else fileContent
	change = "List changed." if isNewM3U else "List didn't changed."
	dp.update(0, line2=change, line3=' ')

	myIP = json.load(urllib2.urlopen('http://httpbin.org/ip'))['origin'] # get current IP
	#myIP = urllib2.urlopen('http://ip.42.pl/raw').read()
	
	isFilmonUpdate = isForceFilmonScan
	
	if not os.path.isfile(localIPFile): # compare with previous IP (if exist)
		f = open(localIPFile,'w')
		f.write(myIP)
		fileContent = ''
		f.close()
	else:
		f = open(localIPFile,'r')
		fileContent = f.read()
		f.close()
	
	isNewIP = myIP != fileContent # check if IP changed
	change = "IP changed." if isNewIP else "IP didn't changed."
	dp.update(0, line2=myIP, line3=change)
	if isNewIP:
		isFilmonUpdate = True

	FilmonLastUpdate = OPEN_URL(FilmonLastUpdateURL) # get filmon channels' last update from server.
	
	if not os.path.isfile(localFilmonLastUpdateFile): # compare last update against local file (if exist)
		f = open(localFilmonLastUpdateFile,'w')
		f.write(FilmonLastUpdate)
		fileContent = ''
		f.close()
	else:
		f = open(localFilmonLastUpdateFile,'r')
		fileContent = f.read()
		f.close()
	
	isNewFilmonList = FilmonLastUpdate != fileContent # check if filmon channels changed
	filmonVer = FilmonLastUpdate if isNewFilmonList else fileContent
	
	maxVer = m3uVer if m3uVer > filmonVer else filmonVer
	iptvVer = "{0}.{1}.{2} - {3}:{4}".format(maxVer[6:8], maxVer[4:6], maxVer[2:4], maxVer[8:10], maxVer[10:12])
	
	if not isFilmonUpdate:
		change = "Filmon list changed." if isNewFilmonList else "Filmon list didn't changed."
		dp.update(0, line2=change, line3=' ')
		if isNewFilmonList:
			isFilmonUpdate = True
	
	if not isFilmonUpdate and not isNewM3U: # if nothing changed
		message = "Everything is up to date. :-)"
		print message
		dp.update(100, line2=message, line3=' ')
		dp.close()
		xbmc.executebuiltin("Notification(ISRALIVE, {0}, 5000, {1})".format(message, __icon__))
		return
	
	if isNewM3U or not os.path.isfile(localOldM3Ufile): # if static channels updated or local file is missing
		OldM3U = OPEN_URL(staticM3Uurl).replace('\r','')
			
		f = open(localOldM3Ufile,'w')
		f.write(OldM3U)
		f.close()
		f = open(localM3ULastUpdateFile,'w')
		f.write(M3ULastUpdate)
		f.close()
	else:	# use local static list
		f = open(localOldM3Ufile,'r')
		OldM3U = f.read()
		f.close()
		
	if isFilmonUpdate or not os.path.isfile(localFilmonM3Ufile): # if IP cahnged or filmon channels updated or local file is missing
		fileContent = OPEN_URL(FilmonChannelsURL) # load filmon channels to be scan into a list
		channels = json.loads(fileContent)

		isIptvAddonGotham = iptvAddon.getAddonInfo('version')  >= "1.9.3"
		
		M3Ulist, errorLog = myFilmon.MakeM3ULinks(channels, dp, isIptvAddonGotham) # make m3u-links for filmon channels
		
		if M3Ulist == None: # if there is critical error (couldn't load any file) or canceled by user.
			f = open(errorLogFile, 'w')
			f.write(errorLog)
			f.close()
			print errorLog
			dp.update(100)
			dp.close() 
			dlg = xbmcgui.Dialog()
			dlg.ok('ISRAELIVE', 'Cannot create links.', "See iptvErr.log")
			#xbmc.executebuiltin("Notification(ISRALIVE, Cannot create all links - see iptvErr.log, 5000, {0})".format(__icon2__))
			return
		
		f = open(localFilmonM3Ufile,'w') # store local m3u for filmon channels
		f.write(M3Ulist)
		f.close()
		
		if isNewIP:
			f = open(localIPFile,'w') # store current IP
			f.write(myIP)
			f.close()
		
		f = open(localFilmonLastUpdateFile,'w') # store last update of filmon's m3u file
		f.write(FilmonLastUpdate)
		f.close()
	else: # use local filmon list
		f = open(localFilmonM3Ufile,'r')
		M3Ulist = f.read()
		f.close()
		errorLog = ''
	
	f = open(finalM3Ufilename, 'w') # make the finnal m3u list (this file will used in IPTVSimple)
	finalList = MakeFinalM3UList(OldM3U, M3Ulist)
	finalM3Ulist = '#EXTM3U\n\n#EXTINF:-1 tvg-id="IPTVVersion" tvg-name="IPTVVersion",LiveTV V.{0}\nhttp://udp\n'.format(iptvVer)
	for item in finalList:
		finalM3Ulist += "\n{0}\n".format(item["link"])
	f.write(finalM3Ulist)
	f.close()

	f = open(errorLogFile, 'w') # write the error log
	f.write(errorLog)
	f.close()

	if isForceFilmonScan: # make user to check force scan manualy (scan won't run automaticaly every time).
		Addon.setSetting('ForceFilmonScan', 'false')
		
	if errorLog != '':
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'Links updated.', "Please restart XBMC.", "Some links didn't created - see iptvErr.log")
		#xbmc.executebuiltin("Notification(ISRALIVE, Cannot create all links - see iptvErr.log, 5000, {0})".format(__icon2__))
	else:
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'Links updated.', "Please restart XBMC.")
		#xbmc.executebuiltin("Notification(ISRALIVE, Links updated - Please reset the PVR database., 5000, {0})".format(__icon__))
	if os.path.exists(xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple")):
		DeleteCache()

def MakeFinalM3UList(staticM3U, filmonM3U):
	list = []
	
	matches=re.compile('#([0-9]+)#\n(.*?)\n\n',re.I+re.M+re.U+re.S).findall(staticM3U)
	for index, link in matches:
		item_data = {'index': int(index), 'link': link}
		list.append(item_data)
	
	matches=re.compile('#([0-9]+)#\n(.*?)\n\n',re.I+re.M+re.U+re.S).findall(filmonM3U)
	for index, link in matches:
		item_data = {'index': int(index), 'link': link}
		list.append(item_data)
		
	return sorted(list, key=lambda k: k['index'])
	
def UpdateIPTVSimpleSettings(iptvAddon, sourceSettings):
	iptvSettingsFile = os.path.join(xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple" ).decode("utf-8"), "settings.xml")
	if not os.path.isfile(iptvSettingsFile):
		iptvAddon.setSetting("m3uPath", sourceSettings['IPTVm3uPath']) # make 'settings.xml' in 'userdata/addon_data/pvr.iptvsimple' folder
	
	# get settings.xml into dictionary
	import xml.etree.ElementTree as ET

	tree = ET.parse(iptvSettingsFile)
	elements = tree.findall('*')

	dict = {}
	for elem in elements:
		dict[elem.get('id')] = elem.get('value')
		
	# make changes
	dict["epgPathType"] = sourceSettings["IPTVepgPathType"]
	dict["epgUrl"] = sourceSettings["IPTVepgUrl"]
	dict["logoPathType"] = sourceSettings["IPTVlogoPathType"]
	dict["logoPath"] = sourceSettings["IPTVlogoPath"]
	dict["m3uPathType"] = sourceSettings['IPTVm3uPathType']
	dict["m3uPath"] = sourceSettings['IPTVm3uPath']
		
	#make new settings.xml (string)
	xml = "<settings>\n"
	for k, v in dict.iteritems():
		xml += '\t<setting id="{0}" value="{1}" />\n'.format(k, v)
	xml += "</settings>\n"
	
	# write updates back to settings.xml
	f = open(iptvSettingsFile, 'w') 
	f.write(xml)
	f.close()

def UpdateIPTVSimple():
	iptvAddon, sourceSettings = GetSourceSettings()
	if iptvAddon == None:
		return
	
	UpdateIPTVSimpleSettings(iptvAddon, sourceSettings)
	
	dlg = xbmcgui.Dialog()
	dlg.ok('ISRAELIVE', 'IPTV-Simple updated.', "Please restart XBMC.")
			
def DownloadLogosFolder():
	import downloader,extract
	
	iptvAddon, sourceSettings = GetSourceSettings()
	if iptvAddon == None:
		return
		
	logosUrl = sourceSettings["logoBaseUrl"] # Base URL for logos of channels
	logoPath = sourceSettings["IPTVlogoPath"]
	zipFile = os.path.join(sourceSettings["packageFolder"], 'logos.zip')

	dp = xbmcgui.DialogProgress()
	dp.create("ISRAELIVE", "Logo Icons Downloading...", '', 'Please Wait')
	
	if not os.path.exists(sourceSettings["packageFolder"]):
		os.makedirs(sourceSettings["packageFolder"])
	
	try: os.remove(zipFile)
	except:	pass
	
	downloader.download(logosUrl, zipFile, dp)
	
	if not os.path.exists(logoPath):
		os.makedirs(logoPath)
	
	dp.update (0, "", "Extracting Zip Please Wait")
	extract.all(zipFile ,logoPath, dp)
	
	try: os.remove(zipFile)
	except:	pass

	UpdateIPTVSimpleSettings(iptvAddon, sourceSettings) # check and update iptv-simple settings if nesessery
		
	dlg = xbmcgui.Dialog()
	dlg.ok('ISRAELIVE', 'Logo Pack Download Complete')
	
def DeleteCache():
	mypath=xbmc.translatePath( "special://userdata/addon_data/pvr.iptvsimple" ).decode("utf-8")
	for f in os.listdir(mypath):
		if os.path.isfile(os.path.join(mypath,f)):
			if f.endswith('cache'):
				os.remove(os.path.join(mypath,f))

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
    if not iconimage:
		iconimage = ""
    data = {"url": url, "image": iconimage, "name": name}
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
	#if url.find('plugin.video.ArabicStreamSuperCollection') > 0:
	#	url = myTeledunet.PlayTeledunet(re.compile('url=(.+?)&').findall(url)[0])
	listitem = xbmcgui.ListItem(name, iconImage='', thumbnailImage='', path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
elif mode==10: 
	addFavorites(url, iconimage, name) 
#elif mode==12:
#	downloader_is(url,description)
#	if os.path.exists(xbmc.translatePath("special://home/addons/") + 'pvr.iptvsimple'):
#		RefreshIPTVlinks()	
elif mode==15:
	listFavorites()
elif mode==18:
	removeFavorties(url)
elif mode==20:
	RefreshIPTVlinks()
	sys.exit()
elif mode==21:
	DownloadLogosFolder()
	sys.exit()
elif mode==22:
	UpdateIPTVSimple()
	sys.exit()
elif mode==40:
	LiveTV_Settings()
elif mode==41:
	Addon.openSettings()
elif mode==42:
	RefreshIPTVlinks()
elif mode==43:
	DownloadLogosFolder()
elif mode==44:
	iptvAddon = GetIptvAddon()
	if iptvAddon != None:
		dlg = xbmcgui.Dialog()
		dlg.ok('ISRAELIVE', 'You can use Live TV on this machine. :-)')

xbmcplugin.endOfDirectory(int(sys.argv[1]))
