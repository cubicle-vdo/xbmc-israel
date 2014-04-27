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
import json

class MakoSeasonLoader(MakoBaseLoader):

    __guid = ''

    def __init__(self, settings, url, id):
        super(MakoSeasonLoader, self).__init__(settings)    # call base class ctor
	self.queryUrl = self.BASE_URI + url
	self.queryUrl = self.queryUrl + '?programType=regular'
	self.__guid = id

    def loadURL(self):
        
	seasonDict = {}

        # load the URL but only get the season we're interested in
	allSeasonsDict = super(MakoSeasonLoader, self).loadURL()
	seasons = allSeasonsDict['root']['programData']['seasons']
	for season in seasons:
	    # identify the season and extract it's vod items dictionary
	    try:
	        id = season['id']
		if id == self.__guid:
		    seasonDict = season
	    except:
	        pass

	return seasonDict