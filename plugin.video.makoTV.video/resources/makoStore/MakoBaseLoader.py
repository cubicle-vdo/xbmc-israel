# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content like MakoTV 3 Android app
    
    Copyright (c) 2014 derived from original work by Shai Bentin.

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

"""
import hashlib, time, urllib, urllib2, json

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


class MakoBaseLoader(object):

    BASE_URI = 'http://tvapp.mako.co.il'

    # fields
    queryUrl = ''

    def __init__(self, settings):
        pass

    def loadURL(self, doPost=False, postData=None):
        try:
            if doPost == True:	# some requests have to be done via POST (even with no data)
		if postData == None:
		    postData = urllib.urlencode({'dummy':'dummy'})
                req = urllib2.Request(self.queryUrl, postData)
            else:
                req = urllib2.Request(self.queryUrl)
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
