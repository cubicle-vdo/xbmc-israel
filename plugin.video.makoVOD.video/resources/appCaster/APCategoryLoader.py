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
from APLoader import APLoader

class APCategoryLoader(APLoader):
    
    CATEGORY_URI = 'v{{api_version}}/accounts/{{account_id}}/broadcasters/{{broadcaster_id}}/categories/{{category_id}}.json'
        
    def __init__(self, settings, categoryId = ''):
        super(APCategoryLoader, self).__init__(settings) # call the parent constructor with the settings object
        
        self.queryUrl = self.URL +  self.CATEGORY_URI
        self.queryUrl = self.queryUrl.replace('{{api_version}}', '1' + '2')
        self.queryUrl = self.queryUrl.replace('{{account_id}}', self.accountId)
        self.queryUrl = self.queryUrl.replace('{{broadcaster_id}}', self.broadcasterId)
        self.queryUrl = self.queryUrl.replace('{{category_id}}', categoryId)        
        self.queryUrl = self.prepareQueryURL(self.queryUrl, None)