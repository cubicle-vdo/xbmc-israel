import urllib, urllib2, os, xbmc, xbmcaddon, json

AddonID = 'plugin.video.israelive'
Addon = xbmcaddon.Addon(AddonID)

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
	
def ReadList(fileName):
	try:
		f = open(fileName,'r')
		fileContent = f.read()
		f.close()
		content = json.loads(fileContent)
	except:
		content = []

	return content

def GetMarkedLists():
	list = ["Main"]
	if (Addon.getSetting('radio').lower() == 'true'):
		list = ["radio"] + list
	if (Addon.getSetting('uk').lower() == 'true'):
		list += ["uk"]
	if (Addon.getSetting('france').lower() == 'true'):
		list += ["france"]
	if (Addon.getSetting('russia').lower() == 'true'):
		list += ["russia"]
	return list 
	
def updateLogos(chList):
	logosDir = os.path.join(xbmc.translatePath("special://userdata/addon_data"), AddonID, 'logos')
	if not os.path.exists(logosDir):
		os.makedirs(logosDir)
		
	missingLogosList = []
	for channel in chList:
		if channel["logo"] == "":
			continue
		logo = "{0}.png".format(channel["logo"])
		logoFile = os.path.join(logosDir, logo)
		if not os.path.isfile(logoFile):
			if logo not in missingLogosList:
				missingLogosList.append(logo)
	
	icon = Addon.getAddonInfo('icon')
	logosCount = len(missingLogosList)	
	i = 0
	for logo in missingLogosList: 
		i = i + 1
		percent = i * 100 // logosCount 
		#xbmc.executebuiltin("XBMC.Notification(ISRALIVE, Updating logos... {0}%, {1}, {2})".format(percent, 5000 ,icon))
		logoUrl = "http://thewiz.info/XBMC/_STATIC/logo/{0}".format(logo).replace(" ", "%20")
		logoFile = os.path.join(logosDir, logo)

		try:
			response = urllib2.urlopen(logoUrl)
			if response.code != 200:
				raise
			xbmc.executebuiltin("XBMC.Notification(ISRALIVE, Updating logos... {0}%, {1}, {2})".format(percent, 1000 ,icon))
			#xbmc.executebuiltin("XBMC.Notification(ISRALIVE, Updating '{0}' logo... , {1}, {2})".format(logo, 5000 ,icon))
			data = response.read()
			response.close()
			logoFile = open(logoFile, "wb")
			logoFile.write(data)
			logoFile.close()
		except:
			pass
