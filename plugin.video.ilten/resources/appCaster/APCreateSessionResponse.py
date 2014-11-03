# -*- coding: utf-8 -*-
'''
    Created on 26/06/2013

    Copyright (c) 2010-2012 Shai Bentin.
    All rights reserved.  Unpublished -- rights reserved

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

    @author: eli
'''
from APModel import APModel

class APCreateSessionResponse(APModel):
    '''
    classdocs
    '''
    __document = ''
    __signature = ''

    def __init__(self, doc, sig):
        '''
	ctor
	'''

	self.__document = doc
	self.__signature = sig

    def getDocument(self):
        return self.__document

    def getSignature(self):
        return self.__signature

