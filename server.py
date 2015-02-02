#!/usr/bin/python

import SimpleHTTPServer, SocketServer

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)     #  Send 200 OK
        self.end_headers()
        self.wfile.write("Hello Bucky!")


PORT=4000
httpd = SocketServer.ThreadingTCPServer(("", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
