# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys
import xbmcplugin, xbmcgui
import repoCheck

def INDEXsdarot(url):
	repoCheck.UpdateRepo()
	req = urllib2.Request(url)
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<a class="aodInnerTitle".*?<b>(.*?)</b>(.*?)<tr style="margin-top:15px">',re.I+re.M+re.U+re.S).findall(link)
	for result in  match:
		addDir(result[0].decode('windows-1255').encode("utf-8"), result[1], 1, '')
	xbmcplugin.addSortMethod(int(sys.argv[1]), 1)

def INDEXepisode(url,name):  
	match=re.compile('title="(.*?)">.*?"schedule_code" style="display:none">(.*?)<',re.I+re.M+re.U+re.S).findall(url)
	for  name2,num in match:
		link = 'http://switch31-01.castup.net/cunet/gm.asp?ai=31&ar='+num+'&ak=null'
		addLink(name2.decode('windows-1255').encode("utf-8"), link, '', '')

def addLink(name,url,iconimage,description):
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
	liz.setProperty("IsPlayable","true")
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)

def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	
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

#print "checkMode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
	INDEXsdarot('http://www.iba.org.il/nagish/accessibility.aspx?siteCode=1')

elif mode==1:
	INDEXepisode(url, name)

xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
