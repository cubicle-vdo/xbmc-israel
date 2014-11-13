# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from livestreamer import Livestreamer
from urllib import unquote

LIVESTREAMER = None

	
def Stream(wfile, url, quality):
	try:
		Streamer(wfile, url, quality)
	except Exception as e:
		#print "Got Exception: ", str(e)
		pass
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

def start(portNum):
	global LIVESTREAMER
	LIVESTREAMER = Livestreamer()
	httpd = ThreadedHTTPServer(("localhost", portNum), StreamHandler)
	print "Livestreamer: Server Starts - {0}:{1}".format("localhost", portNum)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print "Livestreamer: Server Stops - {0}:{1}".format("localhost", portNum)
