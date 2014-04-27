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

class MakoProgramNode(MakoBaseNode):
    
    # fields that describe a program in the main content menu
    __programURL = ''

    # ctor
    def __init__(self, paramsDict):
        super(MakoProgramNode, self).__init__(paramsDict)    # call the base node ctor

        # find the thumbnail for the program and its guid
	self.guid = self.get('guid')
	self.thumbnailImageURL = self.get('pic')
	self.title = self.get('title')
	self.description = self.get('brief')
	self.__programURL = self.get('url')    # relative to the base URI

    def getProgramURL(self):
        return self.__programURL

