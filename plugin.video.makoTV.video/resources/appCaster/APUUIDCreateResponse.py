# -*- coding: utf-8 -*-
'''
    Created on 26/06/2013

    Copyright (c) 2010-2012 Shai Bentin.
    All rights reserved.  Unpublished -- rights reserved

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

    @author: eli
'''
from APModel import APModel

class APUUIDCreateResponse(APModel):
    '''
    classdocs
    '''
    __deviceId = ''
    __authToken = ''

    def __init__(self, deviceId, token):
	'''
	ctor
	'''

	self.__deviceId = deviceId
	self.__authToken = token

    def getDeviceId(self):
	return self.__deviceId

    def getAuthToken(self):
	return self.__authToken


