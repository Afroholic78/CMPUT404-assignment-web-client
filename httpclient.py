#!/usr/bin/env python
# coding: utf-8
# Copyright 2015 Mickael Zerihoun
# Collaborated with Jake Brand, Thomas Curnow, Dylan Cassidy
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = int (code)
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        # If a port isn't provided connect to port 80
        if(not port):
            port = 80

        if(not host):
            host = localhost

        # Initiate socket connection and return the socket
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((host,port))
        except:
            print "Did not bind on " + host + str(port)
        return s

    def get_code(self, data):  
        return code

    # From the response, extract the code and return it
    def get_headers(self,data):
        header = data.split("\r\n\r\n", 1)[0]
        code = header.split(" ")[1]
        return code

    # From the response, extract the body and return it
    def get_body(self, data):
        body = data.split("\r\n\r\n", 1)[1]
        return body

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    # receive the url and parse out the host, path and port
    def GET(self, url, args=None):
       
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        path = parsed_url.path
        port = parsed_url.port

        if(not path):
            path = "/"
        # Construct the GET header
        get_rekt = "GET " + path + " HTTP/1.1\r\n"
        get_rekt += "Host:" + host + "\r\n"
        get_rekt += "Accept: */*\r\n"
        get_rekt += "Connection: close\r\n\r\n"

        # Establish a connection
        sock = self.connect(host, port)
        sock.send(get_rekt)

        # Retrieve the message
        returned_msg = self.recvall(sock)
        sock.close()

        # Parse it and return it
        code = self.get_headers(returned_msg)
        body = self.get_body(returned_msg)

        return HTTPRequest(code, body)

    # receive the url and parse out the host, path and port
    def POST(self, url, args=None):

        parsed_url = urlparse(url)
        host = parsed_url.hostname
        path = parsed_url.path
        port = parsed_url.port
        size = 0
        arg = ""
        
        if(args):
            arg = urllib.urlencode(args)
            #size = sys.getsizeof(arg)
            size = len(arg)

        if(not path):
            path = "/"


        # Construct the GET header
        post_req = "POST " + path + " HTTP/1.1\r\n"
        post_req += "Host:" + host + "\r\n"
        post_req += "Accept: */*\r\n"
        post_req += "Content-Length:" + str(size) + "\r\n"
        post_req += "Content-Type: application/x-www-form-urlencoded\r\n"
        post_req += "Connection: close\r\n\r\n"
        post_req += arg 

        # Establish a connection
        sock = self.connect(host, port)
        sock.send(post_req)
        
        returned_msg = self.recvall(sock)
        sock.close()
        # Parse it and return it
        code = self.get_headers(returned_msg)
        body = self.get_body(returned_msg)    

        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    #client.GET("asdfasd")
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2] ,sys.argv[1])
    else:
        print client.command( sys.argv[1], command) 
