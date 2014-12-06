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
from APLoader import APLoader


class APCreateSessionRequest(APLoader):

    SESSION_CREATE_URI = 'buckets/{{bucket_id}}/sessions.json'

    def __init__(self, settings, uuid, deviceAuthToken):
        super(APCreateSessionRequest, self).__init__(settings) # call the parent constructor with the settings object

	self.queryUrl = 'https://ais-api.applicaster.com/api/v1/buckets/{{bucket_id}}/sessions.json'
	self.queryUrl = self.queryUrl.replace('{{bucket_id}}', settings['bucketId'])
	self.queryUrl = self.queryUrl + '?device[id]=' + uuid
	self.queryUrl = self.queryUrl + '&device[token]=' + deviceAuthToken

