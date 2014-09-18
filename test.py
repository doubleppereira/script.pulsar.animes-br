#!/usr/bin/env python
import sys
import json
import json
import base64
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

if len(sys.argv) < 4:
    print 'Usage: ./test.py HTTP_PORT METHOD ARG1 "ARG TWO" ARG3 ...\nEx:' 
    print './test.py 9001 search divergent'
    print './test.py 9001 search 1840309'
    print './test.py 9001 search_movie 1840309 divergent 2014'
    print './test.py 9001 search "spider man"'
    sys.exit(1)

HOST_NAME = '127.0.0.1'
PORT_NUMBER = int(sys.argv[1])
METHOD = sys.argv[2]
i = 0
ARGS = []
for ARG in sys.argv:
    if i >= 3:
        ARGS.append(ARG)
    i = i + 1
    
URL = "http://" + HOST_NAME + ":" + str(PORT_NUMBER) + "/"
REQUEST = json.dumps({ "method": METHOD, "callback_url": URL, "args": ARGS})
PAYLOAD = base64.b64encode(REQUEST)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
       self.data_string = self.rfile.read(int(self.headers['Content-Length']))
       self.send_response(200)
       self.end_headers()
       print '\nResponse:\n' + self.data_string
       print '\nPress CTRL+c to end'

server_address = (HOST_NAME, PORT_NUMBER)
httpd = HTTPServer(server_address, Handler)
print 'Waiting for callback at ' + URL
print '\nRequest:\n' + REQUEST
subprocess.Popen(["python", "main.py",PAYLOAD])
try:
     httpd.serve_forever()
except KeyboardInterrupt:
     pass
httpd.server_close()
print 'Stopped'
