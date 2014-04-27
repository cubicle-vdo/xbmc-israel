# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content like MakoTV 3 Android app
    
    Copyright (c) 2014 derived from original work by Shai Bentin.

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

"""
import json, types

class MakoBaseNode(object):

    # inner dictionary of values
    innerDictionary = {}
    
    # fields
    guid = ''
    thumbnailImageURL = ''
    fanArtImageURL = ''
    title = ''
    description = ''

    def __init__(self, paramsDict):
        self.innerDictionary = paramsDict

    def getGUID(self):
        return self.guid

    def getThumbnailURL(self):
        return self.thumbnailImageURL

    def getTitle(self):
        return self.title

    def getDescription(self):
        return self.description

    # get a value from our dictionary (or an included dictionary inside it) without throwing an exception
    def get(self, lookfor = ''):
        return self.__get(lookfor, self.innerDictionary)
    
    # private method
    def __get(self, lookfor = '', dictionary = {}):
        if None == lookfor:
            return ''
        result = ''
        for key in dictionary.keys():
            if key == lookfor:
                return dictionary[key]
            try:
                evaluate = eval("("+dictionary[key]+")")
                if isinstance(evaluate, types.DictType):
                    result = self.__get(lookfor, evaluate)
                    if result != '':
                        break;
            except:
                pass
        
        # if its not a key in the innerDictionary and not a key in one of the dictionaries included
        # IN the dictionary it will return an empty value.
        return result
               
