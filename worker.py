import socket
import zmq
import sys
import time
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://localhost:1337")
while True:
    filename = socket.recv()
    if os.path.isfile(filename):
        socket.send_json({'result' : 'success', 'content' : open(filename).read()})
    else:
        socket.send_json({'result' : 'fail', 'error' : 'not found')
    print("done")
