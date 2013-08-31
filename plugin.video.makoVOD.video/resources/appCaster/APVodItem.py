# -*- coding: utf-8 -*-
'''
    Created on 23/01/2012

    Copyright (c) 2010-2012 Shai Bentin.
    All rights reserved.  Unpublished -- rights reserved

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

    @author: shai
'''
from APModel import APModel

class APVodItem(APModel):
    '''
    classdocs
    '''
    __free = False
    __id = ''
    __title = ''
    __description = ''
    __thumbnail = ''
    __stream = ''
    
    def __init__(self, params = {}):
        self.innerDictionary = params
        try:
            self.__free = self.get('free')
            self.__id = str(self.get('id'))
            self.__description = self.get('summary')
            self.__title = self.get('title')
            self.__thumbnail = self.get('large_thumb')
            self.__stream = self.get('stream_url')
        except:
            pass
        
    def isFree(self):
        return self.__free
    
    def getId(self):
        return self.__id
    
    def getTitle(self):
        return self.__title
    
    def getDescription(self):
        return self.__description
    
    def getThumbnail(self):
        return self.__thumbnail
    
    def getStreamUrl(self):
        return self.__stream