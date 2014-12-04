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
import urllib2, json
from APModel import APModel
import resources.m3u8 as m3u8

class APVodItem(APModel):
    '''
    classdocs
    '''
    __free = False
    __id = ''
    __title = ''
    __description = ''
    __thumbnail = ''
    __stream = ''
    __season = ''
    __hls_cookie = ''
    __isHls = False
    __airDate = ''
    
    def __init__(self, params = {}):
        self.innerDictionary = params
        try:
            self.__free = self.get('free')
            self.__id = str(self.get('id'))
            self.__description = self.get('summary')
            self.__title = self.get('title')
            self.__thumbnail = self.get('thumbnail')
            self.__stream = self.get('stream_url')
	    self.__airDate = self.get('order_date')
	    self.__season = self.get('season_name')
	except:
	    pass

	# for the new incarnation of the plugin we'll have an images_json section
	imagesStr = self.get('images_json')
	#print '***** imagesStr is: ' + imagesStr
	if None != imagesStr and '' != imagesStr:
	    images = json.loads(imagesStr, 'utf-8')

	    # find large thumbnail
	    if 'large_thumbnail' in images:
	        self.__thumbnail = images['large_thumbnail']
	    if self.__thumbnail == '' and 'Carousel_smartphone_image' in images:
	        # if not, try carousel image (based on new UI)
	        self.__thumbnail = images['Carousel_smartphone_image']

        #except:
        #    pass
        
    def isFree(self):
        return self.__free
    
    def getId(self):
        return self.__id
    
    def getTitle(self):
        return self.__title
    
    def getDescription(self):
        return self.__description
    
    def getThumbnail(self):
        return self.__thumbnail
    
    def getStreamUrl(self):
	'''
	In newer builds of Gotham (13.0), ffmpeg 1.2 is included. It supports cookies better now and doesn't probe the input via HEAD (only GET) so work normally
	'''
	return self.__stream

    def getAirDate(self):
        return self.__airDate

    def getSeasonName(self):
        return self.__season

    def getHLSCookie(self):
        return self.__hls_cookie

    def isHLS(self):
        '''
	returns True if the stream URL points to an HTTP live streaming playlist of any kind (normal or variant)
	'''
	urlPath = self.__stream.rsplit('?')[0]
	self.__isHls = urlPath.endswith('m3u8');
	return self.__isHls

    def processHLSPlaylist(self, bFindBest=False):
        '''
	given a URL, determine if it's an HTTP live streaming playlist and find the best segments to use (only if we dont trust ffmpeg)
	'''
        # make sure it's a playlist at all, safe to rsplit
        urlPath = self.__stream.rsplit('?')[0]
	if False == urlPath.endswith('m3u8'):
	    return self.__stream

	self.__isHls = True

	# obtain the playlist and save any cookie that might be set. urlllib will join Set-Cookie headers based on RFC (one of them :)
	req = urllib2.Request(self.__stream)
	response = urllib2.urlopen(req)
	playlistStr = response.read()
	self.__hls_cookie = self.cleanCookie(response.info().getheader('Set-Cookie'))
	response.close()

	# parse m3u8 to find the best bitrate segments. if not variant, return original URL
	urlPath = self.__stream
	if bFindBest == True:
	    variant_m3u8 = m3u8.loads(playlistStr)
	    if True == variant_m3u8.is_variant:
	        maxBW=0
	        maxIdx=0
	        for i, playlist in enumerate(variant_m3u8.playlists):
	            bw = int(playlist.stream_info.bandwidth)
		    if bw > maxBW:
		        maxBW = bw
		        maxIdx = i
	        playlist = variant_m3u8.playlists[maxIdx]

	        # build segments URL
	        urlPath = urlPath.rsplit('/', 1)[0]	# removes the filename
	        urlPath = urlPath + '/' + playlist.uri

        return urlPath

    def cleanCookie(self, cookieStr):
        cookies = cookieStr.split(';')
	authCookie = ''
	for cookie in cookies:
	    pos = cookie.lower().find('hdea_l')
	    if pos >= 0:
		authCookie = authCookie + cookie[pos:] + '; '
	    pos = cookie.lower().find('hdea_s')
	    if pos >= 0:
		authCookie = authCookie + cookie[pos:] + '; '
	return authCookie
