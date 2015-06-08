# -*- coding: utf-8 -*-
import urllib,urllib2

def OPEN_URL(url, headers={}, user_data={}, referer=None, Host=None):
	link = ""
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	for k, v in headers.items():
		req.add_header(k, v)
	if referer:
		req.add_header('Referer' ,referer)
	if Host:
		req.add_header('Host' ,Host)
	try:
		response = urllib2.urlopen(req,timeout=100)
		link = response.read()
		response.close()
	except:
		return None
	return link