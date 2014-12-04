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
import urllib
from APLoader import APLoader
import AISUtil

class APUUIDCreateRequest(APLoader):

    UUID_REQUEST_URI = 'buckets/{{bucket_id}}/devices.json'

    def __init__(self, settings):
	super(APUUIDCreateRequest, self).__init__(settings) # call the parent constructor with the settings object

	self.queryUrl = 'https://ais-api.applicaster.com/api/v1/buckets/{{bucket_id}}/devices.json'
	self.queryUrl = self.queryUrl.replace('{{bucket_id}}', settings['bucketId'])
	self.queryUrl = self.queryUrl + '?device[device_model]=' + urllib.quote_plus(self.deviceModelValue)
	self.queryUrl = self.queryUrl + '&device[os_type]=android'
	self.queryUrl = self.queryUrl + '&device[os_version]=' + self.osVersionValue
	self.queryUrl = self.queryUrl + '&device[bundle_id]=' + self.bundleValue
	self.queryUrl = self.queryUrl + '&device[bundle_version]=' + self.bundleVersionValue
	self.queryUrl = self.queryUrl + '&device[app_id]=101567'
	# create a seed from the device ID and bundle value, used to generate a UUID by the identiity service
	seed = AISUtil.getUUIDSeed(settings)
	self.queryUrl = self.queryUrl + '&device[uuid]=' + seed


