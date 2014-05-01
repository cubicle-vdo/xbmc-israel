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

class MakoSeasonNode(MakoBaseNode):

    # fields
    __seasonURL = ''

    def __init__(self, paramsDict):
        super(MakoSeasonNode, self).__init__(paramsDict)    # call base class ctor
        self.guid = self.get('id')
	self.title = self.get('name')

	# find season URL, when requested returns the same data for the whole program
	self.__seasonURL = self.get('url')

    def getSeasonURL(self):
        return self.__seasonURL

