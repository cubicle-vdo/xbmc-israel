"""
XBMCLocalProxy 0.1
Copyright 2011 Torben Gerkensmeyer

Modified for Livestreamer by your mom 2k15

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import urlparse
import sys
import traceback
import socket
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from livestreamer import Livestreamer
import xbmc, xbmcgui, xbmcaddon
from urllib import unquote
import player

try:
    AddonID = "plugin.video.israelive"
    Addon = xbmcaddon.Addon(AddonID)
    KodiPlayer = Addon.getSetting("dynamicPlayer") == "1"
except:
    KodiPlayer = False

class MyHandler(BaseHTTPRequestHandler):
    """
    Serves a HEAD request
    """
    def do_HEAD(self):
        #print "XBMCLocalProxy: Serving HEAD request..."
        self.answer_request(0)

    """
    Serves a GET request.
    """
    def do_GET(self):
        #print "XBMCLocalProxy: Serving GET request..."
        self.answer_request(1)

    def answer_request(self, sendData):
        try:
            request_path = self.path[1:]
            #print 'request_path: ' + request_path
            if request_path == "stop":
                sys.exit()
            elif request_path == "version":
                self.send_response(200)
                self.end_headers()
                self.wfile.write("Proxy: Running\r\n")
                self.wfile.write("Version: 0.1")
            elif request_path.startswith("?url="):
                if KodiPlayer and sendData:
                    self.send_response(200)
                    url = unquote(request_path[5:]).replace('&', '?', 1)
                    listitem = xbmcgui.ListItem(path=url)
                    xbmc.Player().play(url, listitem)
                    return
                self.serveFile(request_path, sendData)
            else:
                self.send_response(403)
        except:
                traceback.print_exc()
                self.wfile.close()
                return
        try:
            self.wfile.close()
        except:
            pass

    """
    Sends the requested file and add additional headers.
    """
    def serveFile(self, fURL, sendData):
        if (sendData):
            fURL, quality = player.GetStreamUrl(unquote(fURL))
            session = Livestreamer()
            if '|' in fURL:
                    sp = fURL.split('|')
                    fURL = sp[0]
                    headers = dict(urlparse.parse_qsl(sp[1]))
                    session.set_option("http-headers", headers)
                    session.set_option("http-ssl-verify",False)
                    session.set_option("hls-segment-threads",3)
                    session.set_option("stream-segment-threads",3)
            try:
                #streams = session.streams(fURL)
                channel = session.resolve_url(fURL)
                streams = channel.get_streams()
            except Exception as ex:
                traceback.print_exc(file=sys.stdout)
                self.send_response(403)
            self.send_response(200)
            #print "XBMCLocalProxy: Sending headers..."
            self.end_headers()

            #print "XBMCLocalProxy: Sending data..."
            fileout = self.wfile
            try:
                stream = streams[quality]
                try:
                    response = stream.open()
                    buf = 'INIT'
                    while (buf != None and len(buf) > 0):
                        buf = response.read(200 * 1024)
                        fileout.write(buf)
                        fileout.flush()
                    response.close()
                    fileout.close()
                    #print time.asctime(), "Closing connection"
                except socket.error, e:
                    #print time.asctime(), "Client Closed the connection."
                    try:
                        response.close()
                        fileout.close()
                    except Exception, e:
                        return
                except Exception, e:
                    traceback.print_exc(file=sys.stdout)
                    response.close()
                    fileout.close()
            except:
                traceback.print_exc()
                self.wfile.close()
                return
        else:
            self.send_response(200)
            #print "XBMCLocalProxy: Sending headers..."
            self.end_headers()
        try:
            self.wfile.close()
        except:
            pass

class Server(HTTPServer):
    """HTTPServer class with timeout."""

    def get_request(self):
        """Get the request and client address from the socket."""
        self.socket.settimeout(5.0)
        result = None
        while result is None:
            try:
                result = self.socket.accept()
            except socket.timeout:
                pass
        result[0].settimeout(1000)
        return result

class ThreadedHTTPServer(ThreadingMixIn, Server):
    """Handle requests in a separate thread."""
