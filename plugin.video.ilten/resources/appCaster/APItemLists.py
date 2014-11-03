# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content like Channel 10's Android app
    
    Copyright (c) 2014 derived from original work by Shai Bentin.

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: vmaster.

"""
from APModel import APModel
from APCategoryList import APCategoryList
import json

class APItemLists(APModel):
    '''
    Model for special promoted content that doesnt appear in the main categories.
    We really are interested in promoted shows, not specific vod items
    '''

    def __init__(self, params):
	# keep our dictionary
        self.innerDictionary = params

	self.__name = self.get('name')
	self.__id = self.get('id')
	self.__categoryList = None

	# if we have the children part in our dictionary - this gives us a new category list
	if self.isValid():
	    self.__categoryList = APCategoryList(params)

    def isValid(self):
        # used to ignore promoted vod items and other noise
	if self.__name == 'test' or 'vod_items' in self.innerDictionary:
	   return False
	
	# if we have child items, we're good
	if 'children' in self.innerDictionary:
	    return True
	
	return False

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getCategoryList(self):
        return self.__categoryList



	

