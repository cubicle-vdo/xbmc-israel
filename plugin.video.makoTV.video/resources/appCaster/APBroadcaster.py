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

class APBroadcaster(APModel):
    '''
    classdocs
    '''
    __rootCategory = ''

    def __init__(self, broadcasterId, param = []):
        for item in param:
            broadcaster = item['broadcaster']
            if broadcasterId == str(broadcaster["id"]):
                self.innerDictionary = broadcaster
                self.__rootCategory = str(self.get('content_category_id'))
                break 
  
    def getRootCategory(self):
        return self.__rootCategory