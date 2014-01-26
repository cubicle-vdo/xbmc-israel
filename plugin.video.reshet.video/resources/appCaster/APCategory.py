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
    classdocs
    '''
    __id = ''
    __thumbNameImageURL = ''
    __fanArtImageURL = ''
    __title = ''
    __description= ''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.innerDictionary = params
        
        self.__id = str(self.get('id'))
        self.__fanArtImageURL = self.get('medium')
        self.__thumbNameImageURL = self.get('large')
        self.__title = self.get('name')
        self.__description = self.get('description')

	# for the new incarnation of the plugin we'll have an images_json section
	imagesStr = self.get('images_json')
	if None != imagesStr and '' != imagesStr:
	    images = json.loads(imagesStr, 'utf-8')
	    # find large fan art
	    if 'category_big_ipad' in images:
	        self.__fanArtImageURL = images['category_big_ipad']
	    elif 'category_big_android_b' in images:
	        self.__fanArtImageURL = images['category_big_android_b']
	    
	    # find a large enough thumb (but not too large as it degrades perf.)
	    if 'category_big_iphone' in images:
	        self.__thumbNameImageURL = images['category_big_iphone']
	    elif 'category_big_android_m' in images:
	        self.__thumbNameImageURL = images['category_big_android_m']
	    elif 'category_small_android_b' in images:
	        self.__thumbNameImageURL = images['category_small_android_b']
	
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