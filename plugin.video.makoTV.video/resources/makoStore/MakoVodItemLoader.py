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

class MakoVodItemLoader(MakoBaseLoader):

    def __init__(self, settings, url):
        super(MakoVodItemLoader, self).__init__(settings)    # call base class ctor
	self.queryUrl = self.BASE_URI + url
	self.queryUrl = self.queryUrl + '?consumer=' + settings['consumer']
