# -*- coding: utf-8 -*-

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,xbmcaddon

##General vars
__plugin__ = "23TV"
__author__ = "Shmulik \ O2RI"
__credits__ = ""
__version__ = "1.0.1"
__XBMC_Revision__ = ""

__addon__      = xbmcaddon.Addon()
__cwd__        = xbmc.translatePath( __addon__.getAddonInfo('path') ).decode("utf-8")
__usecache__ = __addon__.getSetting("usecache")

def getFromCache(url,type):
  if __usecache__!="true":
    return False;
  url = url.replace('.', ''). replace('/','').replace(':','').replace('?','').replace('-','')
  filePath = os.path.join( __cwd__, 'cache',type,url)
  if (os.path.exists(filePath)):
    return  file(filePath,'r').read()
  return False;

def saveToCache(pre,final,type):
  if __usecache__!="true":
    return False;
  pre = pre.replace('.', ''). replace('/','').replace(':','').replace('?','').replace('-','')
  filePath = os.path.join( __cwd__, 'cache',type,pre)
  fileCache = file(filePath,'w')
  fileCache.write(final)
  fileCache.close()
  return True;
    


def CATEGORIES():

  addDir("23ציק","http://www.23tv.co.il/1283-he/Tachi.aspx",2,"","")
  addDir("תוכניות משודרות","http://www.23tv.co.il/39-he/Tachi.aspx",2,"","") 
  addDir("יהדות ומחשבת ישראל","http://www.23tv.co.il/2571-he/Tachi.aspx",2,"","")
  addDir("תכניות העבר","http://23tv.co.il/51-he/Tachi.aspx",2,"","")
  
  xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

def getMatches(url,pattern):
  req = urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response = urllib2.urlopen(req)
  data=response.read()
  response.close()
  matches=re.compile(pattern,re.M+re.I+re.S).findall(data)
  return matches


def programs(url,name):
  md=5
  if name=="23ציק" :
	md=4
  matches = getMatches(url,';"><a href="(.*?)" id=.*?">(.*?)</a><')
  for url,name in matches:
      if name !='אולפן הבית'  and name.find('חידון')==-1:
          addDir(name,url,md,"","")
  xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
  
def episodes(url):
  matches=getMatches(url,'"top">(.*?)</div>.*?<img src="(.*?)&th=1')
  for name,url in matches:

	newurl=urllib.unquote_plus(url+"&ak=null&cuud=&curettype=1&cucontentlinktype=1")
	newurl=newurl.replace("gmpl.aspx","gm.asp")
	addLink(name,newurl,"")
	
def episodesType1(url):
  matches=getMatches(url,'<div><img src="(.*?)&th=1".*?title="(.*?)"')
  for url,name in matches:
        newurl=urllib.unquote_plus(url+"&ak=null&cuud=&curettype=1&cucontentlinktype=1")
	newurl=newurl.replace("gmpl.aspx","gm.asp")
	print ("newurl" +newurl)
	addLink(name,newurl,"")

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

def getMmsAddress(url):
	link=url
	req = urllib2.Request(link)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', 'http://www.23tv.co.il/1283-he/Tachi.aspx')

	response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	saveToCache(url,data,'mms')
	return data



def addLink(name,url,plot):
        ok=True
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=3&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png")
        liz.setInfo( type="Video", infoLabels={ "Title": str (name),"Plot":plot } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,genre):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Genre":genre} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        INDEX(url)
        
elif mode==2:
        programs(url,name)
elif mode==3:
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage='')
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        xbmc.Player().play(getMmsAddress(url),liz)
elif mode==4:
		episodes(url)
elif mode==5:
		episodesType1(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))

