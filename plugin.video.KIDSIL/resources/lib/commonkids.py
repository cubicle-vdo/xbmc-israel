# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
AddonID = 'plugin.video.KIDSIL' 
ADDON = xbmcaddon.Addon(id=AddonID)

def downloader_israel(url, name, showProgress=True):
	import downloader, extract

	addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
	packageFile = os.path.join(addonsDir, 'packages', 'isr.zip')

	if showProgress:
		dp = xbmcgui.DialogProgress()
		dp.create(AddonName, "Downloading", name, "Please Wait")
		downloader.download(url, packageFile, dp)
		dp.update(0, "", "Extracting Zip Please Wait")
		extract.all(packageFile, addonsDir, dp)
	else:
		urllib.urlretrieve(url, packageFile)
		extract.all(packageFile, addonsDir)
		
	try:
		os.remove(packageFile)
	except:
		pass
			
	xbmc.executebuiltin("UpdateLocalAddons")
	xbmc.executebuiltin("UpdateAddonRepos")

#using xunity downloader with changes 
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

def update_view(url):

    ok=True        
    xbmc.executebuiltin('XBMC.Container.Update(%s)' % url )
    return ok




def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
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


def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        menu = []
        
        #ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        if mode==12:
                #url=urllib.unquote(url)
                menu.append(('[COLOR blue]        הצג פרטי רשימת השמעה [/COLOR]', "XBMC.Container.Update(plugin://plugin.video.KIDSIL/?description&iconimage=''&mode=13&name=''&url=%s)"% (url)))
                liz.addContextMenuItems(items=menu, replaceItems=True)
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
                return ok
        if mode==9:
                menu.append(('[COLOR blue]       TV MODE [/COLOR]', "XBMC.RunPlugin(plugin://plugin.video.KIDSIL/?description&iconimage=''&mode=115&name=''&url=%s)"% (url)))
                liz.addContextMenuItems(items=menu, replaceItems=True)
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
                return ok
        elif  mode==8 :
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
                return ok
        elif mode==11 or mode==15 or mode==115 :
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
                return ok
        elif mode==13:
             menu.append(('[COLOR blue]        נגן ברצף [/COLOR]', "XBMC.RunPlugin(plugin://plugin.video.KIDSIL/?description&iconimage=''&mode=12&name=''&url=%s)"% (url)))
             liz.addContextMenuItems(items=menu, replaceItems=True)
             ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
             return ok
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


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
                
                
                
def CleanTheCache():
    dir=xbmc.translatePath('special://temp/')
    file=os.path.join(dir, 'commoncache.db')
    f = open(file, 'w')
    f.write('')
    f.close
    
    dlg = xbmcgui . Dialog ( )
    dlg.ok("KIDS IL BY O2ri"," cache deleted ! " ,"dora was saved again")
    
                      
def mes():

        
	try:
		link=OPEN_URL('http://goo.gl/r6eog7')
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
