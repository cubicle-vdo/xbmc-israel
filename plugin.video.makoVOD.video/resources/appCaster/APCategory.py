# -*- coding: utf-8 -*-
'''
    Created on 27/01/2012

    Copyright (c) 2010-2012 Shai Bentin.
    All rights reserved.  Unpublished -- rights reserved

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

    @author: shai
'''
from APModel import APModel

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
        self.__fanArtImageURL = self.get('large-poster')
        self.__thumbNameImageURL = self.get('icon_url')
        self.__title = self.get('name')
        self.__description = self.get('description')
        
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