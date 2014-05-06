import urllib, urllib2, os, xbmc;

AddonID = 'plugin.video.israelive'

def OpenURL(url, headers={}, user_data={}, justCookie=False):
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
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

def UpdateLists():
	isRanUpdate = False
	
	listsDir = os.path.join(xbmc.translatePath("special://userdata/addon_data"), AddonID, 'lists')
	if not os.path.exists(listsDir):
		os.makedirs(listsDir)
	listsFile = os.path.join(listsDir, "lists.list")
	if os.path.isfile(listsFile):
		f = open(listsFile,'r')
		fileContent = f.read()
		f.close()
	else:
		fileContent = ""
	
	urlContent = OpenURL("http://thewiz.info/XBMC/_STATIC/lists.list").replace('\r','')
	
	if fileContent != urlContent:
		f = open(listsFile, 'w')
		f.write(urlContent)
		f.close()
		isRanUpdate = True
	
	return isRanUpdate