# -*- coding: utf-8 -*-
import urllib2

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):


	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	if headers:
		for h,hv in headers:
			req.add_header(h,hv)

	response = opener.open(req,post,timeout=timeout)
	link=response.read()
	response.close()
	return link
	
def GetGLArabFullLink(link):
	try:
		import cookielib
		cookieJar = cookielib.LWPCookieJar()
		sessionpage=getUrl('http://www.glarab.com/ajax.aspx?stream=live&type=reg&ppoint=KuwaitSpace',cookieJar)
		sessionpage=sessionpage.split('|')[1]
		link += "?session={0}&hlsid=HLS_2487419".format(sessionpage)
		return link
	except:
		return ""