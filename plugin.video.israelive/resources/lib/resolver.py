# -*- coding: utf-8 -*-
import re, urllib, xbmc, xbmcaddon
import myResolver

AddonID = "plugin.video.israelive"
Addon = xbmcaddon.Addon(AddonID)
useRtmp = Addon.getSetting("StreramProtocol") == "1"

def resolveUrl(url):
	xbmc.log("{0}".format(url), 3)
	try:
		if '.f4m' in url:
			url = url.replace('&mode=3', '').replace('?mode=3', '')
			if 'keshet' in url:
				ticket = myResolver.GetMinus2Ticket()
				url = "{0}?{1}&hdcore=3.0.3".format(url, ticket)
			from F4mProxy import f4mProxyHelper
			url = f4mProxyHelper().playF4mLink(urllib.unquote_plus(url))
		elif "mode=" in url:
			matches = re.compile('^(.*?)[\?|&]mode=(\-?[0-9]+)(.*?)$', re.I+re.M+re.U+re.S).findall(url)
			if len(matches) > 0:
				url = matches[0][0]
				mode = matches[0][1]
				if len(matches[0]) > 2:
					url += matches[0][2]
				if mode == '0':
					mode = '-3'
					url = url[url.rfind(';')+1:]
				url = myResolver.Resolve(url, mode, useRtmp=useRtmp)
		if url is None or url == "down":
			return None
		return url
	except Exception as ex:
		xbmc.log("{0}".format(ex), 3)
		return None