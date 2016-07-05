# -*- coding: utf-8 -*-

'''
Created on 30/04/2011

@author: shai
'''

import xbmc,urllib,urllib2,re,xbmcplugin,xbmcaddon,xbmcgui,os,sys,json,io
import wallacommon as common
__BASE_URL__ = 'http://nickjr.walla.co.il/'
__NAME__ = 'nickjr'
__PATTERN__ = '<div class="title w4b"><a href="(.*?)"'
__PATTERN_MORE__ = 'class="p_r"\sstyle=""\shref="(.*?)"'
__PATTERN_FEATURED__ ='<div class="title w5b mt5"><a href="(.*?)"'
_PATTERN_EXTRA_=      '<div class="title w5b mt5"><a href="(.*?"'

AddonID = "plugin.video.wallaNew.video"
Addon = xbmcaddon.Addon(AddonID)

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
images_file = os.path.join(user_dataDir, 'images_file_nickjr.txt')
if not (os.path.isfile(images_file)):
	f = open(images_file, 'w') 
	f.write('{}') 
	f.close() 




def WriteList(filename, list):
	try:
		with io.open(filename, 'w', encoding='utf-8') as handle:
			handle.write(unicode(json.dumps(list, indent=2, ensure_ascii=False)))
		success = True
	except Exception as ex:
		print ex
		success = False
		
	return success

def ReadList(fileName):
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		print ex
		content=[]

	return content

class manager_nickjr:
    
    def __init__(self):
        self.MODES = common.enum(GET_SERIES_LIST=1, GET_EPISODES_LIST=2)
       
        
    def work(self, mode, url='', name='', page=''):
        
        if (mode==self.MODES.GET_SERIES_LIST):
            self.getSeriesList()
        elif(mode==self.MODES.GET_EPISODES_LIST):
            common.getEpisodeList(__BASE_URL__, url, __PATTERN__, __NAME__, self.MODES.GET_EPISODES_LIST, __PATTERN_FEATURED__, __PATTERN_MORE__)
    
    def search(self,values, searchFor):
         for k in values:
            for v in values[k]:
              if searchFor in v:
                return k
         return None

    def getSeriesList(self):
            images=ReadList(images_file)
            contentType,block = common.getMatches(__BASE_URL__,'padding: 10px(.*?)folder2_game')
            page = re.compile('<a href="(.*?)".*?0px;">(.*?)<').findall(block[0])
            print str (images)
            for path in page:
                summary = ''
                iconImage=''
                url=__BASE_URL__ + path[0]
                if not url in images:
                       iconImage=common.getImageNick(url)
                       images[url]=iconImage
                iconImage=images[url]
                title=path[1]
                common.addDir(contentType,title,url, self.MODES.GET_EPISODES_LIST, iconImage, __NAME__, summary)
            WriteList(images_file, images)
            common.addDir('UTF-8',"דורה ביער המכושף", __BASE_URL__ +'?w=//1887291', self.MODES.GET_EPISODES_LIST, "", __NAME__, summary)
            common.addDir('UTF-8',"ספיישל דורה", __BASE_URL__ +'?w=//2630476', self.MODES.GET_EPISODES_LIST, "", __NAME__, summary)
            
            
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
