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
from lib.megavideo import Megavideo
import re
from t0mm0.common.net import Net
from gozlanurlresolver import common
from gozlanurlresolver.plugnplay.interfaces import gozlanurlresolver
from gozlanurlresolver.plugnplay.interfaces import PluginSettings
from gozlanurlresolver.plugnplay import Plugin

class MegavideoResolver(Plugin, gozlanurlresolver, PluginSettings):
    implements = [gozlanurlresolver, PluginSettings]
    name = "megavideo"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        #just call megavideo library
        m = Megavideo(web_url)
        
        if m.is_valid():
            return m.getLink()
        else:
            common.addon.log_error('megavideo: stream url not found')
            return False
        
        
    def get_url(self, host, media_id):
        return 'http://www.megavideo.com/?v=%s' % media_id
        
        
    def get_host_and_id(self, url):
        r = re.search('//(.+?)/(?:v/|\?v=)([0-9A-Z]+)', url)
        if r:
            return r.groups()
        else:
            return False


    def valid_url(self, url, host):
        return re.match('http://(www.)?megavideo.com/(v/|\?v=)[0-9A-Z]+', 
                        url) or 'megavideo' in host


