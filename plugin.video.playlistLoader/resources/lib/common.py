import urllib, urllib2, os, io, xbmc, xbmcaddon, xbmcgui, json, re

AddonID = 'plugin.video.playlistLoader'
Addon = xbmcaddon.Addon(AddonID)
icon = Addon.getAddonInfo('icon')
AddonName = Addon.getAddonInfo("name")

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
		data = response.read().replace("\r", "")
	
	response.close()
	return data

def ReadFile(fileName):
	try:
		f = open(fileName,'r')
		content = f.read().replace("\n\n", "\n")
		f.close()
	except:
		content = ""

	return content
	
def ReadList(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		print ex
		if os.path.isfile(fileName):
			import shutil
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
		print ex
		success = False
		
	return success

def OKmsg(title, line1, line2 = None, line3 = None):
	dlg = xbmcgui.Dialog()
	dlg.ok(title, line1, line2, line3)
	
def plx2list(url, group="Main"):
	if url.find("http") >= 0:
		response = OpenURL(url)
	else:
		response = ReadFile(url)
	matches = re.compile("^background=(.*?)$",re.I+re.M+re.U+re.S).findall(response)
	background = None if len(matches) < 1 else matches[0]
	list = [{"background": background}]
	matches = re.compile('^type(.*?)#$',re.I+re.M+re.U+re.S).findall(response)
	for match in matches:
		item=re.compile('^(.*?)=(.*?)$',re.I+re.M+re.U+re.S).findall("type{0}".format(match))
		item_data = {}
		for field, value in item:
			item_data[field.strip().lower()] = value.strip()
		item_data['group'] = group
		list.append(item_data)
	return list

'''
flattenList = []
def flatten(list):
	global flattenList
	for item in list:
		if item['type'] != 'playlist':
			flattenList.append(item)
		else:
			list2 = plx2list(item['url'], item['name'])
			flatten(list2)
			
#list = plx2list(mainPlxUrl, "Main")
#flatten(list) 
'''

def m3u2list(url):
	if url.find("http") >= 0:
		response = OpenURL(url)
	else:
		response = ReadFile(url)
		
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
		import chardet
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
	except Exception as e:
		print e