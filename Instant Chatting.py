import argparse, socket
import threading
import json
BUFSIZE = 80
REGISTRAR_PORT = 648
EOF = 'oo'

class threadRecv(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            data = self.sock.recv(BUFSIZE)
            print(">>", data.decode('UTF-8'))

class threadSend(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            msg = input()
            self.sock.sendall(msg.encode('UTF-8'))

def registrar(host, *args):
    servers = [];
    registrarSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    registrarSock.bind((host, REGISTRAR_PORT))
    registrarSock.listen(1)
    print('Waiting to accept a new register')
    
    while True:
        sock, sockname = registrarSock.accept()
        peerInfo = sock.recv(BUFSIZE).decode('UTF-8')
        peerInfo = json.loads(peerInfo)
        if peerInfo['role'] == 'server':
            servers.append(peerInfo)
            print("\nOnline server update:")
            print("name", "address", sep='\t')
            for server in servers:
                print(server['name'], tuple(server['address']), sep='\t')
        elif peerInfo['role'] == 'client':
            sock.sendall(json.dumps(servers).encode('UTF-8'))
            #sock.recv(BUFSIZE)
        sock.close()

def server(host, port):
    print('Please input your name:')
    name = input()
    
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    print("Listening at", listeningSock.getsockname())
    
    registerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    registerSock.connect((host, REGISTRAR_PORT))
    registerInfo = {'role':'server','name':name, 'address':listeningSock.getsockname()}
    registerInfo = json.dumps(registerInfo)
    registerSock.sendall(registerInfo.encode('UTF-8'))
    registerSock.close()
    
    sock, sockname = listeningSock.accept()
    print("We have accepted a connection from", sockname)
    recv = threadRecv(sock)
    recv.start()
    send = threadSend(sock)
    send.start()
    
    recv.join()
    send.join()
    print("Your peer {} closes the connection.".format(sock.getpeername() ))
    sock.close()
    listeningSock.close()
    
def client(host, *args):
    print('Please input your name:')
    name = input()
    getServers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    getServers.connect((host, REGISTRAR_PORT))
    getServers.sendall(json.dumps({'role':'client'}).encode('UTF-8'))
    servers = json.loads(getServers.recv(BUFSIZE).decode('UTF-8'))
    index = 0
    print("Online server:")
    print("num", "name", "address", sep='\t')
    for server in servers:
        print(index, server['name'], tuple(server['address']), sep='\t')
        index += 1
    
    print("Input server num to connect:", end=' ')
    while True:
        select = input()
        try:
            host, port = servers[int(select)]['address']
            serverName = servers[int(select)]['name']
            break
        except:
            print("Please input currect number:", end=' ')
            continue
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to", sock.getpeername())
    
    recv = threadRecv(sock)
    recv.start()
    send = threadSend(sock)
    send.start()
    
    recv.join()
    send.join()
    sock.close()
    
if __name__ == '__main__':
    choices = {'client':client, 'server':server, 'registrar':registrar}
    parser = argparse.ArgumentParser(description='Chat over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=0,
                        help='TCP port (default 0)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)