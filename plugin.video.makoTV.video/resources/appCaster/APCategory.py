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
	    # find large fan art. In the new Mako, promoted iPad banners are the best, if present
	    if 'main_promoted_content_ipad' in images:
	        self.__fanArtImageURL = images['main_promoted_content_ipad']
	    elif 'main_promoted_content_android' in images:
	        self.__fanArtImageURL = images['main_promoted_content_android']
	    
	    # find a large enough thumb. We can only count on the icon to be present for normal categories in Mako
	    if 'icon' in images:
	        self.__thumbNameImageURL = images['icon']

            # for special categories, we can also try the special category parts as it's better than the original show icon
	    nature = self.get('nature')
	    if None != nature and 'Generic' == nature:
                if 'special_category_small' in images:
                    self.__thumbNameImageURL = images['special_category_small']
	    
	
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