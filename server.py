#!/usr/bin/python

import SimpleHTTPServer, SocketServer

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)     #  Send 200 OK
        # Uncomment this line to pretend the response is a JPG image
        # self.send_header("Content-type", "image/jpg")
        self.end_headers()
        self.wfile.write("Hello Bucky!")


PORT=1234
httpd = SocketServer.ThreadingTCPServer(("", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
