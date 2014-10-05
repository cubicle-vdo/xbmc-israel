# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmc,os,time

#using xunity downloader with changes from me
def downloader_is(url,name):
	import downloader,extract
	
	choice = True
	dialog = xbmcgui.Dialog()
	if name.find('repo') < 0:
		choice = dialog.yesno( "XBMC ISRAEL" , "לחץ כן להתקנת תוסף חסר", name)
	 
	if choice == False:
		return
		
	addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
	dp = xbmcgui.DialogProgress()
	dp.create("XBMC ISRAEL", "Downloading", "", "Please Wait")
	packageFile = os.path.join(addonsDir, 'packages', 'isr.zip')
	try:
		os.remove(packageFile)
	except:
		pass
	downloader.download(url, packageFile, dp)
	dp.update(0, "", "Extracting Zip Please Wait")
	extract.all(packageFile, addonsDir, dp)
	#dp.update(0, "", "Downloading")
	#dp.update(0, "", "Extracting Zip Please Wait")
	xbmc.executebuiltin("UpdateLocalAddons")
	xbmc.executebuiltin("UpdateAddonRepos")

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

def addDir(name, url, mode, iconimage, description, isFolder=True, channelName=None, background=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	
	if mode==3 or mode==6 or mode==7 or mode==8 or mode==11 or mode==12 or mode==16 or mode==17 or mode==99 or mode == 13:
		isFolder=False
	
	if mode==3 or mode==11 or mode==12 or mode==16 or mode==17 or mode == 13:
		liz.setProperty("IsPlayable","true")
		items = []

		if mode == 3:
			items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=9&iconimage={2})'.format(sys.argv[0], urllib.quote_plus(url), iconimage)))
			items.append(('Add to israelive-favorites', 'XBMC.RunPlugin({0}?url={1}&mode=10&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage,channelName)))
		elif mode == 11 or mode == 12:
			items.append(('Add to israelive-favorites', 'XBMC.RunPlugin({0}?url={1}&mode=10&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage,name)))
		elif mode == 16 or mode == 13:
			items.append(('Remove from israelive-favorites', 'XBMC.RunPlugin({0}?url={1}&mode=18&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage,name)))
		elif mode == 17:
			items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=9&iconimage={2})'.format(sys.argv[0], urllib.quote_plus(url), iconimage)))
			items.append(('Remove from israelive-favorites', "XBMC.RunPlugin({0}?url={1}&mode=18&iconimage={2}&name={3})".format(sys.argv[0], urllib.quote_plus(url), iconimage,name)))

		liz.addContextMenuItems(items = items)
	
	if background is not None:
		liz.setProperty("Fanart_Image", background)

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	return ok

'''	
#same as above but this is addlink this is where you pass your playable content so you dont use addDir you use addLink "url" is always the playable content		 
def addLink(name,url,iconimage,description):
		#print "once"
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
		return ok
'''

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

'''
def Announcements():
		#Announcement Notifier from xml file
		
		try:
			  link=OPEN_URL('https://dl.dropboxusercontent.com/u/94071174/Online/wow/SUB/israelive.xml')
			  # link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

		except:
				link='nill'
		#print link
		r = re.findall(r'ANNOUNCEMENTWINDOW ="ON"',link)
		if r:

				match=re.compile('<new>(.*?)\\n</new>',re.I+re.M+re.U+re.S).findall(link)
				#print " this is a test " + str (match[0])
				if match[0]:
						TextBoxes("[B][COLOR blue]  ISRAEL LIVE[/B][/COLOR]",match[0]) 
'''

def isFileOld(file, deltaInSec):
	lastUpdate = 0 if not os.path.isfile(file) else int(os.path.getmtime(file))
	now = int(time.time())
	isM3uFileNotUpdate = True if (now - lastUpdate) > deltaInSec else False 
	return isM3uFileNotUpdate
	
def UpdateFile(file, url):
	lastModifiedFile = "{0}LastModified.txt".format(file[:file.rfind('.')])
	if not os.path.isfile(file) or not os.path.isfile(lastModifiedFile):
		fileContent = ""
	else:
		f = open(lastModifiedFile,'r')
		fileContent = f.read()
		f.close()
	
	req = urllib2.Request(url)
	try:
		response = urllib2.urlopen(req)
	except:
		return False
		
	headers = response.info()
	etag = headers.getheader("ETag")
	last_modified = headers.getheader("Last-Modified")
	if not last_modified:
		last_modified = etag
	isNew = fileContent != last_modified
	
	if isNew:
		try:
			data = response.read().replace('\r','')
		except:
			return False
			
		f = open(file, 'w')
		f.write(data)
		f.close()
		
		f = open(lastModifiedFile, 'w')
		f.write(last_modified)
		f.close()
		
	response.close()
	return isNew