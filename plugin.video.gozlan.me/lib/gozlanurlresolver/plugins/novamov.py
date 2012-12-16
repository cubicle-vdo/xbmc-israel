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

class NovamovResolver(Plugin, gozlanurlresolver, PluginSettings):
    implements = [gozlanurlresolver, PluginSettings]
    name = "novamov"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        #find key
        try:
            html = self.net.http_GET(web_url).content
        except urllib2.URLError, e:
            common.addon.log_error('novamov: got http error %d fetching %s' %
                                    (e.code, web_url))
            return False

        r = re.search('flashvars.file="(.+?)".+?flashvars.filekey="(.+?)"', 
                      html, re.DOTALL)
        if r:
            filename, filekey = r.groups()
        else:
            common.addon.log_error('novamov: filename and filekey not found')
            return False
        
        #get stream url from api
        api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % \
              (filekey, filename)
        try:
            html = self.net.http_GET(api).content
        except urllib2.URLError, e:
            common.addon.log_error('novamov: got http error %d fetching %s' %
                                    (e.code, api))
            return False

        r = re.search('url=(.+?)&title', html)
        if r:
            stream_url = r.group(1)
        else:
            common.addon.log_error('novamov: stream url not found')
            return False
            
        return stream_url
        

    def get_url(self, host, media_id):
        return 'http://www.novamov.com/video/%s' % media_id
        
        
    def get_host_and_id(self, url):
        #r = re.search('//(?:embed.)?(.+?)/(?:video/|embed.php\?.+?v=)' + 
        r = re.search('//(?:embed.)?(.+?)/(?:video/|embed.php\?.*?v=)' + 
                      '([0-9a-z]+)', url)
        if r:
            return r.groups()
        else:
            return False


    def valid_url(self, url, host):
        return re.match('http://(www.|embed.)?novamov.com/(video/|embed.php\?)' +
                        '(?:[0-9a-z]+|width)', url) or 'novamov' in host

