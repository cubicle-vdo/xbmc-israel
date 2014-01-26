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
import APLoader


# collection of static functions used to manage the UUID and auth token

def getDeviceAuthToken(settings):
    if 'deviceAuthToken' in settings:
        return settings['deviceAuthToken']
    else:
        return None

def getUUID(settings):
    if 'UUID' in settings:
        return settings['UUID']
    else:
        return None

def getUUIDSeed(settings):
    deviceId = settings['deviceId']
    if None != deviceId and deviceId != '':
        seed = APLoader.SHA1(deviceId + settings['bundle'])
    return seed

def hasUUID(settings):
    uuid = getUUID(settings)
    if None == uuid or uuid == '':
	return False
    return True


