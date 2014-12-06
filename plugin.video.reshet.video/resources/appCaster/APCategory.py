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
    __name = ''

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
	self.__name = self.get('name')

	# for the new incarnation of the plugin we'll have an images_json section
	imagesStr = self.get('images_json')
	if None != imagesStr and '' != imagesStr:
	    images = json.loads(imagesStr, 'utf-8')
	    # find large fan art
	    if 'category_big_ipad' in images:
	        self.__fanArtImageURL = images['category_big_ipad']
	    if self.__fanArtImageURL == '' and 'category_big_android_b' in images:
	        self.__fanArtImageURL = images['category_big_android_b']
	    
	    # if we couldnt find a large promoted thumb, go for the regulars
	    if self.__fanArtImageURL == '' and 'large_thumbnail' in images:
	        self.__fanArtImageURL = images['large_thumbnail']
	    
	    # large carousel is used in the new UI. only use if nothing was found
	    if self.__fanArtImageURL == '' and 'Carousel_smartphone_image' in images:
	        self.__fanArtImageURL = images['Carousel_smartphone_image']
	    
	    # parse thumbnail
	    if 'category_small_android_b' in images:
	        self.__thumbNameImageURL = images['category_small_android_b']
	    if self.__thumbNameImageURL == '' and 'vod_small_ipad' in images:
	        self.__thumbNameImageURL = images['vod_small_ipad']

            # if all else fails use the fan art which should already be cached (might degradfe performance a bit)
	    if self.__thumbNameImageURL == '':
	        self.__thumbNameImageURL = self.__fanArtImageURL
	
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

    def getName(self):
        return self.__name