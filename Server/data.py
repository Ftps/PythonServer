import sys, socket, time, pickle, os, glob, shutil

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
            create_folder(conn, u)
        elif h == b'3':
            change_folder(conn, u, DEFAULT_FOLDER)
        elif h == b'4':
            delete_object(conn, u)
        elif h == b'5':
            send_file(conn, u)
        elif h == b'6':
            receive_file(conn, u)
        else:
            print('Unknown action.')
            break

    end_conn(conn, add, str.encode('Thank you for accessing our server, ' + u[0] + '. Goodbye.'))


def change_folder(conn, u, folder=None):
    if folder == None:
        conn.send(b'name')
        folder = conn.recv(BUFFSIZE).decode('utf-8')
        print('Changing folder as a request of user ' + u[0] + ' to ' + os.path.realpath(folder))

    os.chdir(folder)
    folder = os.path.split(os.getcwd())[1]

    fold = [(folder, 'Cur', '4096')]
    for elem in glob.glob('*'):
        if os.path.isdir(elem):
            fold.append((elem, 'Dir', '4096'))
        else:
            fold.append((elem, 'File', str(os.stat(elem).st_size)))

    conn.send(pickle.dumps(fold))

def create_folder(conn, u):
    conn.send(b'name')
    folder = conn.recv(BUFFSIZE).decode('utf-8')
    print('Creating folder ' + folder + ' in ' + os.getcwd() + ' as a request of user ' + u[0] + '.')
    folder = os.path.join(os.getcwd(), folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
        conn.send(b'1')
    else:
        conn.send(b'0')

    conn.recv(BUFFSIZE)
    change_folder(conn, u, '.')

def delete_object(conn, u):
    conn.send(b'name')
    obj = conn.recv(BUFFSIZE).decode('utf-8')
    print('Deleting ' + obj + ' in ' + os.getcwd() + ' as a request of user ' + u[0] + '.')
    if os.path.isdir(obj):
        shutil.rmtree(obj)
    else:
        os.remove(obj)

    change_folder(conn, u, '.')

def send_file(conn, u):
    conn.send(b'1')
    namefile = conn.recv(BUFFSIZE).decode('utf-8')
    print('Sending \'' + namefile + '\' to user ' + u[0] + '.')
    conn.send(pickle.dumps((namefile, os.stat(namefile).st_size)))
    wait(conn, b'send')
    with open(namefile, 'rb') as f:
        l = f.read(BUFFSIZE)
        while l:
            conn.send(l)
            l = f.read(BUFFSIZE)
    print('File sent')
    wait(conn, b'done')
    print('File confirmation from user ' + u[0] + ' received.')

def receive_file(conn, u):
    conn.send(b'ready')
    head = pickle.loads(conn.recv(BUFFSIZE))
    conn.send(b'send')
    print('Receiving file \'' + head[0] + '\' from user ' + u[0] + '.')
    f = open(os.path.join(os.getcwd(), head[0]), 'wb')
    while f.tell() != head[1]:
        l = conn.recv(BUFFSIZE)
        f.write(l)
    f.close()
    print('File \'' + head[0] + '\' received from user ' + u[0] + '.')
    conn.send(b'done')
    conn.recv(BUFFSIZE)
    change_folder(conn, u, '.')
