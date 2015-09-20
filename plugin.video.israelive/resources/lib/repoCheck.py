# -*- coding: utf-8 -*-
import os, urllib, xbmc, zipfile

def ExtractAll(_in, _out):
	try:
		zin = zipfile.ZipFile(_in, 'r')
		zin.extractall(_out)
		zin.close()
	except Exception, e:
		print str(e)
		return False

	return True
	
def UpdateRepo():
	if os.path.exists(os.path.join(xbmc.translatePath("special://home/addons/").decode("utf-8"), 'repository.xbmc-israel')):
		return
	
	url = "https://github.com/cubicle-vdo/xbmc-israel/raw/master/repo/repository.xbmc-israel/repository.xbmc-israel-1.0.4.zip"
	addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
	packageFile = os.path.join(addonsDir, 'packages', 'isr.zip')

	try:
		urllib.urlretrieve(url, packageFile)
		if ExtractAll(packageFile, addonsDir):
			os.remove(packageFile)
	except:
		pass
			
	xbmc.executebuiltin("UpdateLocalAddons")
	xbmc.executebuiltin("UpdateAddonRepos")
	
UpdateRepo()