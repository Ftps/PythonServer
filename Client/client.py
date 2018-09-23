#!/usr/bin/python3 -B

import sys, socket
import data

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket.')
    sys.exit()
print('Socket created')

host = "193.136.143.133"
port = 8888
print('Connecting to server...')
s.connect((host, port))
print('Connection achieved')

if data.login(s) == 1:
    print('Login successful')
    data.server_client(s)
else:
    pass
    print('Access denied')
    #do nothing

s.close()
