# -*- coding: utf-8 -*-
import urllib, urllib2, re, base64

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
	
def GetAdFlyLink(url):
	retUrl = None
	try:
		html = OPEN_URL(url)
		ysmm = re.findall(r"var ysmm =.*\;?", html)

		if len(ysmm) > 0:
			ysmm = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])

			left = ''
			right = ''

			for c in [ysmm[i:i+2] for i in range(0, len(ysmm), 2)]:
				left += c[0]
				right = c[1] + right

			retUrl = base64.b64decode(left.encode() + right.encode())[2:].decode()

			if re.search(r'go\.php\?u\=', retUrl):
				retUrl = base64.b64decode(re.sub(r'(.*?)u=', '', retUrl)).decode()

	except Exception as e:
		print str(e)
		
	return retUrl