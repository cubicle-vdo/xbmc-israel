# -*- coding: utf-8 -*-
import urllib2, re
import jsunpack

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
		sessionpage=getUrl('http://www.glarab.com/ajax.aspx?stream=live&type=reg&ppoint=KuwaitSpace', cookieJar)
		sessionpage=sessionpage.split('|')[1]
		url = "{0}?session={1}&hlsid=HLS_2487419".format(url, sessionpage)
		return url
	except:
		return ""
		
def GetYoutubeFullLink(url):
	from livestreamer import Livestreamer
	livestr = Livestreamer()
	channel = livestr.resolve_url(url)
	streams = channel.get_streams()
	stream = streams["best"]
	return stream.url
	
def GetLivestreamTvFullLink(channelName):
	text = getUrl('http://embed.live-stream.tv/{0}'.format(channelName.lower()))
	unpack = jsunpack.unpack(text)
	matches = re.compile('file:"(.*?)",streamer:"(.*?)"', re.I+re.M+re.U+re.S).findall(unpack)
	final = "{0}/{1}".format(matches[0][1], matches[0][0])
	if 'rtmp' in final:
		return final
	else:
		return 'down'
