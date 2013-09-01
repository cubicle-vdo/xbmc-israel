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
import hashlib, time, urllib, urllib2, json

class APLoader(object):
    bundleValue = '' # (OSUtil.getPackageName(CustomApplication.getAppContext()) + "android")
    bundleVersionValue = '1.1' # OSUtil.getAppVersion(CustomApplication.getAppContext())
    osVersionValue = '10' # OSUtil.getAPIVersion()
    deviceModelValue = 'GT-P1000' # Hey I'm a galaxy tab device
    pKey = '' # privateKey from the properties
    
    queryUrl = ''
    URL = 'http://admin.applicaster.com/'
    broadcasterId = ''
    accountId = ''
    deviceIdValue = ''
    
    def __init__(self, settings):
        self.bundleValue = settings['bundle']
        self.pKey = settings['pKey'] #.getSetting("pKey")
        self.broadcasterId = settings['broadcasterId'] # .getSetting('broadcasterId')
        self.accountId = settings['accountId'] # .getSetting('accountId')
        self.deviceIdValue = settings['deviceId']
        
    def MD5 (self, param):
        localMessageDigest = hashlib.md5()
        localMessageDigest.update(param)
        return localMessageDigest.hexdigest()

    def prepareQueryURL(self, paramString = '', paramMap = {}):
        localStringBuffer = str(paramString)
        val = self.prepareUrlParams(self.signRequestParams(paramString, paramMap), True)
        localStringBuffer = localStringBuffer + '?' + val
        return localStringBuffer
    
    def signRequestParams(self, paramString, paramMap):
        localParamMap = {}
        if paramMap != None:
            localParamMap.update(paramMap)
        now = int(time.time())
        localParamMap[self.prepareAPIKey("bundle")] = self.bundleValue
        localParamMap[self.prepareAPIKey("bver")] = self.bundleVersionValue
        localParamMap[self.prepareAPIKey("d")] = "1"
        localParamMap[self.prepareAPIKey("device_model")] = self.deviceModelValue
        localParamMap[self.prepareAPIKey("os_type")] = "android"
        localParamMap[self.prepareAPIKey("os_version")] = self.osVersionValue
        localParamMap[self.prepareAPIKey("timestamp")] = str(now)
        
        localParamMap[self.prepareAPIKey("udid")] = self.deviceIdValue
        localParamMap[self.prepareAPIKey("ver")] = "1.2"
        
        localStringBuilder = self.pKey + paramString + self.prepareUrlParams(localParamMap, False) + self.pKey
        signedValue = self.MD5(localStringBuilder)
        localParamMap[self.prepareAPIKey("sig")] = signedValue
        return localParamMap
        
    def prepareAPIKey(self, key):
        return "api[" + key + "]";

    def prepareUrlParams(self, paramMap = {}, paramBoolean = False):
        localStringBuffer = ''
        i = 0;
        if (paramMap != None):
            mapKeys = paramMap.keys()
            mapKeys.sort()
            for key in mapKeys:
                if (i > 0):
                    localStringBuffer = localStringBuffer + '&'
                value = paramMap.get(key)
                if (paramBoolean):
                    value = urllib.quote_plus(value)
                localStringBuffer = localStringBuffer + key + '=' + value
                i+=1
        return localStringBuffer
    
    def loadURL(self):
        try:
            req = urllib2.Request(self.queryUrl)
            response = urllib2.urlopen(req)
            jsonData = response.read()
            response.close()
            
            datadict = json.loads(jsonData, 'utf-8')
            return datadict
        except:
            return None
        
    def getQuery(self):
        return self.queryUrl