#!/usr/bin/python3 -B

import sys, socket
from _thread import *
import data

HOST = socket.gethostname()
PORT = 8888
NUMBER_CONNECT = 5

try:
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket.')
    sys.exit()
print('Socket created')

try:
    serv.bind((HOST, PORT))
except socket.error:
    print('Bind failed')
    sys.exit()
print('Bind complete')

serv.listen(NUMBER_CONNECT)
print('Socket is listening...')

while True:
    conn, addr = serv.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    start_new_thread(data.start_user, (conn, addr,))
