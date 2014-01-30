# -*- coding: utf-8 -*-
'''
    Created on 21/01/2012

    Copyright (c) 2010-2012 Shai Bentin.
    All rights reserved.  Unpublished -- rights reserved

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

    @author: shai
'''
import types

class APModel(object):
    
    innerDictionary = {}


    def __init__(self):
        '''
        Constructor
        '''
  
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
               
                
                
    