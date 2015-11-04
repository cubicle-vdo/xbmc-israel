# -*- coding: utf-8 -*-
import urllib, urllib2, gzip, base64, os, time
from StringIO import StringIO

AddonName = "Movix.me"
UA = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"

def OPEN_URL(url, headers={}, user_data={}, referer=None, Host=None):
	link = ""
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	req.add_header('User-Agent', UA)
	req.add_header('Accept-encoding', 'gzip')
	for k, v in headers.items():
		req.add_header(k, v)
	if referer:
		req.add_header('Referer' ,referer)
	if Host:
		req.add_header('Host' ,Host)
	try:
		response = urllib2.urlopen(req,timeout=100)
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO( response.read())
			f = gzip.GzipFile(fileobj=buf)
			link = f.read()
		else:
			link = response.read()
		response.close()
	except:
		return None
	return link

def Decode(string):
	key = AddonName
	decoded_chars = []
	string = base64.urlsafe_b64decode(string.encode("utf-8"))
	for i in xrange(len(string)):
		key_c = key[i % len(key)]
		decoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
		decoded_chars.append(decoded_c)
	decoded_string = "".join(decoded_chars)
	return decoded_string
	
def GetUA():
	return UA

def isFileOld(file, deltaInSec):
	lastUpdate = 0 if not os.path.isfile(file) else int(os.path.getmtime(file))
	now = int(time.time())
	isOld = True if (now - lastUpdate) > deltaInSec else False 
	return isOld
