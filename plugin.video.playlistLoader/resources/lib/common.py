import urllib, urllib2, os, io, xbmc, xbmcaddon, xbmcgui, json, re, chardet, shutil, time, hashlib

AddonID = 'plugin.video.playlistLoader'
Addon = xbmcaddon.Addon(AddonID)
icon = Addon.getAddonInfo('icon')
AddonName = Addon.getAddonInfo("name")
addon_data_dir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
cacheDir = os.path.join(addon_data_dir, "cache")
UA = 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0'

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
		return result

	def http_error_302(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
		return result

def getFinalUrl(url):
	link = url
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', UA)
		opener = urllib2.build_opener(SmartRedirectHandler())
		f = opener.open(req)
		link = f.url
		if link is None or link == '':
			link = url
	except Exception as ex:
		xbmc.log(str(ex), 3)
	return link
		
def OpenURL(url, headers={}, user_data={}, cookieJar=None, justCookie=False):
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	
	for k, v in headers.items():
		req.add_header(k, v)
	if not req.headers.has_key('User-Agent') or req.headers['User-Agent'] == '':
		req.add_header('User-Agent', UA)
			
	response = opener.open(req)
	#response = urllib2.urlopen(req)
	
	if justCookie == True:
		if response.info().has_key("Set-Cookie"):
			data = response.info()['Set-Cookie']
		else:
			data = None
	else:
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO( response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		else:
			data = response.read().replace("\r", "")
	
	response.close()
	return data

def ReadFile(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = handle.read().replace("\n\n", "\n")
	except:
		content = ""
	return content

def SaveFile(fileName, text):
	try:
		with open(fileName, 'w') as handle:
			content = handle.write(text)
	except:
		return False
	return True
	
def ReadList(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		xbmc.log(str(ex), 5)
		if os.path.isfile(fileName):
			shutil.copyfile(fileName, "{0}_bak.txt".format(fileName[:fileName.rfind('.')]))
			xbmc.executebuiltin('Notification({0}, Cannot read file: "{1}". \nBackup createad, {2}, {3})'.format(AddonName, os.path.basename(fileName), 5000, icon))
		content=[]

	return content

def SaveList(filname, list):
	try:
		with io.open(filname, 'w', encoding='utf-8') as handle:
			handle.write(unicode(json.dumps(list, indent=4, ensure_ascii=False)))
		success = True
	except Exception as ex:
		xbmc.log(str(ex), 5)
		success = False
	return success

def OKmsg(title, line1, line2 = None, line3 = None):
	dlg = xbmcgui.Dialog()
	dlg.ok(title, line1, line2, line3)
	
def isFileNew(file, deltaInSec):
	lastUpdate = 0 if not os.path.isfile(file) else int(os.path.getmtime(file))
	now = int(time.time())
	return False if (now - lastUpdate) > deltaInSec else True 
	
def GetList(address, cache=0):
	if address.startswith('http'):
		fileLocation = os.path.join(cacheDir, hashlib.md5(address).hexdigest())
		fromCache = isFileNew(fileLocation, cache*60)
		if fromCache:
			response = ReadFile(fileLocation)
		else:
			response = OpenURL(address)
			if cache > 0:
				SaveFile(fileLocation, response)
	else:
		response = ReadFile(address.decode('utf-8'))
	return response
		
def plx2list(url, cache):
	response = GetList(url, cache)
	matches = re.compile("^background=(.*?)$",re.I+re.M+re.U+re.S).findall(response)
	background = None if len(matches) < 1 else matches[0]
	list = [{"background": background}]
	matches = re.compile('^type(.*?)#$',re.I+re.M+re.U+re.S).findall(response)
	for match in matches:
		item=re.compile('^(.*?)=(.*?)$',re.I+re.M+re.U+re.S).findall("type{0}".format(match))
		item_data = {}
		for field, value in item:
			item_data[field.strip().lower()] = value.strip()
		item_data['group'] = 'Main'
		list.append(item_data)
	return list

def m3u2list(url, cache):
	response = GetList(url, cache)	
	matches=re.compile('^#EXTINF:-?[0-9]*(.*?),(.*?)\n(.*?)$',re.I+re.M+re.U+re.S).findall(response)
	li = []
	for params, display_name, url in matches:
		item_data = {"params": params, "display_name": display_name, "url": url}
		li.append(item_data)

	list = []
	for channel in li:
		item_data = {"display_name": channel["display_name"], "url": channel["url"]}
		matches=re.compile(' (.+?)="(.+?)"',re.I+re.M+re.U+re.S).findall(channel["params"])
		for field, value in matches:
			item_data[field.strip().lower().replace('-', '_')] = value.strip()
		list.append(item_data)
	return list
	
def GetEncodeString(str):
	try:
		str = str.decode(chardet.detect(str)["encoding"]).encode("utf-8")
	except:
		try:
			str = str.encode("utf-8")
		except:
			pass
	return str

def DelFile(filname):
	try:
		if os.path.isfile(filname):
			os.unlink(filname)
	except Exception as ex:
		xbmc.log(str(ex), 5)