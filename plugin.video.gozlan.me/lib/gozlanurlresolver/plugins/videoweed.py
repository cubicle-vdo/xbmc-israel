"""
    gozlanurlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
from t0mm0.common.net import Net
import urllib2
from gozlanurlresolver import common
from gozlanurlresolver.plugnplay.interfaces import gozlanurlresolver
from gozlanurlresolver.plugnplay.interfaces import PluginSettings
from gozlanurlresolver.plugnplay import Plugin

class VideoweedResolver(Plugin, gozlanurlresolver, PluginSettings):
    implements = [gozlanurlresolver, PluginSettings]
    name = "videoweed.es"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        #grab stream details
        try:
            html = self.net.http_GET(web_url).content
        except urllib2.URLError, e:
            common.addon.log_error('videoweed: got http error %d fetching %s' %
                                    (e.code, web_url))
            return False
        
        r = re.search('flashvars.domain="(.+?)".*flashvars.file="(.+?)".*' + 
                      'flashvars.filekey="(.+?)"', html, re.DOTALL)
        
        #use api to find stream address
        if r:
            domain, fileid, filekey = r.groups()
            api_call = ('%s/api/player.api.php?user=undefined&codes=1&file=%s' +
                        '&pass=undefined&key=%s') % (domain, fileid, filekey)
        else:
            common.addon.log_error('videoweed: api url not found')
            return False

        try:
            api_html = self.net.http_GET(api_call).content
        except urllib2.URLERROR, e:
            common.addon.log_error('videoweed: failed to call the video API: ' +
                                   'got http error %d fetching %s' %
                                                            (e.code, api_call))
            return False

        rapi = re.search('url=(.+?)&title=', api_html)
        if rapi:
            stream_url = rapi.group(1)
        else:
            common.addon.log_error('videoweed: stream url not found')

        return stream_url


    def get_url(self, host, media_id):
        return 'http://www.videoweed.es/file/%s' % media_id
        
        
    def get_host_and_id(self, url):
        r = re.search('//(.+?)/file/([0-9a-z]+)', url)
        if r:
            return r.groups()
        else:
            return False


    def valid_url(self, url, host):
        return re.match('http://(www.)?videoweed.(es|com)/file/[0-9a-z]+', 
                       url) or 'videoweed' in host

