import sys, socket, time, pickle, os, tkinter, multiprocessing

BUFFSIZE = 4096
DEFAULT_FOLDER = '/home/ftps/Documents/'
host = ""
port = 8888

def wait(conn, x):
    while conn.recv(BUFFSIZE) != x:
        pass


def login(username, password):

    print('Connecting to server...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))
    except:
        print('Connection not possible at the moment.')
        return None

    print('Connection established.')

    if s.recv(BUFFSIZE) == b'usr':
        s.send(str.encode(username))
    else:
        return None
    if s.recv(BUFFSIZE) == b'pwd':
        s.send(str.encode(password))
    else:
        return None

    if s.recv(BUFFSIZE) == b'1':
        print('Logged in.')
        return s
    else:
        return None
    pass

def server_client(s):

    while True:
        fold = pickle.loads(s.recv(BUFFSIZE))
        for f in fold:
            print(f + ':' + fold[f])
        inn = input()
        if inn == '0':
            s.send(b'0')
            break
        elif inn == '1':
            s.send(b'1')
            print(s.recv(BUFFSIZE).decode('utf-8'))
            inn = input()
            s.send(str.encode(inn))

    print(s.recv(BUFFSIZE).decode('utf-8'))

def receive_file(s, namefile, local):
    s.recv(BUFFSIZE)
    s.send(str.encode(namefile))
    head = pickle.loads(s.recv(BUFFSIZE))
    s.send(b'send')
    print('Receiving file \'' + head[0] + '\'')

    f = open(os.path.join(local, namefile), 'wb')
    while f.tell() != head[1]:
        l = s.recv(BUFFSIZE)
        f.write(l)
    f.close()
    print('File \'' + head[0] + '\' received')
    s.send(b'done')

def send_file(s, namefile):
    wait(s, b'ready')
    s.send(pickle.dumps((os.path.split(namefile)[1], os.stat(namefile).st_size)))
    wait(s, b'send')
    with open(namefile, 'rb') as f:
        l = f.read(BUFFSIZE)
        while l:
            s.send(l)
            l = f.read(BUFFSIZE)
    print('File sent')
    wait(s, b'done')
    s.send(b'1')
    print('File confirmation received')
