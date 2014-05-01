import urllib2, re

UA = 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0'

def getId(channel):
	baseUrl = "http://www.teledunet.com"
	url= "{0}/tv_/?channel={1}".format(baseUrl, channel)

	cookie = OpenURL(baseUrl, justCookie=True)
	if cookie == None:
		return None
	
	headers = { 'Host': 'www.teledunet.com', 
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate',
				'Referer': 'http://www.teledunet.com/',
				'Connection': 'Keep-Alive', 
				'Cookie': cookie}
	
	data = OpenURL(url, headers)
	nameUrl = (re.compile('time_player=(.+?);').findall(data))
	nameUrl = str(nameUrl).replace("['", '').replace("']", '').replace(".","").replace("E+13","00").strip()
	return nameUrl
	
                    
def PlayTeledunet(url):
	channel = url.split('teledunet/')[1].strip()
	url = 'rtmp://www.teledunet.com:1935/teledunet/{0}'.format(channel)
	id0 = getId(channel)
	streamUrl = '{0} app=teledunet swfUrl=http://www.teledunet.com/tv/player.swf?bufferlength=5&repeat=single&autostart=true&id0={1}&streamer={0}&file={2}&provider=rtmp playpath={2} live=1 pageUrl=http://www.teledunet.com/tv/?channel={2}&no_pub'.format(url, id0, channel)
	return streamUrl
	
def OpenURL(url, headers={}, user_data={}, justCookie=False):
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	
	req.add_header('User-Agent', UA)
	for k, v in headers.items():
		req.add_header(k, v)
	
	response = urllib2.urlopen(req)
	
	if justCookie == True:
		if response.info().has_key("Set-Cookie"):
			data = response.info()['Set-Cookie']
		else:
			data = None
	else:
		data = response.read()
	
	response.close()
	return data