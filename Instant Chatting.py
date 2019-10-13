import argparse, socket
import threading
import json
BUFSIZE = 150
REGISTRAR_PORT = 5060
EOF = 'oo'
CODING = 'UTF-8'

class threadRecv(threading.Thread):
    def __init__(self, sock, serverName):
        threading.Thread.__init__(self)
        self.sock = sock
        self.serverName = serverName
    def run(self):
        while True:
            data = self.sock.recv(BUFSIZE).decode(CODING)
            print(self.serverName, ": ", data)

class threadSend(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            msg = input()
            self.sock.sendall(msg.encode(CODING))

def registrar(host, *args):
    servers = [];
    registrarSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    registrarSock.bind((host, REGISTRAR_PORT))
    registrarSock.listen(1)
    print("Listening at", registrarSock.getsockname())
    
    while True:
        sock, sockname = registrarSock.accept()
        peerInfo = sock.recv(BUFSIZE).decode(CODING)
        peerInfo = json.loads(peerInfo)
        if peerInfo['role'] == 'server':
            peerInfo.pop('role')
            servers.append(peerInfo)
            print("\nNew server {} registers as {}".format(peerInfo['name'], 
                  tuple(peerInfo['address'])))
        elif peerInfo['role'] == 'client':
            sock.sendall(json.dumps(servers).encode(CODING))
        sock.close()

def server(host, port):
    print("Please input your name: ", end='')
    name = input()
    
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    print("\nListening at", listeningSock.getsockname())
    
    registerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    registerSock.connect((host, REGISTRAR_PORT))
    registerInfo = {'role':'server','name':name, 'address':listeningSock.getsockname()}
    registerSock.sendall(json.dumps(registerInfo).encode(CODING))
    registerSock.close()
    
    sock, sockname = listeningSock.accept()
    print("We have accepted a connection from", sockname)
    clientName = sock.recv(BUFSIZE).decode(CODING)
    
    send = threadSend(sock)
    send.daemon = True
    send.start()
    
    data = None
    while data != EOF:
        data = sock.recv(BUFSIZE).decode(CODING)
        print(clientName, ": ", data)
    
    print("Your peer {} closes the connection.".format(sock.getpeername()))
    sock.close()
    listeningSock.close()
    
def client(host, *args):
    print('Please input your name: ', end='')
    name = input()
    getServers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    getServers.connect((host, REGISTRAR_PORT))
    getServers.sendall(json.dumps({'role':'client'}).encode(CODING))
    servers = json.loads(getServers.recv(BUFSIZE).decode(CODING))
    index = 1
    print("\nOnline server:")
    print("num", "name", "address", sep='\t')
    for server in servers:
        print(index, server['name'], tuple(server['address']), sep='\t')
        index += 1
    
    print("Input server number to connect: ", end='')
    while True:
        try:
            select = int(input()) - 1
            host, port = servers[select]['address']
            serverName = servers[select]['name']
        except (IndexError, ValueError):
            print("Wrong choice, please input currect number: ", end='')
            continue
        else:
            break
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to", sock.getpeername())
    sock.sendall(name.encode(CODING))
    
    recv = threadRecv(sock, serverName)
    recv.daemon = True
    recv.start()
    
    msg = None
    while msg != EOF:
        msg = input()
        sock.sendall(msg.encode(CODING))
    
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