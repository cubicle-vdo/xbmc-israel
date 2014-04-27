# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content like MakoTV 3 Android app
    
    Copyright (c) 2014 derived from original work by Shai Bentin.

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

"""
from MakoBaseLoader import MakoBaseLoader

class MakoProgramLoader(MakoBaseLoader):

    def __init__(self, settings, url):
        super(MakoProgramLoader,self).__init__(settings)    # call base class ctor
	self.queryUrl = self.BASE_URI + url
	self.queryUrl = self.queryUrl + '?programType=regular'

    def loadURL(self, doPost=False, postData=None):
        # first we perform a normal load
	programDict = super(MakoProgramLoader, self).loadURL()
	programDict = programDict['root']

	# if this is a special type of program with channels and other ilk, locate the VOD section
	if 'specialProgram' in programDict:
	    specialChannels = programDict['specialProgram']
	    for chan in specialChannels:
	        # locate the vod "channel"
		if 'contentSwitch' in chan:
		    content = chan['contentSwitch']
		    if content == 'VOD-Program':
		        # adjust our query URL to point the correct section and reload
			self.queryUrl = self.BASE_URI + chan['link']
			print '***** reloading program with new URL: ' + self.queryUrl
			programDict = self.loadURL()
			print '***** loaded JSON: ' + str(programDict)
	
	return programDict