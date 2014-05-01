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

class MakoVodIndexLoader(MakoBaseLoader):

    INDEX_URL = '/mako-vod-index'

    def __init__(self, settings):
        super(MakoVodIndexLoader, self).__init__(settings) # call the parent constructor with the settings object
	self.queryUrl = self.BASE_URI + self.INDEX_URL
