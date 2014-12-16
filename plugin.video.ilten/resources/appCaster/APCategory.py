# -*- coding: utf-8 -*-
'''
    Created on 21/01/2012

    Copyright (c) 2010-2012 Shai Bentin.
    All rights reserved.  Unpublished -- rights reserved

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

    @author: shai
'''
from APModel import APModel
import json

class APCategory(APModel):
    '''
    Represent one category (folder). A category can have subcategories or vod items
    '''
    def __init__(self, params):
        self.innerDictionary = params

	self.__thumbNameImageURL = ''
	self.__fanArtImageURL = ''
        self.__id = str(self.get('id'))
        self.__title = self.get('name')
        self.__description = self.get('description')

	# for the new incarnation of the plugin we'll have an images_json section
	imagesStr = self.get('images_json')
	if None != imagesStr and '' != imagesStr:
	    images = json.loads(imagesStr, 'utf-8')

	    # find large fan art
	    if 'large_thumbnail' in images:
	        self.__fanArtImageURL = images['large_thumbnail']
	    
	    # find a large enough thumb (but not too large as it degrades perf.)
	    if 'small_thumbnail' in images:
	        self.__thumbNameImageURL = images['small_thumbnail']

	    # fine tab icon. if found this represents a special tab in the app
	    if 'tab_icon_ipad_on' in images:
	        icon = images['tab_icon_ipad_on']
		if icon != '' and icon != None:
	            self.__thumbNameImageURL = images['tab_icon_ipad_on']
		    self.__fanArtImageURL = ''
	
    def getId(self):
        return self.__id
    
    def getThumbnail(self):
        return self.__thumbNameImageURL
    
    def getFanartImage(self):
        return self.__fanArtImageURL
    
    def getTitle(self):
        return self.__title
    
    def getDescription(self):
        return self.__description