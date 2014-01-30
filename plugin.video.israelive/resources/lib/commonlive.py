# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os


#using xunity downloader with changes from me
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

def addDir(name,url,mode,iconimage,description):
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        if mode==3 or mode==8 or mode==6 or mode==99:
                if mode==3:
					items = []
					items.append(('TV Guide', 'XBMC.Container.Update({0}?url={1}&mode=9&iconimage={2})'.format(sys.argv[0], urllib.quote_plus(url), iconimage)))
					liz.addContextMenuItems(items = items)
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        elif  mode==7 :
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
#same as above but this is addlink this is where you pass your playable content so you dont use addDir you use addLink "url" is always the playable content         
def addLink(name,url,iconimage,description):
        print "once"
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok

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

