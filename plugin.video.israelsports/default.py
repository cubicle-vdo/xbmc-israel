# -*- coding: utf-8 -*-
import urllib, urllib2, sys, re, xbmcplugin, xbmcgui, xbmcaddon, xbmc, random

ADDON = xbmcaddon.Addon(id='plugin.video.israelsports')

def CATEGORIES():
	addDir('חדשים','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=893&page=',2,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTvo6GmRkhBMgJHX0DiWtikRpet97rNyCTsSi_OdsdF7Dp4K-96','1')
	addDir('ליגת האלופות - תקצירים','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=5813&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRf7mZyApMKwnQyHcJ5shoFE8OhLOlbmUIhytkWAP05suAGv9h8xA','1')
	addDir('ליגת האלופות - כתבות','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=5935&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRf7mZyApMKwnQyHcJ5shoFE8OhLOlbmUIhytkWAP05suAGv9h8xA','1')
	addDir('ליגת העל בכדורגל','www.stam.com',6,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRpi-QusXtg3bBYigUFBxDmVj-nbBuPqJsGhWybwI8zx1Rlh2mw','')
	addDir('ליגה איטלקית','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=5808&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ5MZPuGkXGn4XoaDo72fi0gKIOik_0GVZHgHXmkQ1avptCA4WS','1')
	addDir('ליגה אנגלית','http://svc.one.co.il/Cat/Video/?c=85&p=',4,'http://www.bettingexpert.com/deprecated/assets/images/blog/PremLeagueBettingAwards/premier-league-logo.jpg','1')
	addDir('EUROLEAGUE','http://svc.one.co.il/Cat/Video/?c=77&p=',4,'http://www.isramedia.net/images/tvshowpic/euroleague.jpg','1')
	addDir('ליגה ספרדית','http://svc.one.co.il/Cat/Video/?c=113&p=',4,'http://images.one.co.il/Images/OneTV/Categories/2015/08/16/1200/113.png','1')
	addDir('בית"ר נורדיה ירושלים','open',14,'http://www.headstart.co.il/components/img.aspx?img=images%5C2(25).jpg','1')
	addDir('NBA','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=5959&page=',2,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTMaYyCKAudTxqAh0YUsGGbL5axGDZV5YT-wL1-dYK25VfNNTzhKg','1')
	addDir('כדורסל ישראלי','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=5845&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcROtyknPHO9KMMRBxTivXvWDngNdMzr5Mf5VMyJLyPEx_WEpxtk','1')
	addDir('כדורסל   נשים ישראלי','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=4979&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcROtyknPHO9KMMRBxTivXvWDngNdMzr5Mf5VMyJLyPEx_WEpxtk','1')
	addDir('חדשות הספורט','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=3968&page=',2,'http://www.nrg.co.il/images/archive/300x225/631/730.jpg','1')
	addDir('יציע העיתונות','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=5811&page=',2,'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRVDQaVdqH65g5IqYdUf1zqt_FMHSOsbJPYzLI6tC1lxyh_FS97','1')
	addDir('בובה של לילה 4','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=7056&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRjTjLnpK8ye6aN68h5HgcPo08Xtr1KJZd9iRSRQ3GlU9zB0pPViQ','1')
	addDir('בובה של לילה 3','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=3473&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRjTjLnpK8ye6aN68h5HgcPo08Xtr1KJZd9iRSRQ3GlU9zB0pPViQ','1')
	addDir('בובה של לילה 2','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=3186&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRjTjLnpK8ye6aN68h5HgcPo08Xtr1KJZd9iRSRQ3GlU9zB0pPViQ','1')
	addDir('בובה של לילה 1','http://vod.sport5.co.il/Ajax/GetVideos.aspx?Type=B&Vc=3185&page=',2,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRjTjLnpK8ye6aN68h5HgcPo08Xtr1KJZd9iRSRQ3GlU9zB0pPViQ','1')
	xbmc.executebuiltin('Container.SetViewMode(500)')

def list_videos(url,page):
	url1=url+"1"
	url=url+str(page)
	link=OPEN_URL(url1)
	total=re.compile('total-pages="(.*?)"').findall(link)
	if total:
		total=int(total[0])
	else:
		total=1
	print  str(total)+ 'total'
   
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
	
	if  not ('delivery' in clipid[0]) :
		link=OPEN_URL(secondurl)
		highres=re.compile('http://s5-s.nsacdn.com/sport5_vod/(.*?)</FileURL>',re.M+re.I+re.S).findall(link)
		ip=re.compile('<Server priority=.*?>(.*?)<',re.M+re.I+re.S).findall(link)
		random.seed()
		ip=ip[random.randint(0, len(ip)-1)]
		direct=  "http://"+ip+"/sport5_vod/" + str (highres[-1])
	else:
		direct='http://sport5-vh.akamaihd.net/i/video/'+clipid[0]+'.csmil/master.m3u8'
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title":name} )
	liz.setPath(direct)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
			  
def ligat_al():
	link = OPEN_URL('http://svc.one.co.il/Cat/Video/Reviews.aspx?c=28')
	#<a href="/Cat/Video/Reviews.aspx?tm=1"><img style="border:0;width:46px;height:49px;" src="http://images.one.co.il/Images/Teams/Logos_46x49/1.png" alt="הפועל חיפה" /></a>"
	list1=re.compile('<a href="\/Cat\/Video\/Reviews.aspx\?tm=(.*?)".*?src="http://images.one.co.il/Images/Teams/Logos(.*?)" alt="(.*?)" /></a>').findall(link)
	for url, image, name in list1:
		name=name.decode('iso-8859-8').encode('utf-8')
		name=unescape(name)
		url='http://svc.one.co.il/cat/Video/Reviews.aspx?tm='+url
		image='http://images.one.co.il/Images/Teams/Logos'+image
		addDir(name,url,4,image,'al')
	setView('movies', 'default')

def one_videopage(url,description):
	if description!='al' :
		murl=url+str(description)
	else:
		murl=url
					
	link = OPEN_URL(murl)
	list1=re.compile('"Title": "(.*?)".*?"Image": "(.*?)".*?"URLStreamHD" : "(.*?)".*?}').findall(link)
	page_total=re.compile('var page = (.*?);.*?var pages = (.*?);').findall(link)[0]
	current= page_total[0]
	total= page_total[1]
	current=int(current)
	total =int (total)
	for name,image,hq in list1:
		image="http://images.one.co.il/images/video/segment377x285/"+image
		name=unescape(name)
		name=name.decode('windows-1255').encode('utf-8')
		addDir(name,hq,5,image,'')
	if current < total :
		current+=1
		addDir("[COLOR yellow]לעמוד הבא[/COLOR]",url,4,'',str(current))
	addDir("[COLOR blue]חזרה לראשי [/COLOR]",'',None,'','')

	setView('movies', 'default')

def YoutubeUser(username):
	xbmc.executebuiltin('XBMC.Container.Update(plugin://plugin.video.youtube/channel/{0}/)'.format(username))
	
def play_one(name,url,iconimage):
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title":name} )
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
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

def addDir(name,url,mode,iconimage,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	if mode==15 or mode==16 or mode==3 or mode==5:
		liz.setProperty("IsPlayable","true")
	if mode==15 or mode==16 or mode==9 or mode==3 or mode==5 or mode==1:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
	CATEGORIES()
elif mode==2:
	list_videos(url,description)
elif mode==3:
	play_video(url,name,iconimage)
elif mode==4:
	one_videopage(url,description)
elif mode==5:
	play_one(name,url,iconimage)
elif mode==6:
	ligat_al()
elif mode==8:
	LIVE()
elif mode==9:
	YoutubeUser('UChv13q9FGA-siy4T4PcCx4Q')
elif mode==14:
	addDir('?מה זה בית"ר נורדיה ירושלים','blah',16,'','')
	addDir('סרטוני בית"ר נורדיה ירושלים','eli',9,'','')
elif mode==15:
	PlayAwe()
elif mode==16:
	xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=L2928xxYc7c)')
xbmcplugin.endOfDirectory(int(sys.argv[1]))
