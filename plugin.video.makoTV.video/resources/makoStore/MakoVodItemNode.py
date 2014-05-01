# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content like MakoTV 3 Android app
    
    Copyright (c) 2014 derived from original work by Shai Bentin.

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

"""
from MakoBaseNode import MakoBaseNode
import json

class MakoVodItemNode(MakoBaseNode):

    # fields relevant for our node
    __directVideoUrl = ''

    def __init__(self, paramsDict):
        super(MakoVodItemNode, self).__init__(paramsDict)    # call base class ctor

	# make sure we work on the correct part
	videoDict = {}
	if 'root' in paramsDict:
	    videoDict = paramsDict['root']['video']
	else:
	    videoDict = paramsDict['video']

	# find large thumbnail or medium one based on priority
	self.guid = videoDict['guid']
	if 'pic_C' in videoDict:
	    self.thumbnailImageURL = videoDict['pic_C']
	elif 'pic_B' in videoDict:
	    self.thumbnailImageURL = videoDict['pic_B']
	elif 'pic' in videoDict:
	    self.thumbnailImageURL = videoDict['pic']
	
	# title and description
	if 'title' in videoDict:
	    self.title = videoDict['title']
	elif 'externalTitle' in videoDict:
	    self.title = videoDict['externalTitle']
	if 'plot' in videoDict:
	    self.description = videoDict['plot']
	elif 'brief' in videoDict:
	    self.description = videoDict['brief']
	
	# video URL, this will require a ticket later
	if 'directVideoUrl' in videoDict:
	    self.__directVideoUrl = videoDict['directVideoUrl']

    def getDirectVideoUrl(self):
        return self.__directVideoUrl
