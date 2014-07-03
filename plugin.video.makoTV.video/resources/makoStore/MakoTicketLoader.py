# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content like MakoTV 3 Android app
    
    Copyright (c) 2014 derived from original work by Shai Bentin.

    Use of a copyright notice is precautionary only, and does
    not imply publication or disclosure.
 
    Licensed under Eclipse Public License, Version 1.0
    Initial Developer: Shai Bentin.

"""
from urlparse import urlparse
import urllib, urllib2
from MakoBaseLoader import MakoBaseLoader
import json

class MakoTicketLoader(MakoBaseLoader):

    # the ticket for the video item we want
    __ticket = ''

    def __init__(self, settings, url, id):
        super(MakoTicketLoader, self).__init__(settings)    # call base class ctor
	self.queryUrl = 'http://mass.mako.co.il/ClicksStatistics/entitlementsServices.jsp'
	self.queryUrl = self.queryUrl + '?et=gt'
	self.queryUrl = self.queryUrl + '&da=' + settings['appId']
	self.queryUrl = self.queryUrl + '&na=' + settings['appVer']
	self.queryUrl = self.queryUrl + '&du=' + settings['UDID']
	self.queryUrl = self.queryUrl + '&dv=' + id
	self.queryUrl = self.queryUrl + '&rv=akamai'

	# extract the domain and use it to extract just the path and query string
	parsedUrl = urlparse(url)
	domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsedUrl)  # intentionally dont include the last /
	path = url[len(domain):]

	self.queryUrl = self.queryUrl + '&lp=' + urllib.quote_plus(path)

    def loadURL(self, doPost=False, postData=None):
        # we must perform a POST with all arguments in the query string
	ticketDict = super(MakoTicketLoader, self).loadURL(True)

        # find the ticket in the tickets section
	if 'tickets' in ticketDict:
	    ticket = ticketDict['tickets'][0]
	    if 'ticket' in ticket:
	        self.__ticket = ticket['ticket']

	return ticketDict   # generally we dont need this

    def getTicket(self):
        return self.__ticket


