"""
    urlresolver XBMC Addon
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
import urllib2,urllib
import cookielib
from urlresolver import common
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
from xml.sax import saxutils as su

class PutlockerResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "putlocker/sockshare"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()
    
    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        

        #find session_hash
        try:
            html = self.net.http_GET(web_url).content
        except urllib2.URLError, e:
            common.addon.log_error('putlocker: got http error %d fetching %s' %
                                    (e.code, web_url))
            return False
        r = re.search('value="([0-9a-f]+?)" name="hash"', html)
        if r:
            session_hash = r.group(1)
        else:
            common.addon.log_error('putlocker: session hash not found')
            return False

        #post session_hash
        try:
            #html = self.net.http_POST(web_url, form_data={'hash': session_hash, 
            #                       'confirm': 'Continue as Free User',
            #                       }).content
            html = opener.open(web_url,urllib.urlencode({'hash': session_hash,'confirm': 'Continue as Free User'})).read()
        except urllib2.URLError, e:
            common.addon.log_error('putlocker: got http error %d posting %s' %
                                    (e.code, web_url))
            return False
            
        r = re.search('file_password', html)
        if r:
          try:
              #html = self.net.http_POST(web_url, form_data={ 
              #                       'file_password' : 'www.moviex-il.com'
              #                       }).content
              common.addon.log_error('putlocker: Submitting password')
              opener.addheaders = [('Referer',web_url),
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1') ]
              html = opener.open(web_url, urllib.urlencode({ 'file_password' : 'www.moviex-il.com' }) ).read()
          except urllib2.URLError, e:
              common.addon.log_error('putlocker: got http error %d posting %s' %
                                      (e.code, web_url))
              return False


                      #key: '#$0c4de1874473849ff8a'
        r = re.search("key: '\#\$0c4de(.*?)'", html)
        player_key = ""
        if r:
          player_key = r.group(1)
          player_url =  'http://static.putlocker.com/video_player.swf?0.'+player_key
          #common.addon.log_error('putlocker: Downloading player from '+ player_url)          
          #opener.open(player_url).read()
          opener.addheaders = [('Referer',player_url),
                ('User-Agent', 'Mozilla/5.0 (Windowsb NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1') ]
        else:
          print "Key not found\n"

        #find playlist code
        r = re.search('\?stream=(.+?)\'', html)
        if r:
            playlist_code = r.group(1)
        else:
            common.addon.log_error('putlocker: playlist code not found - html='+html)
            return False
        
        #find download link
        xml_url = re.sub('/(file|embed)/.+', '/get_file.php?stream=', web_url)
        xml_url += playlist_code
        try:
            #html = self.net.http_GET(xml_url).content
            html = opener.open(xml_url).read()
        except urllib2.URLError, e:
            common.addon.log_error('putlocker: got http error %d fetching %s' %
                                    (e.code, xml_url))
            return False
        print "XML data:"
        print html
        r = re.search('url="(.+?)(\?|\/)(.+?)"', html)
        cookies = []
        for cookie in cj:
          cookies.append((cookie.name,cookie.value))
          #print "Cookie: "+cookie.name+"="+cookie.value+"\n"
        if r:
            flv_url = r.group(1) + r.group(2) + su.unescape(r.group(3)) + '|Accept='+urllib.quote('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')+'&User-Agent=' + urllib.quote('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1')+'&Accept-Encoding='+urllib.quote('gzip, deflate')+'&Cookie='+urllib.quote('__utma=163708862.388085895.1342125893.1344639465.1344641726.10; __utmz=163708862.1344634373.8.8.utmcsr=moviex-il.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie-%D7%A1%D7%99%D7%A0%D7%93%D7%A8%D7%9C%D7%94-2.html; __utmb=163708862.15.10.1344641726; __utmc=163708862') + '&Connection=' +urllib.quote('Keep-Alive')            
            if player_key!="":
              flv_url=flv_url+"&Referer="+urllib.quote('http://static.putlocker.com/video_player.swf?0.'+player_key)
               
        else:
            common.addon.log_error('putlocker: stream url not found')
            return False
        
        return flv_url

    def get_url(self, host, media_id):
        if 'putlocker' in host:
            host = 'www.putlocker.com'
        else:
            host = 'www.sockshare.com'
        return 'http://%s/file/%s' % (host, media_id)
        
        
    def get_host_and_id(self, url):
        r = re.search('//(.+?)/(?:file|embed)/([0-9A-Z]+)', url)
        if r:
            return r.groups()
        else:
            return False
        
    def valid_url(self, url, host):
        return (re.match('http://(www.)?(putlocker|sockshare).com/' + 
                         '(file|embed)/[0-9A-Z]+', url) or
                'putlocker' in host or 'sockshare' in host)
                 

