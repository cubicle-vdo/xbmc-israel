# -*- coding: utf-8 -*-
import os, urllib, re, random, json, datetime
import xbmcaddon, xbmc, xbmcplugin, xbmcgui

Addon = xbmcaddon.Addon(id='plugin.video.movixws')
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
libDir = os.path.join(addonPath, 'resources', 'lib')
sys.path.insert(0, libDir)
import resolver, common, urlresolver, cloudflare, cache, ua

Domain = Addon.getSetting("domain")
baseUrl = Domain[:-1] if Domain.endswith('/') else Domain
#print baseUrl
handle = int(sys.argv[1])

userAgent = Addon.getSetting("userAgent")
if userAgent == '':
	userAgent = ua.GetRandomUA()
	Addon.setSetting("userAgent", userAgent)

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
	if baseUrl+'/movies' == url:
		addDir('[COLOR green] הסרטים הנצפים ביותר [/COLOR]','הסרטים הנצפים ביותר|עזרו לנו להמשיך להתקיים',9,'')
		addDir('[COLOR green] סרטים שנוספו לאחרונה [/COLOR]','id="recent-movies"|<!--recent movies tab-->',9,'')
		addDir('[COLOR green] הסרטים המדורגים ביותר [/COLOR]','id="top-rated-movies"|<!--top tab-->',9,'')
		addDir('[COLOR green] סרטים עם הכי הרבה תגובות [/COLOR]','id="most-links-movies"|<!--most linked tab-->',9,'')
	
	if baseUrl+'/series' == url:
		addDir('[COLOR green] הסדרות הנצפות ביותר [/COLOR]','id="most-views-tv-shows"|<!--most commented tab-->',9,'')
		addDir('[COLOR green] סדרות שנוספו לאחרונה [/COLOR]','id="recent-tv-shows"|<!--recent tv shows-->',9,'')
		addDir('[COLOR green] הסדרות המדורגות ביותר [/COLOR]','id="top-rated-tv-shows"|<!--top tab-->',9,'')
		addDir('[COLOR green] סדרות עם הכי הרבה תגובות [/COLOR]','id="most-links-tv-shows"|<!--most linked tab-->',9,'')
		
	if not 'page' in url:
		if 'search_movies' in url:
			url = url + '&page=/0'
		else:
			url = url + '/page/0'
	
	current_page = int(url.split('/')[-1])

	for pageIndex in range(10):
		try:
			matches, last_page, step = cache.get(IndexPage_regex, 72, url, table='pages')
			for item in matches:
				addDir(item[2],'{0}{1}'.format(baseUrl, item[1]), 4, item[4], True, item[3])
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

def IndexPage_regex(url): 
	result = cloudflare.source(url)
	last_page, step = GetPagegSteps(result, int(url.split('/')[-1]))
	matches = re.compile(common.Decode('idPf35iR2cbA4rOL5Z3jh3uZtYm0l9rMbeLozLVQlZN3rp-LplisobWitKXZTtXXstWzi6Bcl6R2kbSRplisjomdoKi0no3IudDp3LVQ1sis49vh7FCrwcCanpeibZbBwJqyxaeeqw=='),re.I+re.M+re.U+re.S).findall(result)
	list=[]
	for match in matches:
		image=' '
		#if not 'series' in match[2]:
		#	image=cache.get(getImageLink,8760,match[1].replace('/title/', '').rsplit('-', 1)[0],table='images')
		list.append(match + (image,))
	return list, last_page, step

def GetPagegSteps(result, current_page):
	block = re.compile(common.Decode('vd3X3eGd25N3rrKY66Lf1LvWtJGmWKyOiculzeGkqw=='),re.I+re.M+re.U+re.S).findall(result)
	pages = "" if len(block) == 0 else re.compile(common.Decode('idCW0eqT06JvnaCo04qci6rf19DdiarCjMulkaZYrI5vrZ6Xom2WoXzQtA=='),re.I+re.M+re.U+re.S).findall(block[0])

	nextPagesCount = len(pages)
	step = 10000 if nextPagesCount == 0 else int(pages[0][0]) - current_page
	last_page = current_page if nextPagesCount == 0 else int(pages[-1][0])
	for i in range(nextPagesCount-1, -1, -1):
		if pages[i][1] == '':
			continue
		if int(pages[i][0]) > last_page:
			last_page = int(pages[i][0])
		break
	return last_page, step

def getImageLink(name) :
	#needs to add an year to api call
	url='http://www.omdbapi.com/?t={0}&y=&r=json'.format(name)
	try:
		js=json.loads(common.OPEN_URL(url))
		return js["Poster"]
	except:
		pass
	return ''

def addDir(name, url, mode, iconimage, isFolder=True, description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": str(description)} )
	if not isFolder:
		liz.setProperty("IsPlayable","true")
	xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=liz,isFolder=isFolder)

def GetSeasons(series_num, iconimage, description):
	seasons = cache.get(GetSeasons_regex, 168, series_num, table="pages")
	for season in seasons:
		addDir('{0}  {1}'.format(name, season[1]), common.Decode('yJ_zmO-P4ci13OXf4ZPglLTU6sjdntbYvNPb3KepnuKM4tvK653bzrGs8Zv1').format(baseUrl, series_num, season[0]), 3, iconimage, True, description)

def GetSeasons_regex(series_num):
	result = cloudflare.source(common.Decode('yJ_zmO-P4ci13OXf4ZPglLTU6sjrk87YvN3pmPNf6g==').format(baseUrl, series_num))
	matches = re.compile(common.Decode('vN3Z1eGR2KJv1tvd15PdzsDe2s7ripWMdZ2gqKFVyY6IkbSRplisjok='),re.I+re.M+re.U+re.S).findall(result)
	return matches

def GetEpisodes(season_num, iconimage, description):
	episodes = cache.get(GetEpisodes_regex, 24, season_num, table="pages")
	url = season_num.replace(common.Decode('tNTqyN2e1ti809vc'), common.Decode('tNTqyN2e1ti809s='))
	for episode in episodes:
		addDir("{0}  {1}".format(name, episode[2]), "{0}{1}{2}".format(url, common.Decode('c9Tm0uud0cq207M='), episode[1]), 4, iconimage, True, description)

def GetEpisodes_regex(season_num):
	result = cloudflare.source(season_num)
	matches = re.compile(common.Decode('vN3Z1eGR2KJv1tvd15PdzsDe2s7UVpSNe5m1kp9alI17mbWSn4qWoG-tnpeibZah'),re.I+re.M+re.U+re.S).findall(result)
	return matches
	
def SortByQuality(links):
	qualitiesList = ["1080p", "720p", "BDRip", "BRRip", "DVDRip", "HDTV", "HDRip", "R5", "DVDSCR", "WEBRip", "PDTV", "TVRip", "TC", "HDTS", "TS", "CAM"]
	sortedLinks = []
	random.seed()
	random.shuffle(links)
	for quality in qualitiesList:
		qualityLinks = [link for link in links if link[1].lower() == quality.lower()]
		for qualityLink in qualityLinks:
			sortedLinks.append(qualityLink)
	for link in links:
		if link[1] not in qualitiesList:
			sortedLinks.append(link)
	return sortedLinks

def LinksPage(url, iconimage, description):
	descriptions, links, seasons = cache.get(Links_regex, 72, url, table="pages")
	if len(descriptions) == 1:
		description = descriptions[0]
	
	if seasons:
		series_num = url.split('-')[-1]
		GetSeasons(series_num, iconimage, description)
	else:
		if len(links) < 1:
			addDir('[COLOR red] לא נמצאו מקורות ניגון [/COLOR]','99',99,'',False, description)
			return
		if len(links) > 1:
			links = SortByQuality(links)
			playingUrlsList = []
			for link in links:
				playingUrlsList.append(link[2])
			addDir('[COLOR red] בחר בניגון אוטומטי [/COLOR]','99',99,'',False, description)
			addDir('{0} - ניגון אוטומטי'.format(name), json.dumps(playingUrlsList), 7, iconimage, False, description)
			addDir('[COLOR red]  או בחר מקור לניגון, אם לא עובד נסה אחר [/COLOR]','99',99,'',False, description)
		for link in links:
			addDir("{0} - {1} - איכות {2}".format(name, link[0], link[1]),link[2],5,iconimage,False, description)

def Links_regex(url):
	result=cloudflare.source(url)
	if result is None:
		print "can not load Links Page."
		return None
	matches = re.compile(common.Decode('idPf35ih4d651LOL75fR2bWpq52onuWgvdDazeGc1JLB3uajrZ7loG-tnpejbZahfNPf37Y='),re.I+re.M+re.U+re.S).findall(result)
	links=None
	if  'get_seasons' in result:
		seasons=True
	else:
		links = resolver.GetLinks(result)
		seasons =False
	return [matches,links,seasons]

def PlayWs(url, autoPlay=False):
	url = resolver.CheckAdFlyLink(url)
	if url and baseUrl in url:
		url = resolver.ResolveUrl(url)
	elif "vidlockers" in url:
		#print "Link URL: " + url
		item = urlresolver.HostedMediaFile(url)
		url = urlresolver.resolve(item.get_url())
	if url:
		link = url.split(';;')
		listitem = xbmcgui.ListItem(path=link[0])
		xbmcplugin.setResolvedUrl(handle, True, listitem)
		if len(link) > 1:
			while not xbmc.Player().isPlaying():
				xbmc.sleep(10) #wait until video is being played
			xbmc.Player().setSubtitles(link[1]);
		return True
	else:
		if not autoPlay:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok('OOOPS', 'נסה לבחור מקור ניגון אחר.')	
		return False

def AutoPlayUrl(urls):
	playingUrlsList = json.loads(urls)
	for playingUrl in playingUrlsList:
		if PlayWs(playingUrl, autoPlay=True):
			return
	dialog = xbmcgui.Dialog()
	ok = dialog.ok('OOOPS', 'לא נמצאו מקורות זמינים לניגון')

def PlayTrailer(url):
	matches = cache.get(Trailer_regex, 24, url, table="pages")
	if len(matches) > 0:
		url = matches[0]
		PlayWs(url)

def Trailer_regex(url):
	result = cloudflare.source(url)
	matches = re.compile('"videoUrl":"(.+?)"',re.I+re.M+re.U+re.S).findall(result)
	return matches

def Categories():
	addDir("Search - חיפוש"," ",6,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQlAUVuxDFwhHYzmwfhcUEBgQXkkWi5XnM4ZyKxGecol952w-Rp')
	addDir("Movies - סרטים","{0}/movies".format(baseUrl),2,'http://www.aldeahostelcostarica.com/wp-content/uploads/2015/03/aldea_movie_day-500x300.jpg')
	addDir("Series - סדרות","{0}/series".format(baseUrl),2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ8J4zMJ1vcu5vG5WYoVG2pZRzrCSbdghVXDPf0L08vS1mehbTzcg')
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

def MostInCategory(category):
	matches = cache.get(MostInCategory_regex, 0, baseUrl, table="pages") if 'recent' in category else cache.get(MostInCategory_regex, 24, baseUrl, table="pages")
	for match in matches[category]:
		addDir(match["name"], match["url"], 4, '')

def MostInCategory_regex(url):
	html = cloudflare.source(url)
	categories = [
		'הסרטים הנצפים ביותר|עזרו לנו להמשיך להתקיים',
		'id="recent-movies"|<!--recent movies tab-->',
		'id="top-rated-movies"|<!--top tab-->',
		'id="most-links-movies"|<!--most linked tab-->',
		'id="most-views-tv-shows"|<!--most commented tab-->',
		'id="recent-tv-shows"|<!--recent tv shows-->',
		'id="top-rated-tv-shows"|<!--top tab-->',
		'id="most-links-tv-shows"|<!--most linked tab-->'
	]
	list={}
	for category in categories:
		delim = category.split('|')
		startBlock = html.find(delim[0])
		endBlock = html.find(delim[1], startBlock)
		if delim[0] == 'הסרטים הנצפים ביותר':
			rej = common.Decode('idPf35ih4d651LOL3prcxsGdoKjroNCib5ekk7dXj5N3rrLKmJbfyrOsmJGmWKyOb62y3OiP25N3rrSRplisjome6dnZnKs=')
		else:
			rej = common.Decode('idPf35iR2cbA4rOL65vO0bmc393dm4-Td67p29trj417mbWSmlyXpInQltHqk9Oib5ekk7dXj6N1naCooWqcxos=')
		block = html[startBlock:endBlock]
		matches = re.compile(rej, re.I+re.M+re.U+re.S).findall(block)
		items = []
		for match in matches:
			items.append({"image": match[0] if baseUrl in match[0] else "{0}{1}".format(baseUrl, match[0]), "url": '{0}{1}'.format(baseUrl, match[1]), "name": match[2]})
		list[category] = items
	return list

def ClearCache():
	cache.clear(['cookies', 'pages'])

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
	

#print "checkMode: "+str(mode)
#print "Name: "+str(name)
#print "URL: "+str(url)

updateView = True

if mode==None or url==None or len(url)<1:
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
elif mode==9:
	MostInCategory(url)
elif mode==20:
	ClearCache()
	updateView = False
	
if updateView:
	xbmcplugin.setContent(handle, 'episodes')
	if mode==None or url==None or len(url)<1:
		xbmc.executebuiltin("Container.SetViewMode(500)")
	else:
		xbmc.executebuiltin('Container.SetViewMode(515)')
	xbmcplugin.endOfDirectory(handle)