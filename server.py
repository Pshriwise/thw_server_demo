#!/usr/bin/python

from subprocess import call
import SimpleHTTPServer, SocketServer, cgi, cgitb
import random, os
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
            args = self.path.split('?')
            if len(args) > 1: 
                args = args[1]
            else:
                self.readme()
                return
            args = args.split('&')

            arg_dict = {}
            for arg_pair in args:
                temp = arg_pair.split('=')
                arg_dict[temp[0]]=temp[1]

            #create the slice plot
            if 'filename' not in arg_dict or 'axis' not in arg_dict or 'coord' not in arg_dict :
                self.readme()
                return
            filename = arg_dict['filename']
            axis = arg_dict['axis']
            coord = arg_dict ['coord']

            #make external call to create plot image
            call(['python','slice_tool.py','-f',filename,'-axis',axis,'-coord',coord])

            f = open("temp.png",'r')
            self.wfile.write( f.read() )
            return

        
        self.wfile.write("Path is invalid.")
        self.send_response(200)
        self.end_headers()
        return 

        
    def readme(self):
        h5ms = os.listdir("./")
        h5ms = [x for x in h5ms if ".h5m" in x]
        if len(h5ms) == 0: h5ms = ["None"]
        
        self.wfile.write("Please enter a valid filename:\n")
        for x in h5ms: self.wfile.write(x+"\n")
        self.wfile.write("\n path format is /Slice?filename=<your_filename>&axis=<slice_axis>&coord=<slice_coordinate> \n")
        self.wfile.write("\n NOTE: slices only garaunteed for watertight files.")
        return
    

PORT=4000
httpd = SocketServer.ThreadingTCPServer(("", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
