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
import AISUtil

# static MD5 hash function
def MD5 (param):
    localMessageDigest = hashlib.md5()
    localMessageDigest.update(param)
    return localMessageDigest.hexdigest()

# static SHA1 hash function
def SHA1 (param):
    localMessageDigest = hashlib.sha1()
    localMessageDigest.update(param)
    return localMessageDigest.hexdigest()


class APLoader(object):
    bundleValue = '' # (OSUtil.getPackageName(CustomApplication.getAppContext()) + "android")
    bundleVersionValue = '5.0' # OSUtil.getAppVersion(CustomApplication.getAppContext())
    osVersionValue = '19' # OSUtil.getAPIVersion()
    deviceModelValue = 'Nexus 7' # upgraded to Nexus 7
    pKey = '' # privateKey from the properties
    
    queryUrl = ''
    URL = 'http://admin.applicaster.com/'
    broadcasterId = ''
    accountId = ''
    deviceIdValue = ''
    userIdValue = ''
    
    def __init__(self, settings):
        self.bundleValue = settings['bundle']
        self.pKey = settings['pKey'] #.getSetting("pKey")
        self.broadcasterId = settings['broadcasterId'] # .getSetting('broadcasterId')
        self.accountId = settings['accountId'] # .getSetting('accountId')
        self.deviceIdValue = settings['deviceId']
        if 'UUID' in settings:
            self.userIdValue = settings['UUID']

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
        #localParamMap[self.prepareAPIKey("d")] = "1"
        localParamMap[self.prepareAPIKey("device_model")] = self.deviceModelValue
        localParamMap[self.prepareAPIKey("os_type")] = "android"
        localParamMap[self.prepareAPIKey("os_version")] = self.osVersionValue
        localParamMap[self.prepareAPIKey("timestamp")] = str(now)
        
        localParamMap[self.prepareAPIKey("token")] = self.deviceIdValue
        localParamMap[self.prepareAPIKey("uuid")] = self.userIdValue
        localParamMap[self.prepareAPIKey("ver")] = "1.2"
        
        localStringBuilder = self.pKey + paramString + self.prepareUrlParams(localParamMap, False) + self.pKey
        signedValue = MD5(localStringBuilder)
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
    
    def loadURL(self, doPost=False, postData={}):
        try:
            if doPost == True: # some requests have to be done via POST (even with no data)
                req = urllib2.Request(self.queryUrl, postData)
            else:
                req = urllib2.Request(self.queryUrl)
            req.add_header('User-Agent', "%D7%A8%D7%A9%D7%AA/24.8.11.46 CFNetwork/672.0.2")
            response = urllib2.urlopen(req)
            jsonData = response.read()
            response.close()

            # uncomment for debug
            #print 'jsonData: '+jsonData
            
            datadict = json.loads(jsonData, 'utf-8')
            return datadict
        except:
            return None
        
    def getQuery(self):
        return self.queryUrl