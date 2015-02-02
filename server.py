#!/usr/bin/python

import SimpleHTTPServer, SocketServer

handler = SimpleHTTPServer.SimpleHTTPRequestHandler

PORT=4000
httpd = SocketServer.ThreadingTCPServer(("", PORT), handler ) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
