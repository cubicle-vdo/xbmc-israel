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

from t0mm0.common.net import Net
from gozlanurlresolver.plugnplay.interfaces import gozlanurlresolver
from gozlanurlresolver.plugnplay.interfaces import PluginSettings
from gozlanurlresolver.plugnplay import Plugin
import urllib2
from gozlanurlresolver import common

# Custom imports
import re
from base64 import b64decode
try:
  from json import loads
except ImportError:
  from simplejson import loads



class VideozerResolver(Plugin, gozlanurlresolver, PluginSettings):
    implements = [gozlanurlresolver, PluginSettings]
    name = "videozer"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()
        self.pattern = 'http://((?:www.)?videozer.com)/(?:embed|video)?/([0-9a-zA-Z]+)'


    def get_media_url(self, host, media_id):

        #grab url for this video
        settings_url = "http://www.videozer.com/" + \
            "player_control/settings.php?v=%s" % media_id

        try:
            html = self.net.http_GET(settings_url).content
        except urllib2.URLError, e:
            common.addon.log_error(self.name + ': got http error %d fetching %s' %
                                    (e.code, settings_url))
            return False

        # Try to load the datas from html. This data should be json styled.
        aData = loads(html)

        # Decode the link from the json data settings.
        sMediaLink = b64decode(aData["cfg"]["environment"]["token1"])

        return sMediaLink

    def get_url(self, host, media_id):
            return 'http://www.videozer.com/video/%s' % (media_id)

    def get_host_and_id(self, url):
        r = re.search(self.pattern, url)
        if r:
            return r.groups()
        else:
            return False


    def valid_url(self, url, host):
        return re.match(self.pattern, url) or self.name in host
