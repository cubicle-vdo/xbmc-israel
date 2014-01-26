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
from APModel import APModel

class APExtensions(APModel):
    '''
    classdocs
    APExtensions - the extensions field is a string that can be serialized to a JSON dictionary and contains various
    interesting categories and properties
    '''

    def __init__(self, params={}):
        '''
	ctor
	'''
	self.innerDictionary = params

    def getProgramsCategoryId(self):
        # attempt to find programs category id
	progsCategoryId = self.get('programs_catgeory_id')
	if None == progsCategoryId or '' == progsCategoryId:
	    # with proper spelling
	    progsCategoryId = self.get('programs_category_id')
	return progsCategoryId


