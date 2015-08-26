# -*- coding: utf-8 -*-
import os, urllib, re, random, json, datetime
import xbmcaddon, xbmc, xbmcplugin, xbmcgui

Addon = xbmcaddon.Addon(id='plugin.video.movixws')
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
libDir = os.path.join(addonPath, 'resources', 'lib')
sys.path.insert(0, libDir)
import resolver, repoCheck, common

Domain = Addon.getSetting("domain")
baseUrl = Domain[:-1] if Domain.endswith('/') else Domain
#print baseUrl
handle = int(sys.argv[1])

def searchWs():
	search_entered = ''
	isText = False
	keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
	keyboard.doModal()
	if keyboard.isConfirmed():
		search_entered = urllib.quote_plus(keyboard.getText())
	isText = False if search_entered.strip() == '' else True
	dialog = xbmcgui.Dialog()
	filter = dialog.select("בחר סוג חיפוש", ["הכל", "סרטים", "סדרות"])
	if filter == 1:
		search_entered += "&sortby=movie"
	elif filter == 2:
		search_entered += "&sortby=tv-show"
	isYear = False
	yearsRange = list((range(datetime.datetime.now().year, 1933, -1)))
	years = [str(year) for year in yearsRange]
	years.insert(0, "הכל")
	year = dialog.select("הצג תוצאות לפי שנה", years)
	if year != 0:
		search_entered += "&year={0}".format(years[year])
		isYear = True
	if isText or isYear:
		return IndexPage('{0}/search_movies?q={1}'.format(baseUrl, search_entered))
	else:
		return False

def IndexPage(url):
	if not 'page' in url:
		if 'search_movies' in url:
			url = url + '&page=/0'
		else:
			url = url + '/page/0'
	current_page = int(url.split('/')[-1])
	result = common.OPEN_URL(url)
	block = re.compile('pnation.*?</strong>(.*?)<\/div>',re.I+re.M+re.U+re.S).findall(result)
	pages = "" if len(block) == 0 else re.compile('<a href=".*?[\/&]page[=]?\/(.*?)">(.*?)</a>',re.I+re.M+re.U+re.S).findall(block[0])

	nextPagesCount = len(pages)
	step = 10000 if nextPagesCount == 0 else int(pages[0][0]) - current_page
	last_page = current_page if nextPagesCount == 0 else int(pages[-1][0])
	for i in range(nextPagesCount-1, -1, -1):
		if pages[i][1] == '':
			continue
		if int(pages[i][0]) > last_page:
			last_page = int(pages[i][0])
		break

	for pageIndex in range(10):
		try:
			result = common.OPEN_URL(url)
			matches = re.compile('<div class=\"mov\".*? <img src="(.*?)".*?<h3><a href="(.*?)">(.*?)<.*?<p class=\"ic_text\">(.*?)<\/p>',re.I+re.M+re.U+re.S).findall(result)
			for match in matches:
				addDir(match[2],'{0}{1}'.format(baseUrl, match[1]), 4, match[0], True, match[3])
		except Exception as ex:
			print ex 
		if current_page >= last_page:
			return True
		current_page += step
		url = url[:url.rfind('/')+1]
		url += str(current_page)
	
	if current_page <= last_page:
		addDir('[COLOR blue]תוצאות נוספות[/COLOR]', url, 2, '')
	return True

def addDir(name, url, mode, iconimage, isFolder=True, description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": str(description)} )
	if not isFolder:
		liz.setProperty("IsPlayable","true")
	xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=liz,isFolder=isFolder)

def GetSeasons(series_num, iconimage, description):
	result=common.OPEN_URL('{0}/watchmovies/get_seasons/{1}'.format(baseUrl, series_num))
	matches=re.compile('onclick=\"get_episodes\(\'(.*?)\'\);\">(.*?)<',re.I+re.M+re.U+re.S).findall(result)
	for season in matches:
		addDir('{0}  {1}'.format(name, season[1]), '{0}/watchmovies/get_episodes/{1}?seasonid={2}'.format(baseUrl, series_num, season[0]), 3, iconimage, True, description)

def GetEpisodes(url, iconimage, description):
	result=common.OPEN_URL(url)
	matches=re.compile('onclick=\"get_episode\(\'(.*?)\',\'(.*?)\'\);\">(.*?)<',re.I+re.M+re.U+re.S).findall(result)
	url=url.replace('get_episodes','get_episode')
	for episode in matches:
		addDir(name +'  '+episode[2], url+'&episodeid='+episode[1], 4, iconimage, True, description)

def SortByQuality(links):
	qualitiesList = ["1080p", "720p", "BDRip", "BRRip", "DVDRip", "HDTV", "HDRip", "R5", "DVDSCR", "WEBRip", "PDTV", "TVRip", "TC", "HDTS", "TS", "CAM"]
	sortedLinks = []
	random.seed()
	random.shuffle(links)
	for quality in qualitiesList:
		qualityLinks = [link for link in links if link[2].lower() == quality.lower()]
		for qualityLink in qualityLinks:
			sortedLinks.append(qualityLink)
	for link in links:
		if link[2] not in qualitiesList:
			sortedLinks.append(link)
	return sortedLinks

def LinksPage(url, iconimage, description):
	result=common.OPEN_URL(url)
	matches=re.compile('<div style="width:540px;padding-top:5px;">(.+?)</div>',re.I+re.M+re.U+re.S).findall(result)
	if len(matches) == 1:
		description = matches[0]
	matches=re.compile('<div class="alert submit-link-div".+?<iframe src="(.+?)".+?</iframe>',re.I+re.M+re.U+re.S).findall(result)
	if len(matches) == 1:
		addDir('[COLOR green]{0} - טריילר[/COLOR]'.format(name), matches[0], 8, iconimage, False, description)
	if not 'get_seasons' in result:
		matches=re.compile('<li .+?id="wrapserv"><a href="(.+?)" target.*?src="\/img\/servers\/(.+?).png.+?<div class="span3".+?<b>איכות (.+?)<\/b>.+?<\/li>',re.I+re.M+re.U+re.S).findall(result)
		links = []
		for match in matches:
			if "goodvideohost" in match[1]:
				continue
			elif "yify" in match[1]:
				yifyLinks = resolver.GetYifyLinks(match[0])
				for link in yifyLinks:
					links.append((link["url"], match[1], link["quality"]))
				continue
			links.append(match)

		if len(links) < 1:
			addDir('[COLOR red] לא נמצאו מקורות ניגון [/COLOR]','99',99,'',False, description)
			return
		if len(links) > 1:
			links = SortByQuality(links)
			playingUrlsList = []
			for link in links:
				playingUrlsList.append(link[0])
			addDir('[COLOR red] בחר בניגון אוטומטי [/COLOR]','99',99,'',False, description)
			addDir('{0} - ניגון אוטומטי'.format(name), json.dumps(playingUrlsList), 7, iconimage, False, description)
			addDir('[COLOR red]  או בחר מקור לניגון, אם לא עובד נסה אחר [/COLOR]','99',99,'',False, description)
		for link in links:
			addDir("{0} - {1} - איכות {2}".format(name, link[1], link[2]),link[0],5,iconimage,False, description)
	else:
		series_num=url.split('-')[-1]
		GetSeasons(series_num, iconimage, description)

def PlayWs(url, autoPlay=False):
	url = common.GetAdFlyLink(url)
	if baseUrl.replace('www.', '') in url:
		url = resolver.ResolveUrl(url)
	if url:
		listitem = xbmcgui.ListItem(path=url)
		xbmcplugin.setResolvedUrl(handle, True, listitem)
		return True
	else:
		if not autoPlay:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok('OOOPS', 'Try a differnt Source')	
		return False

def AutoPlayUrl(urls):
	playingUrlsList = json.loads(urls)
	for playingUrl in playingUrlsList:
		if PlayWs(playingUrl, autoPlay=True):
			return
	dialog = xbmcgui.Dialog()
	ok = dialog.ok('OOOPS', 'לא נמצאו מקורות זמינים לניגון')

def PlayTrailer(url):
	result = common.OPEN_URL(url)
	matches = re.compile('"videoUrl":"(.+?)"',re.I+re.M+re.U+re.S).findall(result)
	if len(matches) > 0:
		url = matches[0]
		PlayWs(url)

def Categories():
	addDir("Search - חיפוש"," ",6,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQlAUVuxDFwhHYzmwfhcUEBgQXkkWi5XnM4ZyKxGecol952w-Rp')
	addDir("Movies - סרטים","{0}/movies".format(baseUrl),2,'http://www.aldeahostelcostarica.com/wp-content/uploads/2015/03/aldea_movie_day-500x300.jpg')
	addDir("Series - סדרות","{0}/series".format(baseUrl),2,'http://kibenterprise.com/media/catalog/category/TV_Series.png')
	addDir("Kids - ילדים","{0}/genres/Kids".format(baseUrl),2,'http://www.in-hebrew.co.il/images/logo-s.jpg')
	addDir("Animation - אנימציה","{0}/genres/Animation".format(baseUrl),2,'http://icons.iconarchive.com/icons/designbolts/free-movie-folder/256/Animated-icon.png')
	addDir("Fantasy - פנטזיה","{0}/genres/Fantasy".format(baseUrl),2,'http://blog.tapuz.co.il/girlkido/images/3472680_852.jpg')
	addDir("Family - משפחה","{0}/genres/Family".format(baseUrl),2,'http://pschools.haifanet.org.il/dror/DocLib1/%D7%99%D7%95%D7%9D%20%D7%9E%D7%A9%D7%A4%D7%97%D7%94%20%D7%A9%D7%9E%D7%97.jpg')
	addDir("Israeli - ישראלי","{0}/genres/israeli".format(baseUrl),2,'http://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Flag_of_Israel.svg/250px-Flag_of_Israel.svg.png')
	addDir("Live Shows - הופעות חיות","{0}/genres/LiveShow".format(baseUrl),2,'http://www.netravelfly.co.il/resources/deals/images/Other/Music/Atmosphere/480X320/8.jpg')
	addDir("Comedy - קומדיה","{0}/genres/Comedy".format(baseUrl),2,'http://www.filmsite.org/images/comedy-genre.jpg')
	addDir("Drama - דרמה","{0}/genres/Drama".format(baseUrl),2,'http://comps.canstockphoto.com/can-stock-photo_csp11392197.jpg')
	addDir("Documentary - דוקומנטרי","{0}/genres/Documentary".format(baseUrl),2,'http://icons.iconarchive.com/icons/aaron-sinuhe/tv-movie-folder/512/Documentaries-National-Geographic-icon.png')
	addDir("Action - פעולה","{0}/genres/Action".format(baseUrl),2,'http://pmtips.net/wp-content/uploads/2012/02/action.jpg')
	addDir("Crime - פשע","{0}/genres/Crime".format(baseUrl),2,'http://drthurstone.com/wp-content/uploads/2014/07/Crime-Pix.jpg')
	addDir("Thriller - מתח","{0}/genres/Thriller".format(baseUrl),2,'http://becplmovies.files.wordpress.com/2011/06/thrillers_title12.jpg')
	addDir("War - מלחמה","{0}/genres/War".format(baseUrl),2,'http://cdn2.pitchfork.com/news/53502/0ff1bba7.jpg')
	addDir("Mystery - מיסתורין","{0}/genres/Mystery".format(baseUrl),2,'http://www.barronmind.com/WMHlogoweb.gif')
	addDir("Horror - אימה","{0}/genres/Horror".format(baseUrl),2,'https://cdn4.iconfinder.com/data/icons/desktop-halloween/256/Mask.png')
	addDir("Sci-Fi - מ.בדיוני","{0}/genres/Sci-Fi".format(baseUrl),2,'http://images.clipartpanda.com/sci-fi-clipart-peacealienbw.png')
	xbmc.executebuiltin('Container.SetViewMode(500)')

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

try:
	url=urllib.unquote_plus(params["url"])
except:
	url=None
try:
	name=urllib.unquote_plus(params["name"])
except:
	name=None
try:
	mode=int(params["mode"])
except:
	mode=None
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	iconimage=""
try:
	description=urllib.unquote_plus(params["description"])
except:
	description=""
	

print "checkMode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

updateView = True

if mode==None or url==None or len(url)<1:
	repoCheck.UpdateRepo()
	Categories()
elif mode==2:
	IndexPage(url)
elif mode==3:
	GetEpisodes(url, iconimage, description)
elif mode==4:
	LinksPage(url, iconimage, description)
elif mode==5:
	PlayWs(url)
elif mode==6:
	updateView = searchWs()
elif mode==7:
	AutoPlayUrl(url)
elif mode==8:
	PlayTrailer(url)
	
if updateView:
	xbmcplugin.setContent(handle, 'episodes')
	if mode==None or url==None or len(url)<1:
		xbmc.executebuiltin("Container.SetViewMode(500)")
	else:
		xbmc.executebuiltin('Container.SetViewMode(504)')
	xbmcplugin.endOfDirectory(handle)