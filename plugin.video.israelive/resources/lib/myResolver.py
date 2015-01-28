# -*- coding: utf-8 -*-
import urllib2, re
import jsunpack, common

def getUrl(url, cookieJar=None, post=None, timeout=20, headers=None):
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	req = urllib2.Request(url)
	#req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	if headers:
		for h, hv in headers:
			req.add_header(h,hv)

	response = opener.open(req, post, timeout=timeout)
	link=response.read()
	response.close()
	return link
	
def GetGLArabFullLink(url):
	try:
		import cookielib
		cookieJar = cookielib.LWPCookieJar()
		sessionpage=getUrl('{0}ajax.aspx?stream=live&type=reg&ppoint=KuwaitSpace'.format(common.Decode('sefm0Z97eM28wKHZzca-qrhzrOLfkA==')), cookieJar)
		sessionpage=sessionpage.split('|')[1]
		url = "{0}?session={1}&hlsid=HLS_2487419".format(url, sessionpage)
		return url
	except:
		return ""
		
def GetYoutubeFullLink(url):
	#from livestreamer import Livestreamer
	#livestr = Livestreamer()
	#channel = livestr.resolve_url(url)
	#streams = channel.get_streams()
	import livestreamer
	streams = livestreamer.streams(url)
	stream = streams["best"]
	return stream.url
	
def GetLivestreamTvFullLink(channelName):
	text = getUrl('{0}{1}'.format(common.Decode('sefm0Z97eLuyq9jWj9G1v7tyvOfkxsa5d8q7eA=='), channelName.lower()))
	unpack = jsunpack.unpack(text)
	matches = re.compile('file:"(.*?)",streamer:"(.*?)"', re.I+re.M+re.U+re.S).findall(unpack)
	final = "{0}/{1}".format(matches[0][1], matches[0][0])
	if 'rtmp' in final:
		return final
	else:
		return 'down'
		
def GetSatElitKeyOnly():
	p = getUrl('{0}myPlaylistS.php'.format(common.Decode('sefm0Z97eL-1vemg1MbAdruxsuegz8rAeA==')))
	key = re.compile('iptv\/(.*?)\/',re.I+re.M+re.U+re.S).findall(p)
	return key[0]
	
def GetSatElitFullLink(channelNum, key=None):
	if key is None:
		key = GetSatElitKeyOnly()
	return "{0}iptv/{1}/{2}/index.m3u8".format(common.Decode('sefm0Z97eL-1vemg1MbAdruxsuegz8rAeA=='), key, channelNum)
	
def GetGinkoFullLink(id):
	parts = id.split(';;')
	if len(parts) < 1:
		return "down"

	p = getUrl('{0}watch.php?id={1}'.format(common.Decode('sefm0Z97eM28wKHZytO1tMVzrOLfkA=='), parts[0]))
	url = re.compile('file: "(.*?)"',re.I+re.M+re.U+re.S).findall(p)
	finalUrl = url[0]
	if len(parts) > 1:
		finalUrl = "{0}{1}/{1}.stream/playlist.m3u8{2}".format(common.Decode('sefm0Z97eMSutt_b18p9d72ut9zd0JOvuMN0'), parts[1], url[0][url[0].find('?'):])
	return finalUrl  
	
def GetAatwFullLink(channel):
	p = getUrl('{0}?account=AATW&file={1}&type=live&service=wowza&output=smil'.format(common.Decode('sefm0Z97eMi3u6Hl25PEtbmpt6HV0NJ7'), channel))
	matches = re.compile(' base="(.*?)".*?src="(.*?)"',re.I+re.M+re.U+re.S).findall(p)
	finalUrl = "{0} playpath={1}".format(matches[0][0], matches[0][1])
	return finalUrl

def GetStreamliveToFullLink(url):
	import livestreamer
	streams = livestreamer.streams(url)
	stream = streams["best"]
	return "{0} pageUrl={1} live=true".format(stream.params["rtmp"], stream.params["pageUrl"])
