import socket
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import os
import zmq
import urlparse

def getFile(filename):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:1337")
    socket.send(filename)
    response = socket.recv_json()
    return response

class HttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        result = getFile(self.path[1:])
        res1=result.get('result')
        if  res1== 'success':
            self.send_response(200)
            self.send_header('content-type','application/octet-stream')
            self.end_headers()
            res2=result.get('content')
            self.wfile.write(res2)
        else:
            self.send_response(400)
            self.send_header('content-type','text/html')
            self.end_headers()
            res3=result.get('error')
            self.wfile.write(res3)

server = HTTPServer(("localhost", 8080), HttpServer)
server.serve_forever()
