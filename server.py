#!/usr/bin/python

import SimpleHTTPServer, SocketServer, cgi
import random
import re, datetime

random.seed()

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    __slots__ = ('userId', 'newUser')

    def do_GET(self):
        if self.path == "/form":  # Dispatch based on the URL
            self.send_response(200)      # Send 200 OK
            self.send_header("Content-type", "text/html")
            self.send_header_cookie()
            self.end_headers()
            
            self.wfile.write("""\
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' lang='en' xml:lang='en'>
  <head>
    <title>Demo</title>
  </head>
  <body>
    <p>""");
            self.greeting()
            self.wfile.write("""</p>
    <form action='/form_response' method='POST'>
      <input type='text' name='thename' value='Buckingham U. Badger'/>
      <input type='submit' value='Submit'/>
    </form>
  </body>
</html>""")
            return 
        
        
        self.send_response(200)
        self.send_header_cookie()
        self.end_headers()
        self.greeting()
        self.wfile.write(" Use the uri /form to get started")

    def do_POST(self):
        # We handle here all the POSTs
        bytes = int(self.headers.getheader('content-length')) # Get the number of bytes from the header
        data = self.rfile.read(bytes)        # Read that many bytes
        print "Raw form data:", repr(data)   # Print to console the raw posted data
        dictData = cgi.parse_qs(data)        # Parse form data
        print "Parsed form data:", repr(dictData)   # Print to console the decoded query
        name = dictData['thename'][0]        # Get the name form the form data
        self.send_response(200)
        self.send_header_cookie()
        self.end_headers()

        self.greeting()
        self.wfile.write(" Hello "+name+"!")

    def setUserId(self):
        # Get the user id from the cookie, or create a new one
        # Sets self.userId and self.newUser
        cookie = self.headers.get('Cookie', "")

        self.userId = None
        self.newUser = True
        if cookie != "":
            print "Found cookie:", cookie
            match = re.search('userId=([0-9]+)', cookie)
            if match:
                self.userId = int(match.group(1))
                self.newUser = False
                
        if self.userId == None:
            self.userId = random.randint(1,1000)
            self.newUser = True

    def greeting(self):
        if self.newUser:
            self.wfile.write("Welcome new user %d!" % self.userId)
        else:
            self.wfile.write("Welcome back user %d!" % self.userId)

    def send_header_cookie(self):
        self.setUserId ()
        expiration = datetime.datetime.now() + datetime.timedelta(minutes=2)
        key = "userId"
        val = str(self.userId)
        self.send_header("Set-Cookie", "%s=%s; Expires=%s" % (key, val, expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")))


PORT=4000
httpd = SocketServer.ThreadingTCPServer(("", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
