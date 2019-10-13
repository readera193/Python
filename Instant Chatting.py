import argparse, socket
import threading
import json
BUFSIZE = 80
REGISTRAR_PORT = 8136
EOF = "oo"
CODING = 'UTF-8'
# 目前只有client端發送"oo"或^c結束連線

class recvThread(threading.Thread):
    def __init__(self, sock, serverName):
        threading.Thread.__init__(self)
        self.sock = sock
        self.serverName = serverName
    def run(self):
        while True:
            data = self.sock.recv(BUFSIZE).decode(CODING)
            print(self.serverName, ": ", data)

class sendThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            msg = input()
            self.sock.sendall(msg.encode(CODING))

def registrar(host, *args):
    serverList = [];
    registrarSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    registrarSock.bind((host, REGISTRAR_PORT))
    registrarSock.listen(1)
    print("Listening at", registrarSock.getsockname())
    
    while True:
        sock, sockname = registrarSock.accept()
        peerInfo = sock.recv(BUFSIZE).decode(CODING)
        peerInfo = json.loads(peerInfo)
        if peerInfo['command'] == 'register':
            del peerInfo['command']
            serverList.append(peerInfo)
            print("\nNew server {} registers as {}".format(peerInfo['name'], 
                  tuple(peerInfo['address'])))
        elif peerInfo['command'] == 'unregister':
            del peerInfo['command']
            serverList.remove(peerInfo)
            print("\nServer {} unregisters".format(peerInfo['name']))
        elif peerInfo['command'] == 'ask_server_list':
            sock.sendall(json.dumps(len(serverList)).encode(CODING))
            for server in serverList:
                # 避免連續傳送
                sock.recv(BUFSIZE)
                sock.sendall(json.dumps(server).encode(CODING))
        sock.close()

def server(host, port):
    print("Please input your name: ", end='')
    name = input()
    
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    print("\nListening at", listeningSock.getsockname())
    
    # register start
    registerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    registerSock.connect((host, REGISTRAR_PORT))
    registerInfo = {'command':'register','name':name, 'address':listeningSock.getsockname()}
    registerSock.sendall(json.dumps(registerInfo).encode(CODING))
    registerSock.close()
    # register end
    
    # client start
    sock, sockname = listeningSock.accept()
    print("We have accepted a connection from", sockname)
    clientName = sock.recv(BUFSIZE).decode(CODING)
    
    send = sendThread(sock)
    send.daemon = True
    send.start()
    try:
        data = None
        while data != EOF:
            data = sock.recv(BUFSIZE).decode(CODING)
            print(clientName, ": ", data)
    except ConnectionResetError:
        print("client端強制中止")
    
    print("Your peer {} closes the connection.".format(sock.getpeername()))
    sock.close()
    # client end
    
    # unregister
    unregisterSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    unregisterSock.connect((host, REGISTRAR_PORT))
    unregisterInfo = {'command':'unregister','name':name, 'address':listeningSock.getsockname()}
    unregisterSock.sendall(json.dumps(unregisterInfo).encode(CODING))
    unregisterSock.close()
    
    listeningSock.close()
    
def client(host, *args):
    print('Please input your name: ', end='')
    name = input()
    
    # get&show server list
    getServerList = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    getServerList.connect((host, REGISTRAR_PORT))
    getServerList.sendall(json.dumps({'command':'ask_server_list'}).encode(CODING))
    print("\nOnline server:")
    print("num", "name", "address", sep='\t')
    server_num = json.loads(getServerList.recv(BUFSIZE).decode(CODING))
    serverList = []
    for index in range(1, server_num+1):
        # 避免接收太多資料
        getServerList.sendall(b"start")
        server = json.loads(getServerList.recv(BUFSIZE).decode(CODING))
        print(index, server['name'], tuple(server['address']), sep='\t')
        serverList.append(server)
    
    # select server
    print("Input server number to connect: ", end='')
    while True:
        try:
            select = int(input()) - 1
            host, port = serverList[select]['address']
            serverName = serverList[select]['name']
            break
        except (IndexError, ValueError):
            print("Wrong choice, please input currect number: ", end='')
            continue
    
    # connect server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to", sock.getpeername())
    sock.sendall(name.encode(CODING))
    
    # receive thread & send loop
    recv = recvThread(sock, serverName)
    recv.daemon = True
    recv.start()
    try:
        msg = None
        while msg != EOF:
            msg = input()
            sock.sendall(msg.encode(CODING))
    except KeyboardInterrupt:
        print("強制中止")
    
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