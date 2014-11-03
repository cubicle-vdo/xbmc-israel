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
from APLoader import APLoader
import AISUtil, APUUIDCreateRequest, APCreateSessionRequest

class APAccountLoader(APLoader):
    
    ACCOUNT_URI = 'v{{api_version}}/accounts/{{account_id}}.json'

    # we need to keep the properties dict for later use
    __settings = {}
        
    def __init__(self, settings):
        super(APAccountLoader, self).__init__(settings) # call the parent constructor with the settings object
        
        self.queryUrl = self.URL +  self.ACCOUNT_URI
        self.queryUrl = self.queryUrl.replace('{{api_version}}', '1' + '2')
        self.queryUrl = self.queryUrl.replace('{{account_id}}', self.accountId)
        self.queryUrl = self.prepareQueryURL(self.queryUrl, None)
	self.__settings = settings

    def loadURL(self):
        bHasUUID = AISUtil.hasUUID(self.__settings)
	if False == bHasUUID:
	    # ask the identity service to generate a UUID and return it to the plugin (POST)
	    uuidCreateReq = APUUIDCreateRequest.APUUIDCreateRequest(self.__settings)
	    uuidDict = uuidCreateReq.loadURL(True)
	    return uuidDict
	else:
	    # open a session and continue normally
	    self.openSession()
	    self.prepareQueryURL()
	    return super(APAccountLoader, self).loadURL()

    def openSession(self):
        uuid = AISUtil.getUUID(self.__settings)
	token = AISUtil.getDeviceAuthToken(self.__settings)
        sessionCreateReq = APCreateSessionRequest.APCreateSessionRequest(self.__settings, uuid, token)
	sessionDict = sessionCreateReq.loadURL(True)

