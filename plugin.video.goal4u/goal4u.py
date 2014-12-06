# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,os,base64,datetime,json
import xbmcaddon, xbmc, xbmcplugin, xbmcgui



def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    
    response = urllib2.urlopen(req,timeout=100)
    link=response.read()
    response.close()
    return link
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def addLink(name,url,iconimage,description):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)

def INDEXpage(url,name):
	print url
	link=OPEN_URL(url)
	match=re.compile('embed.?(.*?)\?',re.I+re.M+re.U+re.S).findall(link)
	if match:
		match=match[-1]
		print str(match) + 'blabla'
		firstlink='http://youcloud.tv/player?streamname='+str(match)
		link=OPEN_URL(firstlink)
		
		match=re.compile('var a = (.*?);.*?var b = (.*?);.*?var c = (.*?);.*?var d = (.*?);.*?var f = (.*?);.*?var v_part = \'(.*?)\';',re.I+re.M+re.U+re.S).findall(link)
		print "winners are: " + str(match)
		match=match[0]
		a=int(match[0])/int(match[4])
		b=int(match[1])/int(match[4])
		c=int(match[2])/int(match[4])
		d=int(match[3])/int(match[4])
		v_part=match[5]
		final='rtmp://'+str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)+str(v_part)+' swfUrl=http://cdn.youcloud.tv/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl=http://youcloud.tv'
		print "winners are: " + str(match)
		listItem = xbmcgui.ListItem(name, iconImage = '', thumbnailImage = '', path=final)
		listItem.setInfo(type='Video',infoLabels={ "Title":name})
		listItem.setProperty('IsPlayable', 'true')
		xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
	else:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('XBMC', 'No SIGNAL ',"אין שידור באתר")
def INDEXmain():
	addDir('ספורט 1','http://www.goalim4u.org/p/1_24.html',2,'')
	addDir('ספורט 2','http://www.goalim4u.org/p/2.html',2,'')
	addDir('ספורט 5','http://www.goalim4u.org/p/5_63.html',2,'')
	addDir('+ ספורט חמש','http://www.goalim4u.org/p/5.html',2,'')
	addDir('ספורט חמש לייב','http://www.goalim4u.org/p/5_24.html',2,'')
	addDir('ספורט חמש גולד','http://www.goalim4u.org/p/5_33.html',2,'')
	addDir('ספורט מתחלף','http://www.goalim4u.org/p/blog-page_24.html',2,'')
	addDir('ספורט מתחלף 2','http://www.goalim4u.org/p/2_1.html',2,'')

	
	
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

print "checkMode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
	INDEXmain()
elif mode==2:
	INDEXpage(url,name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))