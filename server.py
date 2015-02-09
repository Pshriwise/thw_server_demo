#!/usr/bin/python

from subprocess import call
import SimpleHTTPServer, SocketServer, cgi
import random
import re, datetime

random.seed()

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    __slots__ = ('userId', 'newUser')

    def do_GET(self):
        
        if "/Slice" in self.path:
            
            self.send_response(200)      # Send 200 OK
            self.send_header("Content-type", "png")

            self.end_headers()

            #prepare the image to return 
            
            #get arguments from the path
            args = self.path.split('?')[1]
            args = args.split('&')

            arg_dict = {}
            for arg_pair in args:
                temp = arg_pair.split('=')
                arg_dict[temp[0]]=temp[1]

            #create the slice plot
            filename = arg_dict['filename']
            axis = arg_dict['axis']
            coord = arg_dict ['coord']

            #make external call to create plot image
            call(['python','slice_tool.py','-f',filename,'-axis',axis,'-coord',coord])

            f = open("temp.png",'r')
            self.wfile.write( f.read() )
            return

        self.send_response(200)
        self.wfile.write("URL is invalid.")
        

PORT=4000
httpd = SocketServer.ThreadingTCPServer(("", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
