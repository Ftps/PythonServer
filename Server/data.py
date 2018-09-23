import sys, socket, time, pickle, os, glob

BUFFSIZE = 4096
DEFAULT_FOLDER = '/home/ftps/Documents/DataBase'

def wait(conn, x):
    while conn.recv(BUFFSIZE) != x:
        pass

def merge_dicts(*dict_args):
    '''
    Function takes n number of dicts and outputs one
    that is the combination of them all (if some keys are repeated,
    the function will take priority on the later ones)
    '''
    result = {}
    for dic in dict_args:
        result.update(dic)
    return result

def end_conn(conn, add, x):
    print('Connection ended with this client: ' + add[0] + ':' + str(add[1]))
    conn.send(x)
    conn.close()




def start_user(conn, add):
    den = 1
    conn.send(b'usr')
    user = conn.recv(BUFFSIZE)
    conn.send(b'pwd')
    password = conn.recv(BUFFSIZE)
    with open('/home/ftps/Prog/PythonServer/Server/Data/User.txt', encoding='utf-8') as f:
        for line in f:
            u = line.split(None, 3)
            if str.encode(u[0]) == user and str.encode(u[1]) == password:
                conn.send(b'1')
                den = 0
                break

    if den:
        print('Adress denied to ' + add[0] + ':' + str(add[1]))
        end_conn(conn, add, b'0')
    else:
        print('Acess granted to ' + add[0] + ':' + str(add[1]) + ' as ' + u[0])
        data_base(conn, add, u)

    pass




def data_base(conn, add, u):
    print("Client " + add[0] + ':' + str(add[1]) + ' accessed server.')
    change_folder(conn, u, DEFAULT_FOLDER)
    while True:
        h = conn.recv(BUFFSIZE)
        if h == b'0':
            break
        elif h == b'1':
            change_folder(conn, u)
        elif h == b'2':
            pass
            #send_file
        elif h == b'3':
            pass
            #receive_file
        else:
            pass

    end_conn(conn, add, str.encode('Thank you for accessing our server, ' + u[0] + '. Goodbye.'))


def change_folder(conn, u, folder=None):
    if folder == None:
        conn.send(b'Send folder name')
        folder = conn.recv(BUFFSIZE).decode('utf-8')
        print('Changing folder as a request of user ' + u[0] + ' to ' + os.path.realpath(folder))

    os.chdir(folder)
    fold = {os.path.realpath(folder):'loc'}
    for elem in glob.glob('*'):
        if os.path.isdir(elem):
            fold.update({elem:'dir'})
        else:
            fold.update({elem:'fil'})


    conn.send(pickle.dumps(fold))

def send_file(conn, add, namefile):
    print('Sending \'' + namefile + '\' to ' + add[0] + ':' + str(add[1]))
    wait(conn, b'ready')
    conn.send(pickle.dumps((namefile, os.stat(namefile).st_size)))
    wait(conn, b'send')
    with open(namefile, 'rb') as f:
        l = f.read(BUFFSIZE)
        while l:
            conn.send(l)
            l = f.read(BUFFSIZE)
    print('File sent')
    wait(conn, b'done')
    print('File confirmation from ' + add[0] + ':' + str(add[1]) + ' received')
    time.sleep(0.5)

def receive_file(conn, add, local=DEFAULT_FOLDER):
    conn.send(b'ready')
    head = pickle.loads(conn.recv(BUFFSIZE))
    conn.send(b'send')
    print('Receiving file \'' + head[0] + '\' from ' + add[0] + ':' + str(add[1]))
    f = open(local + head[0], 'wb')
    while f.tell() != head[1]:
        l = conn.recv(BUFFSIZE)
        f.write(l)
    f.close()
    print('File \'' + head[0] + '\' received from ' + add[0] + ':' + str(add[1]))
    conn.send(b'done')
