# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content like Channel 10's Android app
    
    Copyright (c) 2014 derived from original work by Shai Bentin.

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: vmaster.

"""
from APLoader import APLoader

class APItemListsLoader(APLoader):
    '''
    Do not confuse with APItemLoader which is a VOD item loader
    '''
    ITEM_LISTS_URI = 'v{{api_version}}/accounts/{{account_id}}/broadcasters/{{broadcaster_id}}/item_lists/{{item_list}}.json'

    def __init__(self, settings, itemId = ''):
        super(APItemListsLoader, self).__init__(settings)    # call the base class ctor with the settings

	self.queryUrl = self.URL + self.ITEM_LISTS_URI
	self.queryUrl = self.queryUrl.replace("{{api_version}}", "1" + "2")
        self.queryUrl = self.queryUrl.replace("{{account_id}}", self.accountId)
        self.queryUrl = self.queryUrl.replace("{{broadcaster_id}}", self.broadcasterId)
	self.queryUrl = self.queryUrl.replace("{{item_list}}", str(itemId));

        self.queryUrl = self.prepareQueryURL(self.queryUrl, None)

