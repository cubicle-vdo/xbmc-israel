# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from livestreamer import Livestreamer
from urllib import unquote

import xbmcaddon, os
Addon = xbmcaddon.Addon("plugin.video.israelive")

HOST_NAME = "localhost"
PORT_NUMBER = 88
LIVESTREAMER = None

		
def Stream(wfile, url, quality):
	try:
		Streamer(wfile, url, quality)
	except Exception as e:
		#print "Got Exception: ", str(e)
		offlineFile = os.path.join(Addon.getAddonInfo("path").decode("utf-8"), 'resources', 'lib', 'offline.mp4')
		wfile.write(open(offlineFile, "r").read())
	wfile.close()

def Streamer(wfile, url, quality):
	global LIVESTREAMER
	channel = LIVESTREAMER.resolve_url(url)
	streams = channel.get_streams()
	if not streams:
		raise Exception("No Stream Found!")
	
	stream = streams[quality]
	fd = stream.open()
	while True:
		buff = fd.read(4096)
		if not buff:
		   raise Exception("No Data!")
		wfile.write(buff)
	fd.close()
	fd = None
	#raise Exception("End Of Data!")

class StreamHandler(BaseHTTPRequestHandler):

	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Server", "Enigma2 Livestreamer")
		s.send_header("Content-type", "text/html")
		s.end_headers()

	def do_GET(s):
		"""Respond to a GET request."""
		s.send_response(200)
		s.send_header("Server", "Enigma2 Livestreamer")
		s.send_header("Content-type", "text/html")
		s.end_headers()

		quality = "best"
		try: 
			import player
			url, quality = player.GetStreamUrl(unquote(s.path[1:]))
		except:
			url = None

		Stream(s.wfile, url, quality)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def start():
	global LIVESTREAMER
	LIVESTREAMER = Livestreamer()
	httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), StreamHandler)
	print "Livestreamer: Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print "Livestreamer: Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
