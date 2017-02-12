# -*- coding: utf-8 -*-
import xbmcplugin, xbmcgui
import sys, urlparse, re
import myResolver

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
mode = params.get('mode')
regex = re.compile('[\?|&]mode=(\-?[0-9]+)', re.I+re.M+re.U+re.S)
url = regex.sub('', sys.argv[2][5:]).strip()
url = myResolver.Resolve(url, mode)
listItem = xbmcgui.ListItem(path=url)
xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)