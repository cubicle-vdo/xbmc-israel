# -*- coding: utf-8 -*-
'''
    Created on 21/01/2012

    Copyright (c) 2010-2012 Shai Bentin.
    All rights reserved.  Unpublished -- rights reserved

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

    @author: eli
'''
from APModel import APModel

class APChannel(APModel):
    '''
    classdocs
    '''
    __channelId = ''

    def __init__(self, channelId, param = []):
        for item in param:
	    channel = item['channel']
	    if channelId == str(channel['id']):
	        self.innerDictionary = channel
		self.__channelId = str(self.get('id'))
		break

    def getChannelId(self):
        return __channelId


