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

import os
import random
import re
import urllib2

from lib import _megaupload
from gozlanurlresolver.plugnplay.interfaces import gozlanurlresolver
from gozlanurlresolver.plugnplay.interfaces import SiteAuth
from gozlanurlresolver.plugnplay.interfaces import PluginSettings
from gozlanurlresolver.plugnplay import Plugin
from gozlanurlresolver import common
import xbmc

class MegaUploadResolver(Plugin, gozlanurlresolver, SiteAuth, PluginSettings):
    implements = [gozlanurlresolver, SiteAuth, PluginSettings]
    name = "megaupload"
    profile_path = common.profile_path    
    cookie_file = os.path.join(profile_path, '%s.cookies' % name)

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        try:
            os.makedirs(os.path.dirname(self.cookie_file))
        except OSError:
            pass


    #gozlanurlresolver methods
    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        media_url = _megaupload.resolveURL(web_url, self.cookie_file)
        common.addon.log_debug('login type: %s' % self.login_type)
        ok = True
        if self.login_type == 'free':
            ok = common.addon.show_countdown(25, title='megaupload', text='loading video from free account')
        elif not self.login_type:
            ok = common.addon.show_countdown(45, title='megaupload',
                                        text='loading video with no account')
        if ok:
            return media_url[0]
        else:
            return False
        
    def get_url(self, host, media_id):
        return 'http://www.megaupload.com/?d=%s' % media_id
        
        
    def get_host_and_id(self, url):
        r = re.search('//(.+?)/\?d=([0-9A-Z]+)', url)
        if r:
            return r.groups()
        else:
            return False


    def valid_url(self, url, host):
        return (re.match('http://(www.)?megaupload.com/\?d=' + 
                        '([0-9A-Z]+)', url) or 'megaupload' in host)
    
    #SiteAuth methods
    def login(self):
        self.login_type = None
        if self.get_setting('login') == 'true':
            self.login_type = _megaupload.doLogin('regular', self.cookie_file, 
                                                  self.get_setting('username'), 
                                                  self.get_setting('password'))
        #there must be a better way of doing this
        #xbmc freezes if you load the countdown dialog too quickly 
        xbmc.sleep(1000)

    #PluginSettings methods
    def get_settings_xml(self):
        xml = PluginSettings.get_settings_xml(self)
        xml += '<setting id="MegaUploadResolver_login" '
        xml += 'type="bool" label="login" default="false"/>\n'
        xml += '<setting id="MegaUploadResolver_username" enable="eq(-1,true)" '
        xml += 'type="text" label="username" default=""/>\n'
        xml += '<setting id="MegaUploadResolver_password" enable="eq(-2,true)" '
        xml += 'type="text" label="password" option="hidden" default=""/>\n'
        return xml
